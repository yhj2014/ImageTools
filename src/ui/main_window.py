"""ImageForge 主窗口"""
from pathlib import Path
from typing import List, Optional, Dict, Any

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QKeySequence, QCloseEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QListWidget, QComboBox,
    QProgressBar, QTextEdit, QGroupBox, QFrame,
    QMenuBar, QMenu, QStatusBar, QToolBar,
    QMessageBox, QFileDialog, QApplication,
    QSizePolicy, QSplitter, QScrollArea, QStackedWidget
)

from ui.widgets import (
    FileListWidget, PreviewWidget, FeatureTabWidget,
    ValueSlider
)
from ui.styles import Theme, ThemeManager, DEFAULT_STYLESHEET
from core.worker import TaskWorker, Task
from core.converter import ImageConverter
from core.ffmpeg_manager import FFmpegManager
from utils.logger import get_logger
from utils.config import get_config


class MainWindow(QWidget):
    """ImageForge 主窗口"""

    WINDOW_TITLE = "ImageForge - 专业图像处理工具"
    WINDOW_MIN_SIZE = QSize(1000, 700)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._logger = get_logger()
        self._config = get_config()
        self._file_list: List[str] = []
        self._output_dir = str(Path.home() / "ImageForge_Output")

        self._ffmpeg_manager = FFmpegManager()
        self._converter = ImageConverter()
        self._worker: Optional[TaskWorker] = None

        self._current_feature = "convert"
        self._feature_settings: Dict[str, Any] = {}

        self._init_ui()
        self._init_ffmpeg()
        self._init_worker()

    def _init_ui(self) -> None:
        """初始化UI"""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.WINDOW_MIN_SIZE)
        self.resize(1200, 800)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._sidebar = self._create_sidebar()
        main_layout.addWidget(self._sidebar)

        self._main_content = self._create_main_content()
        main_layout.addWidget(self._main_content, 1)

        self._status_bar = self._create_status_bar()
        main_layout.addWidget(self._status_bar)

        self._update_file_count()

    def _create_sidebar(self) -> QWidget:
        """创建侧边栏"""
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame#Sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(8, 16, 8, 8)
        layout.setSpacing(4)

        logo_label = QLabel("🖼️ ImageForge")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                padding: 8px;
            }
        """)
        layout.addWidget(logo_label)

        layout.addSpacing(16)

        features = [
            ("📁 文件", "file"),
            ("🔄 格式转换", "convert"),
            ("✂️ 裁剪", "crop"),
            ("💧 水印", "watermark"),
            ("📐 缩放", "resize"),
            ("🔃 旋转", "rotate"),
            ("🎨 滤镜", "filter"),
            ("🎬 GIF", "gif"),
            ("📝 重命名", "rename"),
            ("📄 PDF", "pdf"),
        ]

        self._feature_buttons = {}

        for name, feature_id in features:
            btn = QPushButton(name)
            btn.setObjectName("SidebarButton")
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton#SidebarButton {
                    text-align: left;
                    padding: 10px 16px;
                    border: none;
                    border-radius: 6px;
                    background-color: transparent;
                    color: #424242;
                }
                QPushButton#SidebarButton:hover {
                    background-color: #E3F2FD;
                }
                QPushButton#SidebarButton:checked {
                    background-color: #2196F3;
                    color: white;
                }
            """)
            btn.clicked.connect(
                lambda checked, fid=feature_id: self._on_feature_changed(fid)
            )
            self._feature_buttons[feature_id] = btn
            layout.addWidget(btn)

        layout.addStretch()

        settings_btn = QPushButton("⚙️ 设置")
        settings_btn.setObjectName("SidebarButton")
        settings_btn.setStyleSheet("""
            QPushButton#SidebarButton {
                text-align: left;
                padding: 10px 16px;
                border: none;
                border-radius: 6px;
                background-color: transparent;
                color: #424242;
            }
            QPushButton#SidebarButton:hover {
                background-color: #E3F2FD;
            }
        """)
        layout.addWidget(settings_btn)

        return sidebar

    def _create_main_content(self) -> QWidget:
        """创建主内容区"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([400, 600])

        layout.addWidget(splitter, 1)

        bottom_panel = self._create_bottom_panel()
        layout.addWidget(bottom_panel)

        return content

    def _create_toolbar(self) -> QWidget:
        """创建工具栏"""
        toolbar = QFrame()
        toolbar.setObjectName("Toolbar")
        toolbar.setStyleSheet("""
            QFrame#Toolbar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(0, 0, 0, 0)

        add_file_btn = QPushButton("📂 添加文件")
        add_file_btn.clicked.connect(self._on_add_files)
        layout.addWidget(add_file_btn)

        add_folder_btn = QPushButton("📁 添加文件夹")
        add_folder_btn.clicked.connect(self._on_add_folder)
        layout.addWidget(add_folder_btn)

        layout.addSpacing(16)

        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self._on_clear_files)
        layout.addWidget(clear_btn)

        layout.addStretch()

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self._output_dir_edit = QPushButton("选择...")
        self._output_dir_edit.clicked.connect(self._on_select_output_dir)
        output_layout.addWidget(self._output_dir_edit)
        layout.addLayout(output_layout)

        return toolbar

    def _create_left_panel(self) -> QWidget:
        """创建左侧面板 - 文件列表"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)

        title = QLabel("📋 文件列表")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self._file_list_widget = FileListWidget()
        self._file_list_widget.files_dropped.connect(self._on_files_dropped)
        self._file_list_widget.files_removed.connect(self._on_files_removed)
        layout.addWidget(self._file_list_widget, 1)

        self._file_count_label = QLabel("共 0 个文件")
        self._file_count_label.setStyleSheet("color: #757575;")
        layout.addWidget(self._file_count_label)

        return panel

    def _create_right_panel(self) -> QWidget:
        """创建右侧面板 - 功能设置"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)

        title = QLabel("⚙️ 功能设置")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self._feature_tabs = FeatureTabWidget()
        layout.addWidget(self._feature_tabs, 1)

        self._action_layout = self._create_action_buttons()
        layout.addWidget(self._action_layout)

        return panel

    def _create_bottom_panel(self) -> QWidget:
        """创建底部面板 - 进度和日志"""
        panel = QFrame()
        panel.setObjectName("BottomPanel")
        panel.setStyleSheet("""
            QFrame#BottomPanel {
                background-color: #FFFFFF;
                border-top: 1px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 8, 16, 8)

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        self._progress_bar.setStyleSheet("""
            QProgressBar {
                height: 20px;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        layout.addWidget(self._progress_bar)

        status_layout = QHBoxLayout()

        self._status_label = QLabel("就绪")
        self._status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        status_layout.addWidget(self._status_label)

        status_layout.addStretch()

        self._log_text = QTextEdit()
        self._log_text.setMaximumHeight(100)
        self._log_text.setReadOnly(True)
        self._log_text.setStyleSheet("""
            QTextEdit {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                font-family: Consolas, monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self._log_text)

        return panel

    def _create_action_buttons(self) -> QWidget:
        """创建操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 8, 0, 0)

        self._start_btn = QPushButton("🚀 开始处理")
        self._start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 32px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self._start_btn.clicked.connect(self._on_start_processing)
        layout.addWidget(self._start_btn)

        self._cancel_btn = QPushButton("⏹ 取消")
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self._cancel_btn.clicked.connect(self._on_cancel_processing)
        layout.addWidget(self._cancel_btn)

        layout.addStretch()

        return widget

    def _create_status_bar(self) -> QWidget:
        """创建状态栏"""
        status_bar = QFrame()
        status_bar.setObjectName("StatusBar")
        status_bar.setStyleSheet("""
            QFrame#StatusBar {
                background-color: #F5F5F5;
                border-top: 1px solid #E0E0E0;
                padding: 4px 16px;
            }
        """)

        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(0, 0, 0, 0)

        self._ffmpeg_status = QLabel("FFmpeg: 检测中...")
        self._ffmpeg_status.setStyleSheet("color: #757575;")
        layout.addWidget(self._ffmpeg_status)

        layout.addStretch()

        self._version_label = QLabel("v2.0.0")
        self._version_label.setStyleSheet("color: #9E9E9E;")
        layout.addWidget(self._version_label)

        return status_bar

    def _init_ffmpeg(self) -> None:
        """初始化 FFmpeg"""
        success, message = self._ffmpeg_manager.download_if_needed()
        if success:
            version = self._ffmpeg_manager.get_version()
            self._ffmpeg_status.setText(f"FFmpeg: ✓ {version}")
            self._ffmpeg_status.setStyleSheet("color: #4CAF50;")
            self._logger.info(f"FFmpeg 就绪: {version}")
        else:
            self._ffmpeg_status.setText(f"FFmpeg: ✗ {message}")
            self._ffmpeg_status.setStyleSheet("color: #F44336;")
            self._logger.warning(f"FFmpeg 不可用: {message}")

    def _init_worker(self) -> None:
        """初始化工作器"""
        self._worker = TaskWorker(max_workers=4)
        self._worker.progress.connect(self._on_progress)
        self._worker.log.connect(self._on_log)
        self._worker.finished.connect(self._on_finished)

    def _on_feature_changed(self, feature_id: str) -> None:
        """功能切换"""
        self._current_feature = feature_id

        for fid, btn in self._feature_buttons.items():
            btn.setChecked(fid == feature_id)

        self._logger.info(f"切换到功能: {feature_id}")

    def _on_add_files(self) -> None:
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图片文件",
            str(Path.home()),
            "图片文件 (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif *.gif *.tga);;所有文件 (*.*)"
        )

        if files:
            self._add_files(files)

    def _on_add_folder(self) -> None:
        """添加文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            str(Path.home())
        )

        if folder:
            from core.converter import ImageConverter
            folder_path = Path(folder)
            image_files = []

            for ext in ImageConverter.get_input_formats():
                image_files.extend(folder_path.glob(f"*.{ext}"))
                image_files.extend(folder_path.glob(f"*.{ext.upper()}"))

            files = [str(f) for f in image_files]
            if files:
                self._add_files(files)
                self._log("INFO", f"从文件夹添加了 {len(files)} 个文件")

    def _add_files(self, files: List[str]) -> None:
        """添加文件到列表"""
        for file_path in files:
            if file_path not in self._file_list:
                self._file_list.append(file_path)
                self._file_list_widget.add_files([file_path])

        self._update_file_count()

    def _on_files_dropped(self, files: List[str]) -> None:
        """文件拖放"""
        self._add_files(files)
        self._log("INFO", f"拖拽添加了 {len(files)} 个文件")

    def _on_files_removed(self, files: List[str]) -> None:
        """文件移除"""
        for file_path in files:
            if file_path in self._file_list:
                self._file_list.remove(file_path)

        self._update_file_count()

    def _on_clear_files(self) -> None:
        """清空文件列表"""
        self._file_list.clear()
        self._file_list_widget.clear_list()
        self._update_file_count()
        self._log("INFO", "文件列表已清空")

    def _on_select_output_dir(self) -> None:
        """选择输出目录"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            self._output_dir
        )

        if folder:
            self._output_dir = folder
            self._output_dir_edit.setText(folder)

    def _update_file_count(self) -> None:
        """更新文件计数"""
        count = len(self._file_list)
        self._file_count_label.setText(f"共 {count} 个文件")

    def _on_start_processing(self) -> None:
        """开始处理"""
        if not self._file_list:
            QMessageBox.warning(self, "提示", "请先添加要处理的图片文件")
            return

        if not self._ffmpeg_manager.is_available():
            QMessageBox.warning(
                self,
                "FFmpeg 不可用",
                "FFmpeg 未正确安装，部分功能可能无法使用。"
            )

        settings = self._feature_tabs.get_current_settings()

        self._start_btn.setEnabled(False)
        self._cancel_btn.setEnabled(True)
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        self._progress_bar.setMaximum(len(self._file_list))

        self._log("INFO", "=" * 40)
        self._log("INFO", f"开始批量处理: {len(self._file_list)} 个文件")
        self._log("INFO", f"输出目录: {self._output_dir}")
        self._log("INFO", "=" * 40)

        tasks = []
        for file_path in self._file_list:
            task = Task(
                input_path=file_path,
                output_dir=self._output_dir,
                feature=self._current_feature,
                settings=settings
            )
            tasks.append(task)

        self._worker.start(tasks)

    def _on_cancel_processing(self) -> None:
        """取消处理"""
        if self._worker:
            self._worker.cancel()
            self._log("WARNING", "正在取消处理...")

    def _on_progress(self, current: int, total: int, message: str) -> None:
        """进度更新"""
        self._progress_bar.setValue(current)
        self._status_label.setText(f"处理中: {message} ({current}/{total})")

    def _on_log(self, level: str, message: str) -> None:
        """日志更新"""
        self._log(level, message)

    def _on_finished(self, success: bool, count: int, failed: int) -> None:
        """处理完成"""
        self._start_btn.setEnabled(True)
        self._cancel_btn.setEnabled(False)
        self._progress_bar.setVisible(False)
        self._status_label.setText("处理完成")
        self._status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        self._log("INFO", "=" * 40)
        self._log("INFO", f"处理完成: 成功 {count}, 失败 {failed}")
        self._log("INFO", "=" * 40)

        if count > 0:
            reply = QMessageBox.information(
                self,
                "处理完成",
                f"处理完成！\n成功: {count} 个\n失败: {failed} 个\n\n是否打开输出目录？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self._open_output_dir()

    def _log(self, level: str, message: str) -> None:
        """添加日志"""
        self._log_text.append(f"[{level}] {message}")
        self._logger.info(message)

    def _open_output_dir(self) -> None:
        """打开输出目录"""
        import os
        try:
            Path(self._output_dir).mkdir(parents=True, exist_ok=True)
            if os.name == 'nt':
                os.startfile(self._output_dir)
            elif os.name == 'posix':
                import subprocess
                subprocess.run(['open', self._output_dir])
        except Exception as e:
            self._log("ERROR", f"无法打开目录: {e}")

    def closeEvent(self, event: QCloseEvent) -> None:
        """关闭窗口"""
        if self._worker and self._worker.is_running():
            reply = QMessageBox.question(
                self,
                "确认退出",
                "正在处理任务，是否确认退出？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

            self._worker.cancel()

        self._logger.info("ImageForge 关闭")
        event.accept()
