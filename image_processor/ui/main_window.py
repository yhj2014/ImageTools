import os
from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QIcon, QAction, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QFileDialog,
    QComboBox, QLineEdit, QProgressBar, QTextEdit,
    QGroupBox, QApplication, QMessageBox, QSlider,
    QStyle, QFrame
)

from core.converter import OUTPUT_FORMATS, ImageConverter
from core.worker import ConversionWorker


class FileListWidget(QListWidget):
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if ImageConverter.is_image_file(file_path):
                files.append(file_path)
        if files:
            self.files_dropped.emit(files)


class MainWindow(QWidget):
    WINDOW_TITLE = "批量图像处理工具"
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self._file_list: List[str] = []
        self._worker_thread: Optional[QThread] = None
        self._conversion_worker: Optional[ConversionWorker] = None
        self._output_dir = str(Path.home() / "图像转换输出")
        self._output_format = "webp"
        self._quality = 85
        self._max_workers = 4

        self._init_ui()
        self._init_worker()

    def _init_ui(self) -> None:
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)
        self.setStyleSheet(self._get_stylesheet())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        title_label = QLabel("📷 批量图像格式转换")
        title_label.setObjectName("TitleLabel")
        main_layout.addWidget(title_label)

        file_group = self._create_file_group()
        main_layout.addWidget(file_group, 1)

        option_group = self._create_option_group()
        main_layout.addWidget(option_group)

        action_group = self._create_action_group()
        main_layout.addWidget(action_group)

        log_group = self._create_log_group()
        main_layout.addWidget(log_group, 1)

    def _get_stylesheet(self) -> str:
        return """
            QWidget {
                background-color: #FAFAFA;
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
                font-size: 14px;
                color: #212121;
            }
            #TitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2196F3;
                padding: 8px 0;
            }
            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                margin-top: 8px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #2196F3;
            }
            QListWidget {
                background-color: #FFFFFF;
                border: 2px dashed #BDBDBD;
                border-radius: 6px;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QPushButton#secondary {
                background-color: #757575;
            }
            QPushButton#secondary:hover {
                background-color: #616161;
            }
            QPushButton#danger {
                background-color: #F44336;
            }
            QPushButton#danger:hover {
                background-color: #D32F2F;
            }
            QPushButton#success {
                background-color: #4CAF50;
            }
            QPushButton#success:hover {
                background-color: #388E3C;
            }
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 8px 12px;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #757575;
                margin-right: 8px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 8px 12px;
            }
            QLineEdit:hover {
                border-color: #2196F3;
            }
            QProgressBar {
                background-color: #E0E0E0;
                border: none;
                border-radius: 4px;
                text-align: center;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 8px;
                font-family: "Consolas", "Microsoft YaHei", monospace;
                font-size: 12px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #BDBDBD;
                height: 6px;
                background: #E0E0E0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #1976D2;
            }
            QLabel {
                color: #424242;
            }
        """

    def _create_file_group(self) -> QGroupBox:
        group = QGroupBox("📁 文件列表")

        layout = QVBoxLayout(group)

        self._file_list_widget = FileListWidget()
        self._file_list_widget.files_dropped.connect(self._on_files_dropped)
        layout.addWidget(self._file_list_widget, 1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        add_btn = QPushButton("➕ 添加文件")
        add_btn.clicked.connect(self._on_add_files)
        btn_layout.addWidget(add_btn)

        add_folder_btn = QPushButton("📂 添加文件夹")
        add_folder_btn.clicked.connect(self._on_add_folder)
        btn_layout.addWidget(add_folder_btn)

        btn_layout.addStretch()

        clear_btn = QPushButton("🗑️ 清空列表")
        clear_btn.setObjectName("danger")
        clear_btn.clicked.connect(self._on_clear_list)
        btn_layout.addWidget(clear_btn)

        remove_btn = QPushButton("❌ 删除选中")
        remove_btn.setObjectName("secondary")
        remove_btn.clicked.connect(self._on_remove_selected)
        btn_layout.addWidget(remove_btn)

        layout.addLayout(btn_layout)

        return group

    def _create_option_group(self) -> QGroupBox:
        group = QGroupBox("⚙️ 输出设置")

        layout = QHBoxLayout(group)
        layout.setSpacing(16)

        format_layout = QVBoxLayout()
        format_layout.addWidget(QLabel("输出格式:"))
        self._format_combo = QComboBox()
        self._format_combo.addItems([fmt.upper() for fmt in OUTPUT_FORMATS])
        self._format_combo.setCurrentText(self._output_format.upper())
        self._format_combo.currentTextChanged.connect(self._on_format_changed)
        format_layout.addWidget(self._format_combo)
        layout.addLayout(format_layout)

        quality_layout = QVBoxLayout()
        quality_layout.addWidget(QLabel("图像质量:"))
        quality_slider_layout = QHBoxLayout()
        self._quality_slider = QSlider(Qt.Orientation.Horizontal)
        self._quality_slider.setMinimum(1)
        self._quality_slider.setMaximum(100)
        self._quality_slider.setValue(self._quality)
        self._quality_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._quality_slider.setTickInterval(10)
        self._quality_slider.valueChanged.connect(self._on_quality_changed)
        quality_slider_layout.addWidget(self._quality_slider)
        self._quality_label = QLabel(f"{self._quality}%")
        self._quality_label.setFixedWidth(40)
        quality_slider_layout.addWidget(self._quality_label)
        quality_layout.addLayout(quality_slider_layout)
        layout.addLayout(quality_layout)

        thread_layout = QVBoxLayout()
        thread_layout.addWidget(QLabel("并发线程:"))
        thread_value_layout = QHBoxLayout()
        self._thread_slider = QSlider(Qt.Orientation.Horizontal)
        self._thread_slider.setMinimum(1)
        self._thread_slider.setMaximum(8)
        self._thread_slider.setValue(self._max_workers)
        self._thread_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._thread_slider.setTickInterval(1)
        self._thread_slider.valueChanged.connect(self._on_thread_changed)
        thread_value_layout.addWidget(self._thread_slider)
        self._thread_label = QLabel(str(self._max_workers))
        self._thread_label.setFixedWidth(20)
        thread_value_layout.addWidget(self._thread_label)
        thread_layout.addLayout(thread_value_layout)
        layout.addLayout(thread_layout)

        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        output_dir_layout = QHBoxLayout()
        self._output_dir_edit = QLineEdit(self._output_dir)
        self._output_dir_edit.setReadOnly(True)
        output_dir_layout.addWidget(self._output_dir_edit)
        browse_btn = QPushButton("浏览")
        browse_btn.setObjectName("secondary")
        browse_btn.setFixedWidth(60)
        browse_btn.clicked.connect(self._on_browse_output_dir)
        output_dir_layout.addWidget(browse_btn)
        output_layout.addLayout(output_dir_layout)
        layout.addLayout(output_layout)

        layout.addStretch()

        return group

    def _create_action_group(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 8, 0, 8)

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        layout.addWidget(self._progress_bar)

        btn_layout = QHBoxLayout()

        self._start_btn = QPushButton("🚀 开始转换")
        self._start_btn.setObjectName("success")
        self._start_btn.clicked.connect(self._on_start_conversion)
        btn_layout.addWidget(self._start_btn)

        self._cancel_btn = QPushButton("⏹ 取消")
        self._cancel_btn.setObjectName("danger")
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.clicked.connect(self._on_cancel_conversion)
        btn_layout.addWidget(self._cancel_btn)

        self._status_label = QLabel("就绪")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("color: #757575; font-weight: bold;")
        btn_layout.addWidget(self._status_label)

        btn_layout.addStretch()

        self._file_count_label = QLabel("共 0 个文件")
        self._file_count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        btn_layout.addWidget(self._file_count_label)

        layout.addLayout(btn_layout)

        return widget

    def _create_log_group(self) -> QGroupBox:
        group = QGroupBox("📋 转换日志")

        layout = QVBoxLayout(group)

        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumHeight(150)
        layout.addWidget(self._log_text, 1)

        return group

    def _init_worker(self) -> None:
        self._worker_thread = QThread()
        self._conversion_worker = ConversionWorker(
            max_workers=self._max_workers,
            quality=self._quality
        )
        self._conversion_worker.moveToThread(self._worker_thread)

        self._conversion_worker.progress_changed.connect(self._on_progress_changed)
        self._conversion_worker.log_message.connect(self._on_log_message)
        self._conversion_worker.conversion_complete.connect(self._on_conversion_complete)
        self._conversion_worker.single_conversion_done.connect(self._on_single_conversion_done)

        self._worker_thread.start()

    def _on_add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片文件",
            str(Path.home()),
            "图片文件 (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif *.gif *.tga *.psd);;所有文件 (*.*)"
        )
        if files:
            self._add_files(files)

    def _on_add_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            str(Path.home())
        )
        if folder:
            self._add_files_from_folder(folder)

    def _add_files(self, files: List[str]) -> None:
        for file_path in files:
            if file_path not in self._file_list and ImageConverter.is_image_file(file_path):
                self._file_list.append(file_path)
                self._file_list_widget.addItem(Path(file_path).name + " ↗")

        self._update_file_count()

    def _add_files_from_folder(self, folder: str) -> None:
        folder_path = Path(folder)
        image_files = []
        for ext in ImageConverter.get_input_formats():
            image_files.extend(folder_path.glob(f"*.{ext}"))
            image_files.extend(folder_path.glob(f"*.{ext.upper()}"))

        files = [str(f) for f in image_files]
        if files:
            self._add_files(files)
            self._append_log("INFO", f"从文件夹添加了 {len(files)} 个文件")
        else:
            self._append_log("WARNING", "文件夹中没有找到图片文件")

    def _on_files_dropped(self, files: List[str]) -> None:
        self._add_files(files)
        self._append_log("INFO", f"拖拽添加了 {len(files)} 个文件")

    def _on_clear_list(self) -> None:
        self._file_list.clear()
        self._file_list_widget.clear()
        self._update_file_count()
        self._append_log("INFO", "文件列表已清空")

    def _on_remove_selected(self) -> None:
        selected_items = self._file_list_widget.selectedItems()
        if not selected_items:
            return

        indices_to_remove = []
        for item in selected_items:
            row = self._file_list_widget.row(item)
            indices_to_remove.append(row)

        for row in sorted(indices_to_remove, reverse=True):
            self._file_list_widget.takeItem(row)
            if row < len(self._file_list):
                self._file_list.pop(row)

        self._update_file_count()

    def _on_format_changed(self, format_text: str) -> None:
        self._output_format = format_text.lower()

    def _on_quality_changed(self, value: int) -> None:
        self._quality = value
        self._quality_label.setText(f"{value}%")
        if self._conversion_worker:
            self._conversion_worker.set_quality(value)

    def _on_thread_changed(self, value: int) -> None:
        self._max_workers = value
        self._thread_label.setText(str(value))
        if self._conversion_worker:
            self._conversion_worker.set_max_workers(value)

    def _on_browse_output_dir(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            self._output_dir
        )
        if folder:
            self._output_dir = folder
            self._output_dir_edit.setText(folder)

    def _on_start_conversion(self) -> None:
        if not self._file_list:
            QMessageBox.warning(self, "提示", "请先添加要转换的图片文件")
            return

        if not self._conversion_worker:
            QMessageBox.critical(self, "错误", "转换引擎未初始化")
            return

        self._start_btn.setEnabled(False)
        self._cancel_btn.setEnabled(True)
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        self._progress_bar.setMaximum(len(self._file_list))
        self._status_label.setText("转换中...")
        self._status_label.setStyleSheet("color: #2196F3; font-weight: bold;")

        self._append_log("INFO", "=" * 40)
        self._append_log("INFO", f"开始批量转换: {len(self._file_list)} 个文件")
        self._append_log("INFO", f"输出格式: {self._output_format.upper()}, 质量: {self._quality}%")
        self._append_log("INFO", f"输出目录: {self._output_dir}")
        self._append_log("INFO", "=" * 40)

        from functools import partial
        QApplication.instance().processEvents()

        self._conversion_worker.process_files(
            self._file_list.copy(),
            self._output_format,
            self._output_dir
        )

    def _on_cancel_conversion(self) -> None:
        if self._conversion_worker and self._conversion_worker.is_running():
            self._conversion_worker.cancel()
            self._append_log("WARNING", "正在取消转换...")
            self._status_label.setText("取消中...")
            self._status_label.setStyleSheet("color: #FF9800; font-weight: bold;")

    def _on_progress_changed(self, current: int, total: int, filename: str) -> None:
        self._progress_bar.setValue(current)
        remaining = total - current
        self._status_label.setText(f"正在转换: {filename} ({current}/{total})")

    def _on_log_message(self, level: str, message: str) -> None:
        self._append_log(level, message)

    def _on_single_conversion_done(self, success: bool, file_path: str, message: str) -> None:
        if not success:
            self._log_text.setTextColor(Qt.GlobalColor.red)
            self._log_text.append(f"[ERROR] {message}")
            self._log_text.setTextColor(Qt.GlobalColor.black)

    def _on_conversion_complete(self, success: bool, success_count: int, failed_count: int) -> None:
        self._start_btn.setEnabled(True)
        self._cancel_btn.setEnabled(False)
        self._progress_bar.setVisible(False)
        self._status_label.setText("转换完成")
        self._status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        self._append_log("INFO", "=" * 40)
        self._append_log("INFO", f"转换完成: 成功 {success_count}, 失败 {failed_count}")
        self._append_log("INFO", f"输出目录: {self._output_dir}")
        self._append_log("INFO", "=" * 40)

        if success_count > 0:
            reply = QMessageBox.information(
                self,
                "转换完成",
                f"转换完成！\n成功: {success_count} 个\n失败: {failed_count} 个\n\n是否打开输出目录？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._open_output_dir()

    def _append_log(self, level: str, message: str) -> None:
        color_map = {
            "DEBUG": "#9E9E9E",
            "INFO": "#212121",
            "WARNING": "#FF9800",
            "ERROR": "#F44336",
            "CRITICAL": "#D32F2F"
        }
        color = color_map.get(level, "#212121")
        self._log_text.setTextColor(Qt.GlobalColor(color) if level in ["ERROR", "WARNING", "CRITICAL"] else Qt.GlobalColor.black)
        self._log_text.append(f"[{level}] {message}")
        self._log_text.setTextColor(Qt.GlobalColor.black)

    def _update_file_count(self) -> None:
        count = len(self._file_list)
        self._file_count_label.setText(f"共 {count} 个文件")

    def _open_output_dir(self) -> None:
        try:
            Path(self._output_dir).mkdir(parents=True, exist_ok=True)
            os.startfile(self._output_dir) if os.name == 'nt' else None
        except Exception as e:
            self._append_log("ERROR", f"无法打开目录: {e}")

    def closeEvent(self, event):
        if self._conversion_worker and self._conversion_worker.is_running():
            reply = QMessageBox.question(
                self,
                "确认退出",
                "正在执行转换任务，是否确认退出？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

            self._conversion_worker.cancel()

        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait(2000)

        event.accept()
