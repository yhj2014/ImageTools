from concurrent.futures import ThreadPoolExecutor, Future
from typing import List, Optional, Callable
from pathlib import Path

from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QWidget

from core.converter import ImageConverter, OUTPUT_FORMATS
from utils.logger import logger


class ConversionWorker(QObject):
    progress_changed = Signal(int, int, str)
    log_message = Signal(str, str)
    conversion_complete = Signal(bool, int, int)
    single_conversion_done = Signal(bool, str, str)

    def __init__(
        self,
        max_workers: int = 4,
        quality: int = 85,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._converter = ImageConverter()
        self._max_workers = max_workers
        self._quality = quality
        self._is_running = False
        self._is_cancelled = False
        self._executor: Optional[ThreadPoolExecutor] = None

    def set_quality(self, quality: int) -> None:
        self._quality = max(1, min(100, quality))

    def set_max_workers(self, max_workers: int) -> None:
        self._max_workers = max(1, min(16, max_workers))

    def is_running(self) -> bool:
        return self._is_running

    def cancel(self) -> None:
        self._is_cancelled = True
        if self._executor:
            self._executor.shutdown(wait=False, cancel_futures=True)

    def _process_single_file(
        self,
        input_path: str,
        output_path: str,
        index: int,
        total: int
    ) -> tuple[bool, str, str]:
        filename = Path(input_path).name
        self.log_message.emit("INFO", f"正在转换 [{index+1}/{total}]: {filename}")

        success, message = self._converter.convert(
            input_path,
            output_path,
            quality=self._quality
        )

        if success:
            self.log_message.emit("INFO", f"✓ 转换成功: {filename}")
        else:
            self.log_message.emit("ERROR", f"✗ 转换失败: {filename} - {message}")

        self.progress_changed.emit(index + 1, total, filename)
        self.single_conversion_done.emit(success, input_path, message)

        return success, input_path, message

    def process_files(
        self,
        file_list: List[str],
        output_format: str,
        output_dir: str
    ) -> None:
        if not file_list:
            self.log_message.emit("WARNING", "文件列表为空")
            self.conversion_complete.emit(False, 0, 0)
            return

        if not self._converter.is_ffmpeg_available():
            self.log_message.emit("ERROR", "FFmpeg 不可用，请检查安装")
            self.conversion_complete.emit(False, 0, 0)
            return

        self._is_running = True
        self._is_cancelled = False
        total = len(file_list)
        self.log_message.emit("INFO", f"开始批量转换，共 {total} 个文件")
        self.log_message.emit("INFO", f"输出格式: {output_format.upper()}, 输出目录: {output_dir}")

        tasks = []
        for i, input_path in enumerate(file_list):
            output_path = self._converter.get_output_filename(
                input_path,
                output_format,
                output_dir
            )
            tasks.append((input_path, output_path, i, total))

        success_count = 0
        failed_count = 0

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = []
            for input_path, output_path, index, tot in tasks:
                if self._is_cancelled:
                    break
                future = executor.submit(
                    self._process_single_file,
                    input_path,
                    output_path,
                    index,
                    tot
                )
                futures.append(future)

            for future in futures:
                if self._is_cancelled:
                    break
                try:
                    success, _, _ = future.result(timeout=120)
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    self.log_message.emit("ERROR", f"处理异常: {str(e)}")

        self._is_running = False
        self.log_message.emit(
            "INFO",
            f"批量转换完成: 成功 {success_count}, 失败 {failed_count}"
        )
        self.conversion_complete.emit(True, success_count, failed_count)
