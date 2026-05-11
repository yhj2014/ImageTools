"""ImageForge 应用主类"""
from typing import Optional
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication

from utils.logger import get_logger
from utils.config import get_config


class ImageForgeApp(QObject):
    """ImageForge 应用主类

    管理应用生命周期和全局状态
    """
    initialized = Signal()
    about_to_quit = Signal()

    _instance: Optional['ImageForgeApp'] = None

    def __init__(self):
        super().__init__()
        ImageForgeApp._instance = self

        self._logger = get_logger()
        self._config = get_config()
        self._is_initialized = False
        self._is_running = False

    @classmethod
    def get_instance(cls) -> Optional['ImageForgeApp']:
        """获取单例实例"""
        return cls._instance

    def initialize(self) -> bool:
        """初始化应用

        Returns:
            是否初始化成功
        """
        if self._is_initialized:
            return True

        try:
            self._logger.info("初始化 ImageForge...")

            self._config.load()
            self._logger.info("配置加载完成")

            self._is_initialized = True
            self.initialized.emit()

            self._logger.info("ImageForge 初始化完成")
            return True

        except Exception as e:
            self._logger.error(f"初始化失败: {str(e)}")
            return False

    def run(self) -> int:
        """运行应用

        Returns:
            退出码
        """
        if not self._is_initialized:
            if not self.initialize():
                return 1

        self._is_running = True

        app = QApplication.instance()
        if app is None:
            self._logger.error("QApplication 未创建")
            return 1

        try:
            return app.exec()
        finally:
            self._is_running = False
            self._shutdown()

    def _shutdown(self) -> None:
        """关闭应用"""
        self._logger.info("正在关闭 ImageForge...")

        try:
            self._config.save()
            self._logger.info("配置已保存")
        except Exception as e:
            self._logger.error(f"保存配置失败: {str(e)}")

        self.about_to_quit.emit()
        self._logger.info("ImageForge 已关闭")

    def quit(self) -> None:
        """退出应用"""
        app = QApplication.instance()
        if app:
            app.quit()

    def get_config(self):
        """获取配置管理器"""
        return self._config

    def is_running(self) -> bool:
        """检查应用是否正在运行"""
        return self._is_running
