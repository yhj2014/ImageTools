"""预览组件 - 图像预览显示"""
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal, QSize, QRect
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QDragEnterEvent, QDropEvent, QResizeEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QSizePolicy, QFrame, QApplication
)

from utils.helpers import ImageHelper


class PreviewWidget(QWidget):
    """图像预览组件

    提供图像预览功能，支持：
    - 缩放适应窗口
    - 原始尺寸显示
    - 拖拽加载图片
    - 加载动画效果
    """
    file_dropped = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_file: Optional[str] = None
        self._pixmap: Optional[QPixmap] = None
        self._zoom_factor: float = 1.0
        self._fit_mode: str = "fit_window"
        self._is_loading: bool = False

        self._init_ui()
        self._init_drag_drop()

    def _init_ui(self) -> None:
        """初始化UI组件"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._scroll_area.setBackgroundRole(QWidget.backgroundRole())
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self._image_label.setMinimumSize(1, 1)

        self._scroll_area.setWidget(self._image_label)
        layout.addWidget(self._scroll_area)

        self._placeholder_label = QLabel("拖拽图片到这里或点击加载")
        self._placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder_label.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 14px;
                padding: 40px;
            }
        """)
        layout.addWidget(self._placeholder_label)

        self._info_label = QLabel()
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._info_label.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 12px;
                padding: 4px;
            }
        """)
        layout.addWidget(self._info_label)

        self._set_placeholder_visible(True)

    def _init_drag_drop(self) -> None:
        """初始化拖拽支持"""
        self.setAcceptDrops(True)

    def _set_placeholder_visible(self, visible: bool) -> None:
        """设置占位符可见性"""
        self._placeholder_label.setVisible(visible)

    def _show_loading(self) -> None:
        """显示加载中状态"""
        self._is_loading = True
        self._placeholder_label.setText("加载中...")
        self._placeholder_label.setVisible(True)
        QApplication.processEvents()

    def _hide_loading(self) -> None:
        """隐藏加载状态"""
        self._is_loading = False

    def load_image(self, file_path: str) -> bool:
        """加载图像文件

        Args:
            file_path: 图像文件路径

        Returns:
            是否加载成功
        """
        if not Path(file_path).exists():
            return False

        self._show_loading()
        self._current_file = file_path

        try:
            self._pixmap = QPixmap(file_path)
            if self._pixmap.isNull():
                return False

            self._update_display()
            self._set_placeholder_visible(False)

            info = ImageHelper.get_info(file_path)
            self._info_label.setText(
                f"{info['width']} × {info['height']} | "
                f"{Path(file_path).name}"
            )

            self._hide_loading()
            return True

        except Exception as e:
            self._hide_loading()
            self._placeholder_label.setText(f"加载失败: {str(e)}")
            return False

    def _update_display(self) -> None:
        """更新图像显示"""
        if self._pixmap is None:
            return

        if self._fit_mode == "fit_window":
            scaled_pixmap = self._pixmap.scaled(
                self._scroll_area.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        elif self._fit_mode == "original":
            scaled_pixmap = self._pixmap
        else:
            new_size = self._pixmap.size() * self._zoom_factor
            scaled_pixmap = self._pixmap.scaled(
                new_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self._image_label.setPixmap(scaled_pixmap)

    def set_fit_mode(self, mode: str) -> None:
        """设置适应模式

        Args:
            mode: "fit_window" | "original" | "custom"
        """
        self._fit_mode = mode
        self._update_display()

    def set_zoom_factor(self, factor: float) -> None:
        """设置缩放因子

        Args:
            factor: 缩放因子 (0.1 - 10.0)
        """
        self._zoom_factor = max(0.1, min(10.0, factor))
        self._fit_mode = "custom"
        self._update_display()

    def zoom_in(self) -> None:
        """放大图像"""
        self.set_zoom_factor(self._zoom_factor * 1.2)

    def zoom_out(self) -> None:
        """缩小图像"""
        self.set_zoom_factor(self._zoom_factor / 1.2)

    def reset_zoom(self) -> None:
        """重置缩放为适应窗口"""
        self.set_fit_mode("fit_window")

    def get_current_file(self) -> Optional[str]:
        """获取当前预览的文件路径"""
        return self._current_file

    def clear(self) -> None:
        """清除预览"""
        self._current_file = None
        self._pixmap = None
        self._image_label.clear()
        self._info_label.clear()
        self._set_placeholder_visible(True)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and ImageHelper.is_image_file(urls[0].toLocalFile()):
                event.acceptProposedAction()
                self.setStyleSheet("border: 2px dashed #2196F3;")
                return
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event) -> None:
        """拖拽离开事件"""
        self.setStyleSheet("")
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        """放下事件"""
        self.setStyleSheet("")
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if ImageHelper.is_image_file(file_path):
                    self.load_image(file_path)
                    self.file_dropped.emit(file_path)
                    break
        super().dropEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """窗口大小改变事件"""
        super().resizeEvent(event)
        if self._fit_mode == "fit_window":
            self._update_display()
