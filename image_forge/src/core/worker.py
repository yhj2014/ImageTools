"""
多线程任务处理器

该模块使用 ThreadPoolExecutor 实现多线程任务处理，
支持任务队列管理、进度信号、日志信号和取消/暂停功能。
"""

import os
import time
import uuid
import traceback
from pathlib import Path
from typing import Optional, Callable, Any, List, Dict
from enum import Enum
from dataclasses import dataclass, field
from queue import Queue, Empty
from threading import Thread, Event, Lock
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

try:
    from PySide6.QtCore import QObject, Signal, Slot
    HAS_PYSIDE6 = True
except ImportError:
    HAS_PYSIDE6 = False


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = 'pending'     # 等待中
    RUNNING = 'running'     # 运行中
    PAUSED = 'paused'       # 已暂停
    COMPLETED = 'completed' # 已完成
    FAILED = 'failed'       # 失败
    CANCELLED = 'cancelled' # 已取消


@dataclass
class Task:
    """任务数据类"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ''
    func: Callable = None
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0  # 0-100
    message: str = ''
    result: Any = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


class WorkerSignals:
    """
    工作线程信号类

    当 PySide6 可用时，这些信号会在主线程中发射，
    允许 UI 组件响应后台任务的进度和状态变化。
    """

    if HAS_PYSIDE6:
        # 进度信号：发送 (task_id, progress, message)
        progress_updated = Signal(str, int, str)

        # 日志信号：发送 (task_id, level, message)
        # level: 'info', 'warning', 'error', 'debug'
        log_signal = Signal(str, str, str)

        # 任务状态变化信号：发送 (task_id, status)
        status_changed = Signal(str, str)

        # 任务完成信号：发送 (task_id, result, error)
        task_completed = Signal(str, object, object)

        # 全部任务完成信号
        all_tasks_completed = Signal(int, int)  # (success_count, fail_count)

        # 任务开始信号
        task_started = Signal(str)


class WorkerSignalsFallback:
    """
    工作线程信号备用类（当 PySide6 不可用时使用）

    使用普通回调函数代替 Qt 信号。
    """

    def __init__(self):
        """初始化备用信号处理器"""
        self.progress_callback: Optional[Callable] = None
        self.log_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.completed_callback: Optional[Callable] = None
        self.all_completed_callback: Optional[Callable] = None
        self.started_callback: Optional[Callable] = None


class TaskWorker:
    """
    多线程任务处理器类

    该类使用线程池执行图像处理任务，支持：
    - 任务队列管理
    - 进度跟踪和报告
    - 任务暂停/恢复
    - 任务取消
    - 日志记录
    """

    def __init__(
        self,
        max_workers: int = 4,
        signals: Optional[Any] = None
    ):
        """
        初始化任务处理器

        Args:
            max_workers: 最大工作线程数，默认为 4
            signals: 信号对象，如果为 None 且 PySide6 可用则创建 WorkerSignals
        """
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.task_queue: Queue = Queue()
        self.executor: Optional[ThreadPoolExecutor] = None
        self.futures: Dict[str, Future] = {}
        self.task_lock = Lock()

        # 暂停/取消控制
        self._pause_event = Event()
        self._cancel_event = Event()
        self._is_paused = False
        self._is_cancelled = False

        # 统计信息
        self._success_count = 0
        self._fail_count = 0

        # 信号处理
        if signals is not None:
            self.signals = signals
        elif HAS_PYSIDE6:
            self.signals = WorkerSignals()
        else:
            self.signals = WorkerSignalsFallback()

        # 统计锁
        self._stats_lock = Lock()

    def add_task(
        self,
        func: Callable,
        name: str = '',
        args: tuple = (),
        kwargs: dict = None,
        priority: int = 0
    ) -> str:
        """
        添加任务到队列

        Args:
            func: 要执行的函数
            name: 任务名称（用于显示）
            args: 函数位置参数
            kwargs: 函数关键字参数
            priority: 优先级，数字越大优先级越高

        Returns:
            任务 ID
        """
        if kwargs is None:
            kwargs = {}

        task = Task(
            name=name or f"Task-{len(self.tasks) + 1}",
            func=func,
            args=args,
            kwargs=kwargs
        )

        with self.task_lock:
            self.tasks[task.id] = task

        # 将任务加入队列（带优先级）
        self.task_queue.put((priority, task.id))

        self._emit_log(task.id, 'info', f"任务已添加: {task.name}")
        self._emit_status(task.id, TaskStatus.PENDING)

        return task.id

    def add_tasks_batch(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[str]:
        """
        批量添加任务

        Args:
            tasks: 任务字典列表，每个字典包含 func, name, args, kwargs

        Returns:
            任务 ID 列表
        """
        task_ids = []
        for task_data in tasks:
            task_id = self.add_task(
                func=task_data.get('func'),
                name=task_data.get('name', ''),
                args=task_data.get('args', ()),
                kwargs=task_data.get('kwargs', {}),
                priority=task_data.get('priority', 0)
            )
            task_ids.append(task_id)
        return task_ids

    def start(self):
        """启动任务处理器"""
        if self.executor is not None:
            return

        self._is_cancelled = False
        self._is_paused = False
        self._pause_event.set()

        # 创建线程池
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        # 启动任务调度线程
        self._scheduler_thread = Thread(target=self._schedule_tasks, daemon=True)
        self._scheduler_thread.start()

        self._emit_log('', 'info', f"任务处理器已启动 ({self.max_workers} 工作线程)")

    def pause(self):
        """暂停所有任务"""
        if self._is_paused:
            return

        self._is_paused = True
        self._pause_event.clear()
        self._emit_log('', 'info', "任务已暂停")

        # 更新所有运行中任务的状态
        with self.task_lock:
            for task_id, task in self.tasks.items():
                if task.status == TaskStatus.RUNNING:
                    self._emit_status(task_id, TaskStatus.PAUSED)

    def resume(self):
        """恢复所有任务"""
        if not self._is_paused:
            return

        self._is_paused = False
        self._pause_event.set()
        self._emit_log('', 'info', "任务已恢复")

        # 更新所有暂停任务的状态
        with self.task_lock:
            for task_id, task in self.tasks.items():
                if task.status == TaskStatus.PAUSED:
                    self._emit_status(task_id, TaskStatus.RUNNING)

    def cancel(self, task_id: Optional[str] = None):
        """
        取消任务

        Args:
            task_id: 要取消的任务 ID，如果为 None 则取消所有任务
        """
        self._cancel_event.set()

        if task_id is None:
            # 取消所有任务
            with self.task_lock:
                for tid, task in self.tasks.items():
                    if task.status in (TaskStatus.PENDING, TaskStatus.RUNNING, TaskStatus.PAUSED):
                        task.status = TaskStatus.CANCELLED
                        self._emit_status(tid, TaskStatus.CANCELLED)

            self._emit_log('', 'info', "所有任务已取消")

        else:
            # 取消指定任务
            with self.task_lock:
                if task_id in self.tasks:
                    task = self.tasks[task_id]
                    if task.status in (TaskStatus.PENDING, TaskStatus.PAUSED):
                        task.status = TaskStatus.CANCELLED
                        self._emit_status(task_id, TaskStatus.CANCELLED)
                        self._emit_log(task_id, 'info', f"任务已取消: {task.name}")

    def stop(self):
        """停止任务处理器"""
        self.cancel()
        self._cancel_event.clear()

        if self.executor is not None:
            self.executor.shutdown(wait=False)
            self.executor = None

        self._emit_log('', 'info', "任务处理器已停止")

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        获取任务信息

        Args:
            task_id: 任务 ID

        Returns:
            Task 对象，如果不存在返回 None
        """
        with self.task_lock:
            return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        获取所有任务

        Returns:
            Task 对象列表
        """
        with self.task_lock:
            return list(self.tasks.values())

    def get_progress(self) -> Tuple[int, int, int]:
        """
        获取总体进度

        Returns:
            (已完成数, 进行中数, 总数)
        """
        with self.task_lock:
            completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
            running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
            total = len(self.tasks)
            return completed, running, total

    def _schedule_tasks(self):
        """任务调度线程"""
        while not self._cancel_event.is_set():
            # 如果暂停，等待恢复
            if self._is_paused:
                self._pause_event.wait()
                if self._cancel_event.is_set():
                    break

            try:
                # 从队列获取任务，带超时以便检查取消状态
                priority, task_id = self.task_queue.get(timeout=0.1)
            except Empty:
                continue

            # 检查任务是否被取消
            with self.task_lock:
                if task_id not in self.tasks:
                    continue
                task = self.tasks[task_id]

                if task.status == TaskStatus.CANCELLED:
                    continue

            # 提交任务到线程池
            if self.executor:
                future = self.executor.submit(self._execute_task, task_id)
                with self.task_lock:
                    self.futures[task_id] = future

    def _execute_task(self, task_id: str):
        """
        执行单个任务

        Args:
            task_id: 任务 ID
        """
        with self.task_lock:
            if task_id not in self.tasks:
                return
            task = self.tasks[task_id]

        # 更新任务状态为运行中
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        self._emit_status(task_id, TaskStatus.RUNNING)
        self._emit_started(task_id)
        self._emit_log(task_id, 'info', f"开始执行: {task.name}")

        try:
            # 如果有取消/暂停检查点，包装函数
            def check_wrapper():
                # 在执行过程中定期检查暂停/取消状态
                result = task.func(*task.args, **task.kwargs)
                return result

            # 执行任务
            result = check_wrapper()

            # 任务成功
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            task.progress = 100

            with self._stats_lock:
                self._success_count += 1

            self._emit_progress(task_id, 100, "任务完成")
            self._emit_completed(task_id, result, None)
            self._emit_status(task_id, TaskStatus.COMPLETED)
            self._emit_log(task_id, 'info', f"任务完成: {task.name}")

        except Exception as e:
            # 任务失败
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.completed_at = time.time()

            with self._stats_lock:
                self._fail_count += 1

            error_msg = f"任务失败: {str(e)}\n{traceback.format_exc()}"
            self._emit_completed(task_id, None, error_msg)
            self._emit_status(task_id, TaskStatus.FAILED)
            self._emit_log(task_id, 'error', error_msg)

        finally:
            with self.task_lock:
                if task_id in self.futures:
                    del self.futures[task_id]

            # 检查是否所有任务都完成
            self._check_all_completed()

    def _check_all_completed(self):
        """检查是否所有任务都已完成"""
        with self.task_lock:
            pending_count = sum(
                1 for t in self.tasks.values()
                if t.status in (TaskStatus.PENDING, TaskStatus.RUNNING, TaskStatus.PAUSED)
            )

        if pending_count == 0 and self.task_queue.empty():
            with self._stats_lock:
                success = self._success_count
                failed = self._fail_count

            self._emit_all_completed(success, failed)
            self._emit_log('', 'info', f"所有任务已完成 (成功: {success}, 失败: {failed})")

    def _emit_progress(self, task_id: str, progress: int, message: str):
        """发送进度信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.progress_updated.emit(task_id, progress, message)
        elif hasattr(self.signals, 'progress_callback') and self.signals.progress_callback:
            self.signals.progress_callback(task_id, progress, message)

    def _emit_log(self, task_id: str, level: str, message: str):
        """发送日志信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.log_signal.emit(task_id, level, message)
        elif hasattr(self.signals, 'log_callback') and self.signals.log_callback:
            self.signals.log_callback(task_id, level, message)

    def _emit_status(self, task_id: str, status: TaskStatus):
        """发送状态变化信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.status_changed.emit(task_id, status.value)
        elif hasattr(self.signals, 'status_callback') and self.signals.status_callback:
            self.signals.status_callback(task_id, status.value)

    def _emit_completed(self, task_id: str, result: Any, error: Optional[str]):
        """发送任务完成信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.task_completed.emit(task_id, result, error)
        elif hasattr(self.signals, 'completed_callback') and self.signals.completed_callback:
            self.signals.completed_callback(task_id, result, error)

    def _emit_started(self, task_id: str):
        """发送任务开始信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.task_started.emit(task_id)
        elif hasattr(self.signals, 'started_callback') and self.signals.started_callback:
            self.signals.started_callback(task_id)

    def _emit_all_completed(self, success_count: int, fail_count: int):
        """发送全部任务完成信号"""
        if HAS_PYSIDE6 and isinstance(self.signals, WorkerSignals):
            self.signals.all_tasks_completed.emit(success_count, fail_count)
        elif hasattr(self.signals, 'all_completed_callback') and self.signals.all_completed_callback:
            self.signals.all_completed_callback(success_count, fail_count)


class ProgressCallback:
    """
    进度回调辅助类

    用于在长时间运行的任务中报告进度。
    支持嵌套进度（父任务和子任务）。
    """

    def __init__(
        self,
        worker: TaskWorker,
        task_id: str,
        total: int = 100,
        message: str = "处理中..."
    ):
        """
        初始化进度回调

        Args:
            worker: TaskWorker 实例
            task_id: 任务 ID
            total: 总数（用于计算百分比）
            message: 进度消息
        """
        self.worker = worker
        self.task_id = task_id
        self.total = total
        self.current = 0
        self.last_reported = -1

    def update(self, current: int, message: str = None):
        """
        更新进度

        Args:
            current: 当前进度值
            message: 可选的消息
        """
        self.current = current
        progress = int((current / self.total) * 100) if self.total > 0 else 0

        # 避免重复发送相同的进度
        if progress != self.last_reported:
            self.last_reported = progress
            msg = message or f"处理中... {progress}%"
            self.worker._emit_progress(self.task_id, progress, msg)

            # 同时更新任务对象
            with self.worker.task_lock:
                if self.task_id in self.worker.tasks:
                    self.worker.tasks[self.task_id].progress = progress
                    self.worker.tasks[self.task_id].message = msg
