"""功能标签页 - 各功能模块的UI标签页"""
from typing import Optional, Dict, Any
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QSpinBox,
    QDoubleSpinBox, QLineEdit, QCheckBox, QGroupBox,
    QButtonGroup, QRadioButton, QSlider, QTextEdit,
    QListWidget, QListWidgetItem, QFileDialog,
    QTabWidget, QScrollArea, QFrame, QColorDialog,
    QFontComboBox, QSizePolicy, QProgressBar
)

from core.presets import PresetManager
from ui.widgets.slider import ValueSlider, PercentageSlider
from ui.widgets.preview import PreviewWidget


class BaseFeatureTab(QWidget):
    """功能标签页基类

    所有功能标签页的父类，提供通用功能
    """
    settings_changed = Signal(dict)
    preview_requested = Signal()

    def __init__(self, title: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._title = title
        self._settings: Dict[str, Any] = {}
        self._preset_manager = PresetManager()

    def get_title(self) -> str:
        """获取标签页标题"""
        return self._title

    def get_settings(self) -> Dict[str, Any]:
        """获取当前设置"""
        return self._settings.copy()

    def apply_settings(self, settings: Dict[str, Any]) -> None:
        """应用设置"""
        self._settings.update(settings)
        self._update_ui_from_settings()

    def _update_ui_from_settings(self) -> None:
        """从设置更新UI - 子类重写"""
        pass

    def _emit_settings_changed(self) -> None:
        """发送设置改变信号"""
        self.settings_changed.emit(self._settings)


class CropTab(BaseFeatureTab):
    """裁剪标签页

    提供图像裁剪功能：
    - 预设比例裁剪
    - 自定义尺寸裁剪
    - 位置选择
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("✂️ 裁剪", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        ratio_group = QGroupBox("裁剪比例")
        ratio_layout = QVBoxLayout(ratio_group)

        self._ratio_buttons = QButtonGroup()
        ratios = ["自由", "1:1", "4:3", "16:9", "3:2", "2:3", "9:16"]
        ratio_grid = QGridLayout()

        for i, ratio in enumerate(ratios):
            btn = QRadioButton(ratio)
            btn.toggled.connect(
                lambda checked, r=ratio: self._on_ratio_changed(r) if checked else None
            )
            self._ratio_buttons.addButton(btn, i)
            ratio_grid.addWidget(btn, i // 4, i % 4)

        ratio_layout.addLayout(ratio_grid)
        layout.addWidget(ratio_group)

        custom_group = QGroupBox("自定义尺寸")
        custom_layout = QHBoxLayout(custom_group)

        custom_layout.addWidget(QLabel("宽度:"))
        self._width_spin = QSpinBox()
        self._width_spin.setRange(1, 10000)
        self._width_spin.setValue(800)
        self._width_spin.valueChanged.connect(self._emit_settings_changed)
        custom_layout.addWidget(self._width_spin)

        custom_layout.addWidget(QLabel("高度:"))
        self._height_spin = QSpinBox()
        self._height_spin.setRange(1, 10000)
        self._height_spin.setValue(600)
        self._height_spin.valueChanged.connect(self._emit_settings_changed)
        custom_layout.addWidget(self._height_spin)

        layout.addWidget(custom_group)

        position_group = QGroupBox("裁剪位置")
        position_layout = QGridLayout(position_group)

        positions = ["左上", "中上", "右上", "左中", "居中", "右中", "左下", "中下", "右下"]
        self._position_buttons = QButtonGroup()

        for i, pos in enumerate(positions):
            btn = QRadioButton(pos)
            btn.setCheckable(True)
            self._position_buttons.addButton(btn, i)
            position_layout.addWidget(btn, i // 3, i % 3)

        self._position_buttons.button(4).setChecked(True)
        layout.addWidget(position_group)

        layout.addStretch()

    def _on_ratio_changed(self, ratio: str) -> None:
        """比例改变"""
        self._settings["ratio"] = ratio
        self._emit_settings_changed()

    def get_settings(self) -> Dict[str, Any]:
        """获取裁剪设置"""
        settings = super().get_settings()
        settings.update({
            "ratio": self._ratio_buttons.checkedButton().text() if self._ratio_buttons.checkedButton() else "自由",
            "width": self._width_spin.value(),
            "height": self._height_spin.value(),
            "position": self._position_buttons.checkedButton().text() if self._position_buttons.checkedButton() else "居中"
        })
        return settings


class WatermarkTab(BaseFeatureTab):
    """水印标签页

    提供水印功能：
    - 文字水印
    - 图片水印
    - 平铺模式
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("💧 水印", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        type_group = QGroupBox("水印类型")
        type_layout = QHBoxLayout(type_group)
        self._watermark_type_group = QButtonGroup()

        self._text_watermark_btn = QRadioButton("文字水印")
        self._image_watermark_btn = QRadioButton("图片水印")
        self._tiled_watermark_btn = QRadioButton("平铺水印")
        self._watermark_type_group.addButton(self._text_watermark_btn, 0)
        self._watermark_type_group.addButton(self._image_watermark_btn, 1)
        self._watermark_type_group.addButton(self._tiled_watermark_btn, 2)

        self._text_watermark_btn.setChecked(True)
        self._text_watermark_btn.toggled.connect(self._on_type_changed)

        type_layout.addWidget(self._text_watermark_btn)
        type_layout.addWidget(self._image_watermark_btn)
        type_layout.addWidget(self._tiled_watermark_btn)
        type_layout.addStretch()
        layout.addWidget(type_group)

        self._text_settings = self._create_text_settings()
        self._image_settings = self._create_image_settings()
        self._tiled_settings = self._create_tiled_settings()

        layout.addWidget(self._text_settings, 1)
        layout.addStretch()

    def _create_text_settings(self) -> QWidget:
        """创建文字水印设置面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        text_group = QGroupBox("文字设置")
        text_layout = QVBoxLayout(text_group)

        self._watermark_text = QLineEdit()
        self._watermark_text.setPlaceholderText("输入水印文字...")
        self._watermark_text.setText("© Copyright")
        self._watermark_text.textChanged.connect(self._emit_settings_changed)
        text_layout.addWidget(QLabel("水印文字:"))
        text_layout.addWidget(self._watermark_text)

        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体:"))
        self._font_combo = QFontComboBox()
        self._font_combo.setCurrentFont(QFont("Microsoft YaHei"))
        self._font_combo.currentFontChanged.connect(self._emit_settings_changed)
        font_layout.addWidget(self._font_combo)
        font_layout.addWidget(QLabel("字号:"))
        self._font_size = QSpinBox()
        self._font_size.setRange(8, 200)
        self._font_size.setValue(24)
        self._font_size.valueChanged.connect(self._emit_settings_changed)
        font_layout.addWidget(self._font_size)
        text_layout.addLayout(font_layout)

        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("颜色:"))
        self._color_btn = QPushButton("选择颜色")
        self._color_btn.setFixedWidth(100)
        self._color_btn.clicked.connect(self._select_color)
        color_layout.addWidget(self._color_btn)
        color_layout.addWidget(QLabel("透明度:"))
        self._opacity_slider = PercentageSlider("透明度:", 80)
        self._opacity_slider.value_changed.connect(self._emit_settings_changed)
        color_layout.addWidget(self._opacity_slider)
        text_layout.addLayout(color_layout)

        rotate_layout = QHBoxLayout()
        rotate_layout.addWidget(QLabel("旋转角度:"))
        self._rotate_slider = ValueSlider(min_value=-180, max_value=180, value=0, label="")
        self._rotate_slider.value_changed.connect(self._emit_settings_changed)
        rotate_layout.addWidget(self._rotate_slider)
        text_layout.addLayout(rotate_layout)

        layout.addWidget(text_group)

        pos_group = QGroupBox("位置")
        pos_layout = QGridLayout(pos_group)

        positions = ["左上", "中上", "右上", "左中", "居中", "右中", "左下", "中下", "右下"]
        self._position_group = QButtonGroup()

        for i, pos in enumerate(positions):
            btn = QRadioButton(pos)
            self._position_group.addButton(btn, i)
            pos_layout.addWidget(btn, i // 3, i % 3)

        self._position_group.button(8).setChecked(True)
        self._position_group.buttonClicked.connect(self._emit_settings_changed)
        layout.addWidget(pos_group)

        return widget

    def _create_image_settings(self) -> QWidget:
        """创建图片水印设置面板"""
        widget = QWidget()
        widget.setVisible(False)
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("水印图片:"))
        self._watermark_image_path = QLineEdit()
        self._watermark_image_path.setPlaceholderText("选择水印图片...")
        file_layout.addWidget(self._watermark_image_path)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self._browse_watermark_image)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("缩放:"))
        self._scale_slider = PercentageSlider("缩放:", 50)
        self._scale_slider.value_changed.connect(self._emit_settings_changed)
        scale_layout.addWidget(self._scale_slider)
        layout.addLayout(scale_layout)

        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("透明度:"))
        self._image_opacity_slider = PercentageSlider("透明度:", 80)
        self._image_opacity_slider.value_changed.connect(self._emit_settings_changed)
        opacity_layout.addWidget(self._image_opacity_slider)
        layout.addLayout(opacity_layout)

        return widget

    def _create_tiled_settings(self) -> QWidget:
        """创建平铺水印设置面板"""
        widget = QWidget()
        widget.setVisible(False)
        layout = QVBoxLayout(widget)

        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("平铺间距:"))
        self._spacing_slider = ValueSlider(min_value=50, max_value=500, value=100, label="间距:")
        self._spacing_slider.value_changed.connect(self._emit_settings_changed)
        spacing_layout.addWidget(self._spacing_slider)
        layout.addLayout(spacing_layout)

        rotate_layout = QHBoxLayout()
        rotate_layout.addWidget(QLabel("旋转角度:"))
        self._tiled_rotate_slider = ValueSlider(min_value=0, max_value=360, value=30, label="")
        self._tiled_rotate_slider.value_changed.connect(self._emit_settings_changed)
        rotate_layout.addWidget(self._tiled_rotate_slider)
        layout.addLayout(rotate_layout)

        return widget

    def _on_type_changed(self, checked: bool) -> None:
        """水印类型改变"""
        if not checked:
            return

        wtype = self._watermark_type_group.checkedId()
        self._text_settings.setVisible(wtype == 0)
        self._image_settings.setVisible(wtype == 1)
        self._tiled_settings.setVisible(wtype == 2)
        self._emit_settings_changed()

    def _select_color(self) -> None:
        """选择颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            self._color_btn.setStyleSheet(f"background-color: {color.name()};")

    def _browse_watermark_image(self) -> None:
        """浏览水印图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择水印图片", "", "图片文件 (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self._watermark_image_path.setText(file_path)

    def get_settings(self) -> Dict[str, Any]:
        """获取水印设置"""
        settings = super().get_settings()
        settings.update({
            "type": ["text", "image", "tiled"][self._watermark_type_group.checkedId()],
            "text": self._watermark_text.text(),
            "font": self._font_combo.currentFont().family(),
            "font_size": self._font_size.value(),
            "color": self._color_btn.styleSheet(),
            "opacity": self._opacity_slider.get_value(),
            "rotate": self._rotate_slider.get_value(),
            "position": self._position_group.checkedButton().text() if self._position_group.checkedButton() else "右下",
            "watermark_image": self._watermark_image_path.text(),
            "scale": self._scale_slider.get_value(),
            "spacing": self._spacing_slider.get_value()
        })
        return settings


class ResizeTab(BaseFeatureTab):
    """缩放标签页

    提供图像缩放功能：
    - 预设尺寸
    - 自定义尺寸
    - 等比缩放
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("📐 缩放", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        preset_group = QGroupBox("预设尺寸")
        preset_layout = QGridLayout(preset_group)

        presets = [
            ("800×600", 800, 600),
            ("1024×768", 1024, 768),
            ("1920×1080", 1920, 1080),
            ("4K (3840×2160)", 3840, 2160)
        ]

        self._preset_buttons = QButtonGroup()
        for i, (name, w, h) in enumerate(presets):
            btn = QRadioButton(name)
            self._preset_buttons.addButton(btn, i)
            preset_layout.addWidget(btn, i // 2, i % 2)

        layout.addWidget(preset_group)

        custom_group = QGroupBox("自定义尺寸")
        custom_layout = QGridLayout(custom_group)

        custom_layout.addWidget(QLabel("宽度:"), 0, 0)
        self._width_spin = QSpinBox()
        self._width_spin.setRange(1, 10000)
        self._width_spin.setValue(1920)
        self._width_spin.valueChanged.connect(self._emit_settings_changed)
        custom_layout.addWidget(self._width_spin, 0, 1)

        custom_layout.addWidget(QLabel("高度:"), 0, 2)
        self._height_spin = QSpinBox()
        self._height_spin.setRange(1, 10000)
        self._height_spin.setValue(1080)
        self._height_spin.valueChanged.connect(self._emit_settings_changed)
        custom_layout.addWidget(self._height_spin, 0, 3)

        self._keep_aspect_check = QCheckBox("保持宽高比")
        self._keep_aspect_check.setChecked(True)
        custom_layout.addWidget(self._keep_aspect_check, 1, 0, 1, 4)

        layout.addWidget(custom_group)

        algo_group = QGroupBox("缩放算法")
        algo_layout = QHBoxLayout(algo_group)

        self._algo_combo = QComboBox()
        self._algo_combo.addItems(["最近邻", "双线性", "双三次", "Lanczos"])
        self._algo_combo.setCurrentText("双线性")
        self._algo_combo.currentTextChanged.connect(self._emit_settings_changed)
        algo_layout.addWidget(QLabel("算法:"))
        algo_layout.addWidget(self._algo_combo)
        algo_layout.addStretch()
        layout.addWidget(algo_group)

        layout.addStretch()

    def get_settings(self) -> Dict[str, Any]:
        """获取缩放设置"""
        settings = super().get_settings()
        settings.update({
            "width": self._width_spin.value(),
            "height": self._height_spin.value(),
            "keep_aspect": self._keep_aspect_check.isChecked(),
            "algorithm": self._algo_combo.currentText()
        })
        return settings


class RotateTab(BaseFeatureTab):
    """旋转标签页

    提供图像旋转和翻转功能：
    - 固定角度旋转
    - 自定义角度旋转
    - 水平/垂直翻转
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("🔄 旋转", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        rotate_group = QGroupBox("旋转角度")
        rotate_layout = QGridLayout(rotate_group)

        angles = [("90°", 90), ("180°", 180), ("270°", 270)]
        self._angle_buttons = QButtonGroup()

        for i, (name, angle) in enumerate(angles):
            btn = QRadioButton(name)
            btn.setProperty("angle", angle)
            self._angle_buttons.addButton(btn, i)
            rotate_layout.addWidget(btn, 0, i)

        rotate_layout.addWidget(QLabel("自定义角度:"), 1, 0)
        self._custom_angle = QDoubleSpinBox()
        self._custom_angle.setRange(-180, 180)
        self._custom_angle.setValue(0)
        self._custom_angle.setSuffix("°")
        self._custom_angle.valueChanged.connect(self._emit_settings_changed)
        rotate_layout.addWidget(self._custom_angle, 1, 1, 1, 2)

        layout.addWidget(rotate_group)

        flip_group = QGroupBox("翻转")
        flip_layout = QHBoxLayout(flip_group)

        self._h_flip_btn = QPushButton("水平翻转")
        self._v_flip_btn = QPushButton("垂直翻转")
        self._h_flip_btn.clicked.connect(lambda: self._on_flip("horizontal"))
        self._v_flip_btn.clicked.connect(lambda: self._on_flip("vertical"))
        flip_layout.addWidget(self._h_flip_btn)
        flip_layout.addWidget(self._v_flip_btn)
        flip_layout.addStretch()

        layout.addWidget(flip_group)
        layout.addStretch()

    def _on_flip(self, direction: str) -> None:
        """翻转"""
        self._settings["flip"] = direction
        self._emit_settings_changed()

    def get_settings(self) -> Dict[str, Any]:
        """获取旋转设置"""
        settings = super().get_settings()
        angle = 0
        if self._angle_buttons.checkedButton():
            angle = self._angle_buttons.checkedButton().property("angle")

        settings.update({
            "angle": self._custom_angle.value() if self._custom_angle.value() != 0 else angle,
            "flip": self._settings.get("flip", None)
        })
        return settings


class FilterTab(BaseFeatureTab):
    """滤镜标签页

    提供图像滤镜功能：
    - 亮度/对比度/饱和度
    - 灰度转换
    - 模糊/锐化
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("🎨 滤镜", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        adjust_group = QGroupBox("图像调整")
        adjust_layout = QVBoxLayout(adjust_group)

        self._brightness_slider = ValueSlider("亮度:", min_value=-100, max_value=100, value=0)
        self._brightness_slider.value_changed.connect(self._emit_settings_changed)
        adjust_layout.addWidget(self._brightness_slider)

        self._contrast_slider = ValueSlider("对比度:", min_value=-100, max_value=100, value=0)
        self._contrast_slider.value_changed.connect(self._emit_settings_changed)
        adjust_layout.addWidget(self._contrast_slider)

        self._saturation_slider = ValueSlider("饱和度:", min_value=-100, max_value=100, value=0)
        self._saturation_slider.value_changed.connect(self._emit_settings_changed)
        adjust_layout.addWidget(self._saturation_slider)

        layout.addWidget(adjust_group)

        effect_group = QGroupBox("效果")
        effect_layout = QVBoxLayout(effect_group)

        self._gray_check = QCheckBox("灰度转换")
        self._gray_check.stateChanged.connect(self._emit_settings_changed)
        effect_layout.addWidget(self._gray_check)

        blur_layout = QHBoxLayout()
        blur_layout.addWidget(QLabel("模糊:"))
        self._blur_slider = ValueSlider(min_value=0, max_value=20, value=0, step=1)
        self._blur_slider.value_changed.connect(self._emit_settings_changed)
        blur_layout.addWidget(self._blur_slider)
        effect_layout.addLayout(blur_layout)

        sharpen_layout = QHBoxLayout()
        sharpen_layout.addWidget(QLabel("锐化:"))
        self._sharpen_slider = ValueSlider(min_value=0, max_value=3, value=0)
        self._sharpen_slider.value_changed.connect(self._emit_settings_changed)
        sharpen_layout.addWidget(self._sharpen_slider)
        effect_layout.addLayout(sharpen_layout)

        layout.addWidget(effect_group)
        layout.addStretch()

    def get_settings(self) -> Dict[str, Any]:
        """获取滤镜设置"""
        settings = super().get_settings()
        settings.update({
            "brightness": self._brightness_slider.get_value(),
            "contrast": self._contrast_slider.get_value(),
            "saturation": self._saturation_slider.get_value(),
            "grayscale": self._gray_check.isChecked(),
            "blur": self._blur_slider.get_value(),
            "sharpen": self._sharpen_slider.get_value()
        })
        return settings


class GifTab(BaseFeatureTab):
    """GIF标签页

    提供GIF制作功能：
    - 多图合成
    - 帧延迟设置
    - 循环次数
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("🎬 GIF", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        frame_group = QGroupBox("帧设置")
        frame_layout = QVBoxLayout(frame_group)

        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("帧延迟 (毫秒):"))
        self._delay_spin = QSpinBox()
        self._delay_spin.setRange(10, 10000)
        self._delay_spin.setValue(200)
        self._delay_spin.setSuffix(" ms")
        self._delay_spin.valueChanged.connect(self._emit_settings_changed)
        delay_layout.addWidget(self._delay_spin)
        frame_layout.addLayout(delay_layout)

        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("循环次数:"))
        self._loop_combo = QComboBox()
        self._loop_combo.addItems(["无限循环", "播放一次", "2次", "3次", "5次"])
        self._loop_combo.currentTextChanged.connect(self._emit_settings_changed)
        loop_layout.addWidget(self._loop_combo)
        loop_layout.addStretch()
        frame_layout.addLayout(loop_layout)

        layout.addWidget(frame_group)

        size_group = QGroupBox("尺寸设置")
        size_layout = QHBoxLayout(size_group)

        size_layout.addWidget(QLabel("宽度:"))
        self._gif_width = QSpinBox()
        self._gif_width.setRange(100, 2000)
        self._gif_width.setValue(480)
        self._gif_width.valueChanged.connect(self._emit_settings_changed)
        size_layout.addWidget(self._gif_width)

        size_layout.addWidget(QLabel("高度:"))
        self._gif_height = QSpinBox()
        self._gif_height.setRange(100, 2000)
        self._gif_height.setValue(320)
        self._gif_height.valueChanged.connect(self._emit_settings_changed)
        size_layout.addWidget(self._gif_height)

        self._gif_keep_aspect = QCheckBox("保持比例")
        self._gif_keep_aspect.setChecked(True)
        size_layout.addWidget(self._gif_keep_aspect)
        size_layout.addStretch()

        layout.addWidget(size_group)
        layout.addStretch()

    def get_settings(self) -> Dict[str, Any]:
        """获取GIF设置"""
        loop_map = {"无限循环": 0, "播放一次": 1, "2次": 2, "3次": 3, "5次": 5}
        settings = super().get_settings()
        settings.update({
            "delay": self._delay_spin.value(),
            "loop": loop_map.get(self._loop_combo.currentText(), 0),
            "width": self._gif_width.value(),
            "height": self._gif_height.value(),
            "keep_aspect": self._gif_keep_aspect.isChecked()
        })
        return settings


class RenameTab(BaseFeatureTab):
    """重命名标签页

    提供批量重命名功能：
    - 模板变量
    - 前缀/后缀
    - 序号格式
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("📝 重命名", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        template_group = QGroupBox("命名模板")
        template_layout = QVBoxLayout(template_group)

        self._template_edit = QLineEdit()
        self._template_edit.setPlaceholderText("例如: {name}_{date}_{index}")
        self._template_edit.setText("{name}_{index}")
        self._template_edit.textChanged.connect(self._emit_settings_changed)
        template_layout.addWidget(QLabel("模板变量:"))
        template_layout.addWidget(self._template_edit)

        help_text = QLabel("可用变量: {name} 原文件名, {date} 日期, {time} 时间, {index} 序号")
        help_text.setStyleSheet("color: #757575; font-size: 11px;")
        template_layout.addWidget(help_text)

        layout.addWidget(template_group)

        prefix_suffix = QGroupBox("前缀/后缀")
        ps_layout = QGridLayout(prefix_suffix)

        ps_layout.addWidget(QLabel("前缀:"), 0, 0)
        self._prefix_edit = QLineEdit()
        self._prefix_edit.textChanged.connect(self._emit_settings_changed)
        ps_layout.addWidget(self._prefix_edit, 0, 1)

        ps_layout.addWidget(QLabel("后缀:"), 1, 0)
        self._suffix_edit = QLineEdit()
        self._suffix_edit.textChanged.connect(self._emit_settings_changed)
        ps_layout.addWidget(self._suffix_edit, 1, 1)

        layout.addWidget(prefix_suffix)

        index_group = QGroupBox("序号设置")
        index_layout = QHBoxLayout(index_group)

        index_layout.addWidget(QLabel("起始值:"))
        self._start_index = QSpinBox()
        self._start_index.setRange(0, 99999)
        self._start_index.setValue(1)
        self._start_index.valueChanged.connect(self._emit_settings_changed)
        index_layout.addWidget(self._start_index)

        index_layout.addWidget(QLabel("位数:"))
        self._index_padding = QSpinBox()
        self._index_padding.setRange(1, 6)
        self._index_padding.setValue(3)
        self._index_padding.setSuffix(" 位")
        self._index_padding.valueChanged.connect(self._emit_settings_changed)
        index_layout.addWidget(self._index_padding)
        index_layout.addStretch()

        layout.addWidget(index_group)
        layout.addStretch()

    def get_settings(self) -> Dict[str, Any]:
        """获取重命名设置"""
        settings = super().get_settings()
        settings.update({
            "template": self._template_edit.text(),
            "prefix": self._prefix_edit.text(),
            "suffix": self._suffix_edit.text(),
            "start_index": self._start_index.value(),
            "index_padding": self._index_padding.value()
        })
        return settings


class PdfTab(BaseFeatureTab):
    """PDF标签页

    提供PDF转换功能：
    - 单张单页
    - 多张单页
    - 网格布局
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("📄 PDF", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        mode_group = QGroupBox("PDF模式")
        mode_layout = QVBoxLayout(mode_group)

        self._mode_group = QButtonGroup()
        modes = [
            ("单张单页", "single"),
            ("多张单页", "multi"),
            ("2×2 网格", "grid_2x2"),
            ("3×3 网格", "grid_3x3")
        ]

        for i, (name, mode) in enumerate(modes):
            btn = QRadioButton(name)
            btn.setProperty("mode", mode)
            self._mode_group.addButton(btn, i)
            mode_layout.addWidget(btn)

        self._mode_group.button(1).setChecked(True)
        layout.addWidget(mode_group)

        page_group = QGroupBox("页面设置")
        page_layout = QVBoxLayout(page_group)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("页面尺寸:"))
        self._page_size = QComboBox()
        self._page_size.addItems(["A4", "A3", "Letter", "Legal"])
        self._page_size.currentTextChanged.connect(self._emit_settings_changed)
        size_layout.addWidget(self._page_size)
        size_layout.addStretch()
        page_layout.addLayout(size_layout)

        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("边距 (像素):"))
        self._margin_spin = QSpinBox()
        self._margin_spin.setRange(0, 100)
        self._margin_spin.setValue(10)
        self._margin_spin.valueChanged.connect(self._emit_settings_changed)
        margin_layout.addWidget(self._margin_spin)
        margin_layout.addStretch()
        page_layout.addLayout(margin_layout)

        layout.addWidget(page_group)
        layout.addStretch()

    def get_settings(self) -> Dict[str, Any]:
        """获取PDF设置"""
        settings = super().get_settings()
        mode = "multi"
        if self._mode_group.checkedButton():
            mode = self._mode_group.checkedButton().property("mode")

        settings.update({
            "mode": mode,
            "page_size": self._page_size.currentText(),
            "margin": self._margin_spin.value()
        })
        return settings


class FeatureTabWidget(QTabWidget):
    """功能标签页容器

    管理所有功能标签页的切换
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._tabs: Dict[str, BaseFeatureTab] = {}

        self._init_tabs()

    def _init_tabs(self) -> None:
        """初始化所有标签页"""
        tabs = [
            CropTab(),
            WatermarkTab(),
            ResizeTab(),
            RotateTab(),
            FilterTab(),
            GifTab(),
            RenameTab(),
            PdfTab()
        ]

        for tab in tabs:
            self.addTab(tab, tab.get_title())
            self._tabs[tab.get_title()] = tab

    def get_tab(self, title: str) -> Optional[BaseFeatureTab]:
        """获取指定标签页"""
        return self._tabs.get(title)

    def get_current_settings(self) -> Dict[str, Any]:
        """获取当前标签页的设置"""
        current = self.currentWidget()
        if isinstance(current, BaseFeatureTab):
            return current.get_settings()
        return {}
