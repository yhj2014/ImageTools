"""滑块组件 - 带数值显示的滑块"""
from typing import Optional, Callable, Any
from functools import partial

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSlider,
    QLineEdit, QDoubleSpinBox, QSpinBox,
    QSizePolicy, QStyle
)


class ValueSlider(QWidget):
    """带数值显示的滑块组件

    支持：
    - 整数/浮点数滑块
    - 数值输入框
    - 范围限制
    - 步进值设置
    - 值变化信号
    """
    value_changed = Signal(float)

    def __init__(
        self,
        label: str = "",
        min_value: float = 0,
        max_value: float = 100,
        value: float = 50,
        step: float = 1,
        decimals: int = 0,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._decimals = decimals
        self._updating = False

        self._init_ui(label, value)

    def _init_ui(self, label_text: str, initial_value: float) -> None:
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        if label_text:
            self._label = QLabel(label_text)
            self._label.setMinimumWidth(60)
            layout.addWidget(self._label)
        else:
            self._label = None

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimumWidth(100)
        self._slider.setMinimum(int(self._min_value))
        self._slider.setMaximum(int(self._max_value))
        self._slider.setValue(int(initial_value))
        self._slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._slider.setTickInterval(int(self._step))
        self._slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self._slider, 1)

        self._value_label = QLabel()
        self._value_label.setMinimumWidth(50)
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._value_label)

        self._update_value_display(initial_value)

    def _on_slider_changed(self, value: int) -> None:
        """滑块值改变"""
        if self._updating:
            return

        actual_value = float(value)
        self._update_value_display(actual_value)
        self.value_changed.emit(actual_value)

    def _update_value_display(self, value: float) -> None:
        """更新数值显示"""
        if self._decimals > 0:
            self._value_label.setText(f"{value:.{self._decimals}f}")
        else:
            self._value_label.setText(str(int(value)))

    def set_value(self, value: float) -> None:
        """设置值

        Args:
            value: 新值
        """
        if self._updating:
            return

        value = max(self._min_value, min(self._max_value, value))
        self._updating = True
        self._slider.setValue(int(value))
        self._update_value_display(value)
        self._updating = False

    def get_value(self) -> float:
        """获取当前值"""
        return float(self._slider.value())

    def set_range(self, min_value: float, max_value: float) -> None:
        """设置范围

        Args:
            min_value: 最小值
            max_value: 最大值
        """
        self._min_value = min_value
        self._max_value = max_value
        self._slider.setMinimum(int(min_value))
        self._slider.setMaximum(int(max_value))

    def set_enabled(self, enabled: bool) -> None:
        """设置启用状态"""
        self._slider.setEnabled(enabled)
        if self._label:
            self._label.setEnabled(enabled)
        self._value_label.setEnabled(enabled)


class PercentageSlider(ValueSlider):
    """百分比滑块 - 专门用于百分比值

    范围 0-100，步进 1
    """

    def __init__(
        self,
        label: str = "百分比:",
        value: float = 50,
        parent: Optional[QWidget] = None
    ):
        super().__init__(
            label=label,
            min_value=0,
            max_value=100,
            value=value,
            step=1,
            decimals=0,
            parent=parent
        )


class RangeSlider(QWidget):
    """范围滑块 - 选择数值范围"""

    range_changed = Signal(float, float)

    def __init__(
        self,
        label: str = "",
        min_value: float = 0,
        max_value: float = 100,
        lower_value: float = 25,
        upper_value: float = 75,
        step: float = 1,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._min_value = min_value
        self._max_value = max_value
        self._step = step

        self._init_ui(label, lower_value, upper_value)

    def _init_ui(
        self,
        label_text: str,
        lower: float,
        upper: float
    ) -> None:
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        if label_text:
            self._label = QLabel(label_text)
            layout.addWidget(self._label)

        self._lower_slider = QSlider(Qt.Orientation.Horizontal)
        self._lower_slider.setMinimum(int(self._min_value))
        self._lower_slider.setMaximum(int(self._max_value))
        self._lower_slider.setValue(int(lower))
        self._lower_slider.valueChanged.connect(self._on_lower_changed)
        layout.addWidget(self._lower_slider)

        self._lower_label = QLabel(str(int(lower)))
        self._lower_label.setMinimumWidth(40)
        layout.addWidget(self._lower_label)

        self._upper_slider = QSlider(Qt.Orientation.Horizontal)
        self._upper_slider.setMinimum(int(self._min_value))
        self._upper_slider.setMaximum(int(self._max_value))
        self._upper_slider.setValue(int(upper))
        self._upper_slider.valueChanged.connect(self._on_upper_changed)
        layout.addWidget(self._upper_slider)

        self._upper_label = QLabel(str(int(upper)))
        self._upper_label.setMinimumWidth(40)
        layout.addWidget(self._upper_label)

    def _on_lower_changed(self, value: int) -> None:
        """下限值改变"""
        if value > self._upper_slider.value():
            self._upper_slider.setValue(value)
        self._lower_label.setText(str(value))
        self.range_changed.emit(value, self._upper_slider.value())

    def _on_upper_changed(self, value: int) -> None:
        """上限值改变"""
        if value < self._lower_slider.value():
            self._lower_slider.setValue(value)
        self._upper_label.setText(str(value))
        self.range_changed.emit(self._lower_slider.value(), value)

    def get_range(self) -> tuple[float, float]:
        """获取范围值"""
        return (
            float(self._lower_slider.value()),
            float(self._upper_slider.value())
        )

    def set_range(self, lower: float, upper: float) -> None:
        """设置范围值"""
        self._lower_slider.setValue(int(lower))
        self._upper_slider.setValue(int(upper))
