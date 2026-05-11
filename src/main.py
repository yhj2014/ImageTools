"""ImageForge - 专业图像处理工具
主程序入口
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

from utils.logger import get_logger
from utils.config import get_config
from ui.main_window import MainWindow


def setup_environment() -> None:
    """设置运行环境"""
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


def check_dependencies() -> bool:
    """检查依赖是否满足

    Returns:
        是否满足所有依赖
    """
    missing = []

    try:
        from PySide6.QtCore import __version__ as pyside_version
    except ImportError:
        missing.append("PySide6")

    try:
        from PIL import __version__ as pil_version
    except ImportError:
        missing.append("Pillow")

    if missing:
        print(f"错误: 缺少以下依赖: {', '.join(missing)}")
        print("请运行: uv install")
        return False

    return True


def main() -> int:
    """主函数

    Returns:
        退出码
    """
    setup_environment()

    logger = get_logger()
    logger.info("=" * 60)
    logger.info("ImageForge 启动中...")
    logger.info("=" * 60)

    if not check_dependencies():
        return 1

    config = get_config()
    logger.info(f"加载配置: 主题={config.get('appearance.theme', 'light')}")

    app = QApplication(sys.argv)
    app.setApplicationName("ImageForge")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("ImageForge")
    app.setOrganizationDomain("imageforge.app")

    from ui.styles import DEFAULT_STYLESHEET
    app.setStyleSheet(DEFAULT_STYLESHEET)

    try:
        window = MainWindow()
        window.show()

        logger.info("主窗口已显示")
        logger.info("ImageForge 启动完成")

        return app.exec()

    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        QMessageBox.critical(
            None,
            "启动错误",
            f"程序启动失败:\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
