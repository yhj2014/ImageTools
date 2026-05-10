import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from PySide6.QtCore import QObject, Signal


class LogEmitter(QObject):
    log_signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger("ImageProcessor")
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)

        self._log_file: Optional[Path] = None

    def set_log_file(self, log_dir: Path) -> None:
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log_file = log_dir / f"image_processor_{timestamp}.log"

        file_handler = logging.FileHandler(self._log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)

    def get_log_file(self) -> Optional[Path]:
        return self._log_file

    def debug(self, message: str) -> None:
        self._logger.debug(message)
        self.log_signal.emit("DEBUG", message)

    def info(self, message: str) -> None:
        self._logger.info(message)
        self.log_signal.emit("INFO", message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)
        self.log_signal.emit("WARNING", message)

    def error(self, message: str) -> None:
        self._logger.error(message)
        self.log_signal.emit("ERROR", message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)
        self.log_signal.emit("CRITICAL", message)


logger = LogEmitter()
