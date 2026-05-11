"""
日志系统模块 - 提供统一的日志记录功能

功能特性:
- 文件日志和控制台日志双输出
- 支持多种日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- 日志文件自动轮转 (按大小和时间)
- 集成 PySide6 Signal 便于 UI 层监听日志消息
- 可定制的日志格式

使用方法:
    from utils.logger import Logger
    
    # 获取全局日志器实例
    logger = Logger.get_instance()
    
    # 记录不同级别的日志
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误")
"""

import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PySide6.QtCore import QObject, Signal, Slot
    HAS_PYSIDE6 = True
except ImportError:
    HAS_PYSIDE6 = False


class LogSignalEmitter(QObject if HAS_PYSIDE6 else object):
    """
    日志信号发射器 - 用于跨线程传递日志消息到 UI 层
    
    当使用 PySide6 时,提供 Qt Signal 支持,可在主线程中接收日志消息并显示在 UI 上
    当未安装 PySide6 时,提供回退机制保证代码仍可运行
    """
    
    if HAS_PYSIDE6:
        # 定义 Qt Signal 信号,用于传递日志消息
        # level: 日志级别 (int)
        # message: 日志消息内容 (str)
        # 时间戳由日志处理器自动添加
        log_message = Signal(int, str)


class Logger:
    """
    日志系统主类 - 提供统一的日志记录接口
    
    特性:
    - 单例模式,全局共享一个日志器实例
    - 支持控制台和文件双输出
    - 支持日志文件自动轮转
    - 支持 PySide6 Signal 信号集成
    """
    
    _instance: Optional['Logger'] = None  # 单例实例
    _initialized: bool = False  # 初始化标志
    
    # 默认日志格式 - 包含时间戳、级别、模块名和消息
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # 简化格式 - 用于控制台输出
    SIMPLE_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    def __init__(
        self,
        name: str = 'ImageForge',
        log_dir: Optional[str] = None,
        log_level: int = logging.DEBUG,
        console_output: bool = True,
        file_output: bool = True,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        when: str = 'midnight',
        interval: int = 1
    ):
        """
        初始化日志系统
        
        Args:
            name: 日志器名称,默认为 'ImageForge'
            log_dir: 日志文件目录,默认为用户配置目录下的 logs 文件夹
            log_level: 日志级别,默认为 DEBUG
            console_output: 是否输出到控制台,默认 True
            file_output: 是否输出到文件,默认 True
            max_bytes: 单个日志文件最大字节数,超过后自动轮转
            backup_count: 保留的备份文件数量
            when: 时间轮转的时间单位 ('midnight', 'H', 'D', 'W0'-'W6')
            interval: 轮转间隔,配合 when 使用
        """
        self.name = name
        self.log_level = log_level
        self.console_output = console_output
        self.file_output = file_output
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.when = when
        self.interval = interval
        
        # 设置日志目录
        if log_dir is None:
            self.log_dir = self._get_default_log_dir()
        else:
            self.log_dir = Path(log_dir)
        
        # 创建日志目录(如果不存在)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 日志文件路径
        self.log_file = self.log_dir / f'{name}.log'
        
        # 创建 Python logging 日志器
        self._logger = logging.getLogger(name)
        self._logger.setLevel(log_level)
        self._logger.propagate = False  # 防止日志向上传播
        
        # 信号发射器 - 用于发送日志消息到 UI
        self.signal_emitter = LogSignalEmitter()
        
        # 设置日志处理器
        self._setup_handlers()
        
    def _get_default_log_dir(self) -> Path:
        """
        获取默认的日志目录
        
        优先使用用户配置目录,否则使用当前目录下的 logs 文件夹
        
        Returns:
            Path: 日志目录路径
        """
        try:
            from PySide6.QtCore import QStandardPaths
            # 使用 Qt 的标准路径获取用户文档目录
            config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
            log_dir = Path(config_dir) / 'logs'
        except ImportError:
            # 回退到当前目录
            log_dir = Path.cwd() / 'logs'
        
        return log_dir
    
    def _setup_handlers(self):
        """
        设置日志处理器
        
        根据配置添加控制台处理器和/或文件处理器
        """
        # 清除已有的处理器,避免重复添加
        self._logger.handlers.clear()
        
        # 添加控制台处理器
        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_formatter = logging.Formatter(self.SIMPLE_FORMAT, datefmt='%H:%M:%S')
            console_handler.setFormatter(console_formatter)
            self._logger.addHandler(console_handler)
        
        # 添加文件处理器 - 使用 RotatingFileHandler 按大小轮转
        if self.file_output:
            file_handler = RotatingFileHandler(
                filename=str(self.log_file),
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.log_level)
            file_formatter = logging.Formatter(self.DEFAULT_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
    
    @classmethod
    def get_instance(
        cls,
        name: str = 'ImageForge',
        log_dir: Optional[str] = None,
        log_level: int = logging.DEBUG,
        **kwargs
    ) -> 'Logger':
        """
        获取日志系统单例实例
        
        Args:
            name: 日志器名称
            log_dir: 日志目录
            log_level: 日志级别
            **kwargs: 其他配置参数
            
        Returns:
            Logger: 日志系统实例
        """
        if cls._instance is None:
            cls._instance = cls(
                name=name,
                log_dir=log_dir,
                log_level=log_level,
                **kwargs
            )
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """
        重置单例实例
        
        用于测试或重新初始化日志系统
        """
        if cls._instance is not None:
            # 关闭所有处理器
            for handler in cls._instance._logger.handlers:
                handler.close()
                cls._instance._logger.removeHandler(handler)
            
            cls._instance = None
    
    def set_level(self, level: int):
        """
        设置日志级别
        
        Args:
            level: 日志级别 (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_level = level
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)
    
    def _emit_signal(self, level: int, message: str):
        """
        发射日志信号
        
        如果使用了 PySide6,会将日志消息通过 Signal 发送到主线程
        
        Args:
            level: 日志级别
            message: 日志消息
        """
        if HAS_PYSIDE6 and hasattr(self.signal_emitter, 'log_message'):
            self.signal_emitter.log_message.emit(level, message)
    
    def debug(self, message: str):
        """
        记录 DEBUG 级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.debug(message)
        self._emit_signal(logging.DEBUG, message)
    
    def info(self, message: str):
        """
        记录 INFO 级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.info(message)
        self._emit_signal(logging.INFO, message)
    
    def warning(self, message: str):
        """
        记录 WARNING 级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.warning(message)
        self._emit_signal(logging.WARNING, message)
    
    def error(self, message: str):
        """
        记录 ERROR 级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.error(message)
        self._emit_signal(logging.ERROR, message)
    
    def critical(self, message: str):
        """
        记录 CRITICAL 级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.critical(message)
        self._emit_signal(logging.CRITICAL, message)
    
    def exception(self, message: str, exc_info: bool = True):
        """
        记录异常信息
        
        自动添加异常堆栈跟踪信息
        
        Args:
            message: 日志消息
            exc_info: 是否包含异常信息,默认为 True
        """
        self._logger.exception(message, exc_info=exc_info)
        self._emit_signal(logging.ERROR, message)
    
    def log(self, level: int, message: str):
        """
        通用日志记录方法
        
        Args:
            level: 日志级别
            message: 日志消息
        """
        self._logger.log(level, message)
        self._emit_signal(level, message)
    
    @property
    def logger(self) -> logging.Logger:
        """
        获取底层的 Python logging 日志器
        
        Returns:
            logging.Logger: Python 日志器实例
        """
        return self._logger


# 创建便捷函数,用于快速获取日志器
def get_logger(**kwargs) -> Logger:
    """
    获取日志系统实例的便捷函数
    
    Args:
        **kwargs: 传递给 Logger.get_instance 的参数
        
    Returns:
        Logger: 日志系统实例
    """
    return Logger.get_instance(**kwargs)


if __name__ == '__main__':
    # 测试日志系统
    print("测试日志系统...")
    
    # 获取日志器实例
    logger = Logger.get_instance(
        name='TestLogger',
        log_level=logging.DEBUG,
        console_output=True,
        file_output=True
    )
    
    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")
    
    # 测试异常日志
    try:
        raise ValueError("测试异常")
    except Exception:
        logger.exception("捕获到异常")
    
    print(f"\n日志文件位置: {logger.log_file}")
    print("日志系统测试完成!")
