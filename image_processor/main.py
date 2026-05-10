import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from utils.logger import logger


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("批量图像处理工具")
    app.setOrganizationName("ImageProcessor")
    app.setOrganizationDomain("imageprocessor.local")
    app.setStyle("Fusion")

    logger.info("=" * 50)
    logger.info("批量图像处理工具启动")
    logger.info("=" * 50)

    log_dir = Path.home() / ".image_processor" / "logs"
    logger.set_log_file(log_dir)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
