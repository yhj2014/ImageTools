# -*- coding: utf-8 -*-
"""
QSS 样式表模块 - PySide6 组件的样式定义

本模块提供完整的 QSS（Qt Style Sheets）样式表，支持：
- 现代简洁的设计风格
- 完整的组件样式覆盖
- 响应式布局适配
- 中文界面文字支持
"""

from .theme import Theme


# =============================================================================
# 基础样式 - 全局样式和应用到所有组件的基础样式
# =============================================================================

def get_base_styles() -> str:
    """
    获取基础样式表 - 全局样式和字体设置
    
    Returns:
        包含基础样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       全局基础样式
       ========================================================================== */
    
    /* 重置 QMainWindow 的默认内边距 */
    QMainWindow {{
        padding: 0px;
        margin: 0px;
    }}
    
    /* 主窗口背景 */
    QWidget {{
        background-color: {colors.background};
        color: {colors.text_primary};
        font-family: {' '.join(fonts.primary)};
        font-size: {fonts.size_base}px;
        selection-background-color: {colors.primary};
        selection-color: {colors.text_on_primary};
    }}
    
    /* 所有输入组件的字体大小 */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QDateEdit, QTimeEdit, QDateTimeEdit {{
        font-size: {fonts.size_base}px;
    }}
    
    /* 滚动条基础样式 */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 10px;
        margin: 0px;
        border: none;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors.scrollbar};
        min-height: 30px;
        border-radius: 5px;
        margin: 2px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors.scrollbar_hover};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
        background: none;
        border: none;
    }}
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
    
    QScrollBar:horizontal {{
        background-color: transparent;
        height: 10px;
        margin: 0px;
        border: none;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {colors.scrollbar};
        min-width: 30px;
        border-radius: 5px;
        margin: 2px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {colors.scrollbar_hover};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
        background: none;
        border: none;
    }}
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}
    
    /* 文字选择样式 */
    QMenuBar::item:selected, QMenu::item:selected {{
        background-color: {colors.primary_light};
        color: {colors.text_on_primary};
    }}
    
    /* 禁用状态的文字颜色 */
    QWidget:disabled {{
        color: {colors.text_disabled};
    }}
    """


# =============================================================================
# 按钮样式
# =============================================================================

def get_button_styles() -> str:
    """
    获取按钮样式表 - 包含所有类型按钮的样式
    
    Returns:
        包含按钮样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       按钮样式
       ========================================================================== */
    
    /* 普通按钮 - 主要操作 */
    QPushButton {{
        background-color: {colors.primary};
        color: {colors.text_on_primary};
        border: none;
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px {sizes.padding_lg}px;
        min-height: {sizes.button_height_md}px;
        font-size: {fonts.size_base}px;
        font-weight: {fonts.weight_medium};
        outline: none;
    }}
    
    QPushButton:hover {{
        background-color: {colors.primary_hover};
    }}
    
    QPushButton:pressed {{
        background-color: {colors.primary_dark};
    }}
    
    QPushButton:disabled {{
        background-color: {colors.border};
        color: {colors.text_disabled};
    }}
    
    QPushButton:focus {{
        border: 2px solid {colors.primary_light};
    }}
    
    /* 次要按钮 */
    QPushButton[class="secondary"] {{
        background-color: {colors.secondary};
        color: {colors.text_on_primary};
    }}
    
    QPushButton[class="secondary"]:hover {{
        background-color: {colors.secondary_hover};
    }}
    
    /* 成功按钮 */
    QPushButton[class="success"] {{
        background-color: {colors.success};
        color: {colors.text_on_primary};
    }}
    
    QPushButton[class="success"]:hover {{
        background-color: {colors.success_hover};
    }}
    
    /* 警告按钮 */
    QPushButton[class="warning"] {{
        background-color: {colors.warning};
        color: {colors.text_on_primary};
    }}
    
    QPushButton[class="warning"]:hover {{
        background-color: {colors.warning_hover};
    }}
    
    /* 危险/错误按钮 */
    QPushButton[class="danger"] {{
        background-color: {colors.error};
        color: {colors.text_on_primary};
    }}
    
    QPushButton[class="danger"]:hover {{
        background-color: {colors.error_hover};
    }}
    
    /* 透明按钮 - 只有文字 */
    QPushButton[class="text"] {{
        background-color: transparent;
        color: {colors.primary};
    }}
    
    QPushButton[class="text"]:hover {{
        background-color: {colors.primary_light}20;
    }}
    
    QPushButton[class="text"]:pressed {{
        background-color: {colors.primary_light}40;
    }}
    
    /* 轮廓按钮 - 有边框 */
    QPushButton[class="outline"] {{
        background-color: transparent;
        color: {colors.primary};
        border: 1px solid {colors.primary};
    }}
    
    QPushButton[class="outline"]:hover {{
        background-color: {colors.primary_light}20;
    }}
    
    /* 小尺寸按钮 */
    QPushButton[class="small"] {{
        min-height: {sizes.button_height_sm}px;
        padding: {sizes.padding_xs}px {sizes.padding_sm}px;
        font-size: {fonts.size_sm}px;
    }}
    
    /* 大尺寸按钮 */
    QPushButton[class="large"] {{
        min-height: {sizes.button_height_lg}px;
        padding: {sizes.padding_md}px {sizes.padding_xl}px;
        font-size: {fonts.size_lg}px;
    }}
    
    /* 图标按钮 */
    QPushButton[class="icon"] {{
        background-color: transparent;
        border: none;
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_xs}px;
        min-width: {sizes.icon_xl}px;
        min-height: {sizes.icon_xl}px;
    }}
    
    QPushButton[class="icon"]:hover {{
        background-color: {colors.background_dark};
    }}
    
    /* 工具栏按钮 */
    QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px;
        color: {colors.text_primary};
    }}
    
    QToolButton:hover {{
        background-color: {colors.background_dark};
    }}
    
    QToolButton:pressed {{
        background-color: {colors.border};
    }}
    
    QToolButton:checked {{
        background-color: {colors.primary_light}30;
        color: {colors.primary};
    }}
    
    /* 菜单按钮 */
    QToolButton::menu-button {{
        border: none;
        width: 16px;
    }}
    
    QToolButton::menu-indicator {{
        image: none;
        subcontrol-origin: padding;
        subcontrol-position: right center;
    }}
    """


# =============================================================================
# 输入框样式
# =============================================================================

def get_input_styles() -> str:
    """
    获取输入框样式表 - 包含文本输入、下拉框等样式
    
    Returns:
        包含输入框样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       输入框样式
       ========================================================================== */
    
    /* 单行文本输入框 */
    QLineEdit {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        min-height: {sizes.input_height_md}px;
        selection-background-color: {colors.primary};
    }}
    
    QLineEdit:hover {{
        border-color: {colors.border_hover};
    }}
    
    QLineEdit:focus {{
        border-color: {colors.border_focus};
    }}
    
    QLineEdit:disabled {{
        background-color: {colors.background_dark};
        border-color: {colors.border_disabled};
        color: {colors.text_disabled};
    }}
    
    /* 提示占位符文字样式（需要通过 setStyleSheet 设置） */
    QLineEdit[placeholder="true"] {{
        color: {colors.text_tertiary};
    }}
    
    /* 多行文本编辑框 */
    QTextEdit, QPlainTextEdit {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_md}px;
        selection-background-color: {colors.primary};
    }}
    
    QTextEdit:hover, QPlainTextEdit:hover {{
        border-color: {colors.border_hover};
    }}
    
    QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {colors.border_focus};
    }}
    
    QTextEdit:disabled, QPlainTextEdit:disabled {{
        background-color: {colors.background_dark};
        border-color: {colors.border_disabled};
        color: {colors.text_disabled};
    }}
    
    /* 数字输入框 */
    QSpinBox, QDoubleSpinBox {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px;
        min-height: {sizes.input_height_md}px;
    }}
    
    QSpinBox:hover, QDoubleSpinBox:hover {{
        border-color: {colors.border_hover};
    }}
    
    QSpinBox:focus, QDoubleSpinBox:focus {{
        border-color: {colors.border_focus};
    }}
    
    QSpinBox:disabled, QDoubleSpinBox:disabled {{
        background-color: {colors.background_dark};
        color: {colors.text_disabled};
    }}
    
    /* 数字输入框的上下箭头 */
    QSpinBox::up-button, QDoubleSpinBox::up-button {{
        background-color: transparent;
        border: none;
        border-left: 1px solid {colors.border};
        border-radius: 0px;
        width: 24px;
    }}
    
    QSpinBox::down-button, QDoubleSpinBox::down-button {{
        background-color: transparent;
        border: none;
        border-left: 1px solid {colors.border};
        border-radius: 0px;
        width: 24px;
    }}
    
    QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
    QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {colors.background_dark};
    }}
    
    /* 下拉框 */
    QComboBox {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px {sizes.padding_lg}px;
        min-height: {sizes.input_height_md}px;
    }}
    
    QComboBox:hover {{
        border-color: {colors.border_hover};
    }}
    
    QComboBox:focus {{
        border-color: {colors.border_focus};
    }}
    
    QComboBox:disabled {{
        background-color: {colors.background_dark};
        color: {colors.text_disabled};
    }}
    
    /* 下拉框下拉按钮 */
    QComboBox::drop-down {{
        border: none;
        width: 24px;
        subcontrol-origin: padding;
        subcontrol-position: right center;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {colors.text_secondary};
        margin-right: 8px;
    }}
    
    QComboBox::down-arrow:hover {{
        border-top-color: {colors.text_primary};
    }}
    
    /* 下拉菜单 */
    QComboBox QAbstractItemView {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_xs}px;
        selection-background-color: {colors.primary_light}30;
        outline: none;
    }}
    
    QComboBox QAbstractItemView::item {{
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        border-radius: {sizes.radius_xs}px;
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background-color: {colors.background_dark};
    }}
    
    /* 日期时间选择器 */
    QDateEdit, QTimeEdit, QDateTimeEdit {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px;
        min-height: {sizes.input_height_md}px;
    }}
    
    QDateEdit:hover, QTimeEdit:hover, QDateTimeEdit:hover {{
        border-color: {colors.border_hover};
    }}
    
    QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {{
        border-color: {colors.border_focus};
    }}
    
    QDateEdit::drop-down, QTimeEdit::drop-down, QDateTimeEdit::drop-down {{
        border: none;
        width: 24px;
        subcontrol-origin: padding;
        subcontrol-position: right center;
    }}
    
    QDateEdit::down-arrow, QTimeEdit::down-arrow, QDateTimeEdit::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {colors.text_secondary};
        margin-right: 8px;
    }}
    
    /* 滑块 */
    QSlider::groove:horizontal {{
        border: none;
        height: 4px;
        background-color: {colors.border};
        border-radius: 2px;
    }}
    
    QSlider::handle:horizontal {{
        background-color: {colors.primary};
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}
    
    QSlider::handle:horizontal:hover {{
        background-color: {colors.primary_hover};
    }}
    
    QSlider::sub-page:horizontal {{
        background-color: {colors.primary};
        border-radius: 2px;
    }}
    
    QSlider::groove:vertical {{
        border: none;
        width: 4px;
        background-color: {colors.border};
        border-radius: 2px;
    }}
    
    QSlider::handle:vertical {{
        background-color: {colors.primary};
        width: 16px;
        height: 16px;
        margin: 0 -6px;
        border-radius: 8px;
    }}
    
    QSlider::handle:vertical:hover {{
        background-color: {colors.primary_hover};
    }}
    
    QSlider::add-page:vertical {{
        background-color: {colors.primary};
        border-radius: 2px;
    }}
    
    /* 复选框 */
    QCheckBox {{
        background-color: transparent;
        color: {colors.text_primary};
        spacing: {sizes.space_sm}px;
    }}
    
    QCheckBox:hover {{
        color: {colors.text_primary};
    }}
    
    QCheckBox::indicator {{
        width: {sizes.icon_md}px;
        height: {sizes.icon_md}px;
        border: 2px solid {colors.border};
        border-radius: {sizes.radius_xs}px;
        background-color: {colors.surface};
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {colors.border_hover};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {colors.primary};
        border-color: {colors.primary};
        image: none;
    }}
    
    QCheckBox::indicator:checked:hover {{
        background-color: {colors.primary_hover};
        border-color: {colors.primary_hover};
    }}
    
    QCheckBox::indicator:indeterminate {{
        background-color: {colors.primary};
        border-color: {colors.primary};
    }}
    
    QCheckBox::indicator:disabled {{
        background-color: {colors.background_dark};
        border-color: {colors.border_disabled};
    }}
    
    QCheckBox:disabled {{
        color: {colors.text_disabled};
    }}
    
    /* 单选按钮 */
    QRadioButton {{
        background-color: transparent;
        color: {colors.text_primary};
        spacing: {sizes.space_sm}px;
    }}
    
    QRadioButton:hover {{
        color: {colors.text_primary};
    }}
    
    QRadioButton::indicator {{
        width: {sizes.icon_md}px;
        height: {sizes.icon_md}px;
        border: 2px solid {colors.border};
        border-radius: 8px;
        background-color: {colors.surface};
    }}
    
    QRadioButton::indicator:hover {{
        border-color: {colors.border_hover};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {colors.primary};
        border-color: {colors.primary};
    }}
    
    QRadioButton::indicator:checked:hover {{
        background-color: {colors.primary_hover};
        border-color: {colors.primary_hover};
    }}
    
    QRadioButton::indicator:disabled {{
        background-color: {colors.background_dark};
        border-color: {colors.border_disabled};
    }}
    
    QRadioButton:disabled {{
        color: {colors.text_disabled};
    }}
    
    /* 进度条 */
    QProgressBar {{
        background-color: {colors.background_dark};
        border: none;
        border-radius: {sizes.radius_sm}px;
        min-height: 8px;
        text-align: center;
        color: {colors.text_secondary};
        font-size: {fonts.size_sm}px;
    }}
    
    QProgressBar::chunk {{
        background-color: {colors.primary};
        border-radius: {sizes.radius_sm}px;
    }}
    
    /* 标签 */
    QLabel {{
        background-color: transparent;
        color: {colors.text_primary};
        padding: 0px;
    }}
    
    /* 可链接的标签 */
    QLabel[class="link"] {{
        color: {colors.primary};
        text-decoration: underline;
    }}
    
    QLabel[class="link"]:hover {{
        color: {colors.primary_hover};
    }}
    
    /* 提示标签（用于说明文字） */
    QLabel[class="helper"] {{
        color: {colors.text_secondary};
        font-size: {fonts.size_sm}px;
    }}
    
    /* 徽章标签 */
    QLabel[class="badge"] {{
        background-color: {colors.primary};
        color: {colors.text_on_primary};
        border-radius: {sizes.radius_full}px;
        padding: 2px 8px;
        font-size: {fonts.size_xs}px;
        font-weight: {fonts.weight_bold};
    }}
    
    /* 错误标签 */
    QLabel[class="error"] {{
        color: {colors.error};
        font-size: {fonts.size_sm}px;
    }}
    
    /* 标题标签 */
    QLabel[class="title"] {{
        color: {colors.text_primary};
        font-size: {fonts.size_xl}px;
        font-weight: {fonts.weight_semibold};
    }}
    
    /* 子标题标签 */
    QLabel[class="subtitle"] {{
        color: {colors.text_secondary};
        font-size: {fonts.size_md}px;
    }}
    """


# =============================================================================
# 容器和布局样式
# =============================================================================

def get_container_styles() -> str:
    """
    获取容器样式表 - 包含分组框、框架、卡片等容器样式
    
    Returns:
        包含容器样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       容器和布局样式
       ========================================================================== */
    
    /* 分组框 */
    QGroupBox {{
        background-color: transparent;
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        margin-top: 16px;
        padding-top: 16px;
        padding-bottom: 8px;
        padding-left: 8px;
        padding-right: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 8px;
        padding: 0 8px;
        color: {colors.text_primary};
        font-size: {fonts.size_md}px;
        font-weight: {fonts.weight_semibold};
    }}
    
    QGroupBox::title:disabled {{
        color: {colors.text_disabled};
    }}
    
    /* 框架 */
    QFrame {{
        background-color: transparent;
        border: none;
    }}
    
    /* 分隔线 */
    QFrame[class="divider"] {{
        background-color: {colors.divider};
    }}
    
    QFrame[class="divider"][orientation="horizontal"] {{
        max-height: 1px;
        min-height: 1px;
    }}
    
    QFrame[class="divider"][orientation="vertical"] {{
        max-width: 1px;
        min-width: 1px;
    }}
    
    /* 卡片容器 */
    QFrame[class="card"] {{
        background-color: {colors.background_card};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        padding: {sizes.padding_lg}px;
    }}
    
    /* 提升的卡片 */
    QFrame[class="card"][elevated="true"] {{
        border: none;
        background-color: {colors.background_card};
        border-radius: {sizes.radius_md}px;
        padding: {sizes.padding_lg}px;
    }}
    
    /* 透明背景的卡片 */
    QFrame[class="card"][flat="true"] {{
        background-color: transparent;
        border: none;
        border-radius: 0px;
        padding: 0px;
    }}
    
    /* 滚动区域 */
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    
    QScrollArea:focus {{
        border: none;
    }}
    
    /* 容器小部件 */
    QWidget[class="container"] {{
        background-color: {colors.background};
    }}
    
    /* 工具栏容器 */
    QToolBar {{
        background-color: {colors.surface};
        border: none;
        border-bottom: 1px solid {colors.border};
        spacing: {sizes.space_sm}px;
        padding: {sizes.padding_sm}px;
    }}
    
    QToolBar::separator {{
        background-color: {colors.border};
        width: 1px;
        margin: 4px 8px;
    }}
    
    /* 状态栏 */
    QStatusBar {{
        background-color: {colors.surface};
        border-top: 1px solid {colors.border};
        color: {colors.text_secondary};
        font-size: {fonts.size_sm}px;
    }}
    
    QStatusBar QLabel {{
        padding: 2px 8px;
    }}
    
    /* 停靠窗口 */
    QDockWidget {{
        titlebar-close-icon: url(none);
        titlebar-normal-icon: url(none);
    }}
    
    QDockWidget::title {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        text-align: left;
    }}
    
    QDockWidget::close-button, QDockWidget::float-button {{
        background-color: transparent;
        border: none;
        padding: 2px;
    }}
    
    QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
        background-color: {colors.background_dark};
        border-radius: {sizes.radius_xs}px;
    }}
    
    /* 栈式窗口（用于 QStackedWidget） */
    QStackedWidget {{
        background-color: {colors.background};
    }}
    
    /* 窗口小部件 */
    QWidget#qt_design_stackedwidget_stackedobject {{
        background-color: {colors.background};
    }}
    """


# =============================================================================
# 菜单和对话框样式
# =============================================================================

def get_menu_dialog_styles() -> str:
    """
    获取菜单和对话框样式表
    
    Returns:
        包含菜单和对话框样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       菜单和对话框样式
       ========================================================================== */
    
    /* 菜单栏 */
    QMenuBar {{
        background-color: {colors.surface};
        border-bottom: 1px solid {colors.border};
        padding: 4px;
        color: {colors.text_primary};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        border-radius: {sizes.radius_sm}px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {colors.primary_light}30;
    }}
    
    QMenuBar::item:pressed {{
        background-color: {colors.primary_light}50;
    }}
    
    /* 下拉菜单 */
    QMenu {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        padding: {sizes.padding_xs}px;
        color: {colors.text_primary};
    }}
    
    QMenu::item {{
        background-color: transparent;
        padding: {sizes.padding_sm}px {sizes.padding_lg}px;
        border-radius: {sizes.radius_sm}px;
        min-width: 120px;
    }}
    
    QMenu::item:selected {{
        background-color: {colors.primary_light}30;
    }}
    
    QMenu::separator {{
        height: 1px;
        background-color: {colors.border};
        margin: {sizes.padding_xs}px {sizes.padding_sm}px;
    }}
    
    QMenu::indicator {{
        width: 16px;
        height: 16px;
        margin-right: 4px;
    }}
    
    QMenu::indicator:non-exclusive:unchecked {{
        image: none;
    }}
    
    QMenu::indicator:non-exclusive:checked {{
        image: none;
        border: 2px solid {colors.primary};
        background-color: {colors.primary};
        border-radius: 3px;
    }}
    
    /* 子菜单箭头 */
    QMenu::right-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-left-color: {colors.text_secondary};
        margin-right: 8px;
    }}
    
    QMenu::right-arrow:hover {{
        border-left-color: {colors.text_primary};
    }}
    
    /* 菜单提示 */
    QMenu QLabel {{
        padding: 4px {sizes.padding_lg}px;
        color: {colors.text_secondary};
        font-size: {fonts.size_sm}px;
    }}
    
    /* 对话框 */
    QDialog {{
        background-color: {colors.background};
    }}
    
    /* 消息框 */
    QMessageBox {{
        background-color: {colors.background};
    }}
    
    QMessageBox QLabel {{
        color: {colors.text_primary};
        padding: {sizes.padding_md}px;
    }}
    
    QMessageBox QPushButton {{
        min-width: 80px;
        min-height: {sizes.button_height_md}px;
    }}
    
    /* 文件对话框 */
    QFileDialog {{
        background-color: {colors.background};
    }}
    
    QFileDialog QLabel {{
        color: {colors.text_primary};
    }}
    
    QFileDialog QLineEdit {{
        background-color: {colors.surface};
    }}
    
    /* 颜色选择器 */
    QColorDialog {{
        background-color: {colors.background};
    }}
    
    /* 字体选择器 */
    QFontDialog {{
        background-color: {colors.background};
    }}
    
    /* 输入对话框 */
    QInputDialog {{
        background-color: {colors.background};
    }}
    
    QInputDialog QLabel {{
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px;
    }}
    
    /* 进度对话框 */
    QProgressDialog {{
        background-color: {colors.background};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
    }}
    
    QProgressDialog QLabel {{
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px;
    }}
    
    /* 工具提示 */
    QToolTip {{
        background-color: {colors.text_primary};
        color: {colors.background};
        border: none;
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        font-size: {fonts.size_sm}px;
    }}
    
    /* 什么是这个提示 */
    QWhatsThis {{
        background-color: {colors.text_primary};
        color: {colors.background};
        border: none;
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
    }}
    
    /* 气泡提示 */
    QBubbleTip {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
    }}
    """


# =============================================================================
# 列表和树形结构样式
# =============================================================================

def get_list_tree_styles() -> str:
    """
    获取列表和树形结构样式表 - 包含列表、树、表格等样式
    
    Returns:
        包含列表和树形结构样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       列表、树和表格样式
       ========================================================================== */
    
    /* 列表小部件 */
    QListWidget, QListView {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        padding: {sizes.padding_xs}px;
        outline: none;
    }}
    
    QListWidget:hover, QListView:hover {{
        border-color: {colors.border_hover};
    }}
    
    QListWidget:focus, QListView:focus {{
        border-color: {colors.border_focus};
    }}
    
    QListWidget::item, QListView::item {{
        background-color: transparent;
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        border-radius: {sizes.radius_sm}px;
        min-height: 36px;
    }}
    
    QListWidget::item:hover, QListView::item:hover {{
        background-color: {colors.background_dark};
    }}
    
    QListWidget::item:selected, QListView::item:selected {{
        background-color: {colors.primary_light}30;
        color: {colors.primary};
    }}
    
    QListWidget::item:selected:!active, QListView::item:selected:!active {{
        background-color: {colors.background_dark};
        color: {colors.text_primary};
    }}
    
    /* 树形小部件 */
    QTreeWidget, QTreeView {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        padding: {sizes.padding_xs}px;
        outline: none;
    }}
    
    QTreeWidget:hover, QTreeView:hover {{
        border-color: {colors.border_hover};
    }}
    
    QTreeWidget:focus, QTreeView:focus {{
        border-color: {colors.border_focus};
    }}
    
    QTreeWidget::item, QTreeView::item {{
        background-color: transparent;
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px;
        min-height: 32px;
    }}
    
    QTreeWidget::item:hover, QTreeView::item:hover {{
        background-color: {colors.background_dark};
    }}
    
    QTreeWidget::item:selected, QTreeView::item:selected {{
        background-color: {colors.primary_light}30;
        color: {colors.primary};
    }}
    
    /* 树形结构的分支指示器 */
    QTreeWidget::branch, QTreeView::branch {{
        background-color: transparent;
    }}
    
    QTreeWidget::branch:has-children:!has-siblings:closed,
    QTreeWidget::branch:closed:has-children:has-siblings,
    QTreeView::branch:has-children:!has-siblings:closed,
    QTreeView::branch:closed:has-children:has-siblings {{
        border-image: none;
        image: none;
    }}
    
    QTreeWidget::branch:open:has-children:!has-siblings,
    QTreeWidget::branch:open:has-children:has-siblings,
    QTreeView::branch:open:has-children:!has-siblings,
    QTreeView::branch:open:has-children:has-siblings {{
        border-image: none;
        image: none;
    }}
    
    /* 表格小部件 */
    QTableWidget, QTableView {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        padding: 0px;
        outline: none;
        gridline-color: {colors.border};
        selection-background-color: {colors.primary_light}30;
    }}
    
    QTableWidget:hover, QTableView:hover {{
        border-color: {colors.border_hover};
    }}
    
    QTableWidget:focus, QTableView:focus {{
        border-color: {colors.border_focus};
    }}
    
    /* 表格标题栏 */
    QTableWidget QHeaderView::section,
    QTableView QHeaderView::section {{
        background-color: {colors.background_dark};
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
        border: none;
        border-bottom: 2px solid {colors.border};
        border-right: 1px solid {colors.border};
        font-weight: {fonts.weight_semibold};
        font-size: {fonts.size_sm}px;
    }}
    
    QTableWidget QHeaderView::section:hover,
    QTableView QHeaderView::section:hover {{
        background-color: {colors.border};
    }}
    
    QTableWidget QHeaderView::section:pressed,
    QTableView QHeaderView::section:pressed {{
        background-color: {colors.border_hover};
    }}
    
    /* 表格单元格 */
    QTableWidget::item, QTableView::item {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        padding: {sizes.padding_sm}px {sizes.padding_md}px;
    }}
    
    QTableWidget::item:hover, QTableView::item:hover {{
        background-color: {colors.background_dark};
    }}
    
    QTableWidget::item:selected, QTableView::item:selected {{
        background-color: {colors.primary_light}30;
        color: {colors.primary};
    }}
    
    /* 交替行颜色 */
    QTableWidget#alternating_colors::item,
    QTableView#alternating_colors::item {{
        background-color: {colors.surface};
    }}
    
    QTableWidget#alternating_colors::item:alternate,
    QTableView#alternating_colors::item:alternate {{
        background-color: {colors.background_dark};
    }}
    
    /* 表格角按钮（resize 区域） */
    QTableView::corner {{
        background-color: {colors.background_dark};
        border: none;
    }}
    
    /* 表格排序指示器 */
    QTableWidget QHeaderView::section:horizontal {
        border-left: none;
    }
    
    /* 表头排序列箭头 */
    QTreeView::header:horizontal {{
        border: none;
    }}
    """


# =============================================================================
# 标签页和面板样式
# =============================================================================

def get_tab_panel_styles() -> str:
    """
    获取标签页和面板样式表
    
    Returns:
        包含标签页和面板样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       标签页和面板样式
       ========================================================================== */
    
    /* 标签部件 - 顶部标签栏 */
    QTabWidget::pane {{
        background-color: {colors.background};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        top: -1px;
    }}
    
    QTabWidget::tab-bar {{
        alignment: left;
    }}
    
    /* 标签栏样式 - 顶部 */
    QTabBar::tab {{
        background-color: {colors.background_dark};
        color: {colors.text_secondary};
        padding: {sizes.padding_sm}px {sizes.padding_lg}px;
        min-width: 100px;
        min-height: 36px;
        border: 1px solid {colors.border};
        border-bottom: none;
        border-top-left-radius: {sizes.radius_sm}px;
        border-top-right-radius: {sizes.radius_sm}px;
        font-weight: {fonts.weight_medium};
    }}
    
    QTabBar::tab:hover {{
        background-color: {colors.surface};
        color: {colors.text_primary};
    }}
    
    QTabBar::tab:selected {{
        background-color: {colors.background};
        color: {colors.primary};
        border-color: {colors.border};
        border-bottom-color: {colors.background};
    }}
    
    QTabBar::tab:!selected {{
        margin-top: 2px;
    }}
    
    /* 标签栏样式 - 底部 */
    QTabWidget[tab-position="south"]::pane {{
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        bottom: -1px;
    }}
    
    QTabWidget[tab-position="south"] QTabBar::tab {{
        border: 1px solid {colors.border};
        border-top: none;
        border-bottom-left-radius: {sizes.radius_sm}px;
        border-bottom-right-radius: {sizes.radius_sm}px;
    }}
    
    QTabWidget[tab-position="south"] QTabBar::tab:selected {{
        border-bottom-color: {colors.background};
    }}
    
    /* 标签栏样式 - 左侧 */
    QTabWidget[tab-position="west"]::pane {{
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        left: -1px;
    }}
    
    QTabWidget[tab-position="west"] QTabBar::tab {{
        border: 1px solid {colors.border};
        border-right: none;
        border-top-left-radius: {sizes.radius_sm}px;
        border-bottom-left-radius: {sizes.radius_sm}px;
        min-width: 80px;
    }}
    
    QTabWidget[tab-position="west"] QTabBar::tab:selected {{
        border-right-color: {colors.background};
    }}
    
    /* 标签栏样式 - 右侧 */
    QTabWidget[tab-position="east"]::pane {{
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_md}px;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
        right: -1px;
    }}
    
    QTabWidget[tab-position="east"] QTabBar::tab {{
        border: 1px solid {colors.border};
        border-left: none;
        border-top-right-radius: {sizes.radius_sm}px;
        border-bottom-right-radius: {sizes.radius_sm}px;
        min-width: 80px;
    }}
    
    QTabWidget[tab-position="east"] QTabBar::tab:selected {{
        border-left-color: {colors.background};
    }}
    
    /* 可关闭的标签 */
    QTabBar::tab:selected {{
        border-bottom: 2px solid {colors.primary};
    }}
    
    QTabBar QToolButton {{
        background-color: transparent;
        border: none;
        width: 16px;
    }}
    
    QTabBar QToolButton::right-arrow {{
        image: none;
        border-left: 4px solid {colors.text_secondary};
        border-top: 4px solid transparent;
        border-bottom: 4px solid transparent;
    }}
    
    QTabBar QToolButton::left-arrow {{
        image: none;
        border-right: 4px solid {colors.text_secondary};
        border-top: 4px solid transparent;
        border-bottom: 4px solid transparent;
    }}
    
    /* 折叠面板 */
    QScrollArea#collapsible_box {{
        background-color: transparent;
        border: none;
    }}
    
    /* 分割器 */
    QSplitter::handle {{
        background-color: {colors.border};
    }}
    
    QSplitter::handle:horizontal {{
        width: 1px;
        margin: 4px 0;
    }}
    
    QSplitter::handle:vertical {{
        height: 1px;
        margin: 0 4px;
    }}
    
    QSplitter::handle:hover {{
        background-color: {colors.border_hover};
    }}
    
    QSplitter::handle:pressed {{
        background-color: {colors.primary};
    }}
    """


# =============================================================================
# 自定义组件样式
# =============================================================================

def get_custom_styles() -> str:
    """
    获取自定义组件样式表 - 包含自定义 UI 组件的样式
    
    Returns:
        包含自定义组件样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       自定义组件样式
       ========================================================================== */
    
    /* 搜索框 */
    QLineEdit[class="search"] {{
        background-color: {colors.background_dark};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_full}px;
        padding: {sizes.padding_sm}px {sizes.padding_lg}px;
        padding-left: 36px;
    }}
    
    QLineEdit[class="search"]:focus {{
        background-color: {colors.surface};
        border-color: {colors.primary};
    }}
    
    /* 工具栏搜索框 */
    QWidget[class="search-container"] {{
        background-color: transparent;
    }}
    
    /* 侧边栏 */
    QWidget[class="sidebar"] {{
        background-color: {colors.surface};
        border-right: 1px solid {colors.border};
    }}
    
    /* 导航菜单项 */
    QWidget[class="nav-item"]:hover {{
        background-color: {colors.background_dark};
    }}
    
    QWidget[class="nav-item"][active="true"] {{
        background-color: {colors.primary_light}20;
    }}
    
    QWidget[class="nav-item"]:hover QLabel,
    QWidget[class="nav-item"][active="true"] QLabel {{
        color: {colors.primary};
    }}
    
    /* 头像 */
    QWidget[class="avatar"] {{
        background-color: {colors.primary_light};
        border-radius: {sizes.radius_full}px;
    }}
    
    QWidget[class="avatar"][size="small"] {{
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
    }}
    
    QWidget[class="avatar"][size="medium"] {{
        min-width: 40px;
        max-width: 40px;
        min-height: 40px;
        max-height: 40px;
    }}
    
    QWidget[class="avatar"][size="large"] {{
        min-width: 48px;
        max-width: 48px;
        min-height: 48px;
        max-height: 48px;
    }}
    
    /* 分割按钮组 */
    QWidget[class="button-group"] {{
        background-color: transparent;
    }}
    
    QWidget[class="button-group"] QPushButton {{
        border-radius: 0px;
        margin: 0px;
    }}
    
    QWidget[class="button-group"] QPushButton:first {{
        border-top-left-radius: {sizes.radius_sm}px;
        border-bottom-left-radius: {sizes.radius_sm}px;
    }}
    
    QWidget[class="button-group"] QPushButton:last {{
        border-top-right-radius: {sizes.radius_sm}px;
        border-bottom-right-radius: {sizes.radius_sm}px;
    }}
    
    QWidget[class="button-group"] QPushButton:only-one {{
        border-radius: {sizes.radius_sm}px;
    }}
    
    /* 标签输入框容器 */
    QWidget[class="tag-input-container"] {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: {sizes.radius_sm}px;
        padding: {sizes.padding_xs}px;
    }}
    
    QWidget[class="tag-input-container"]:focus {{
        border-color: {colors.primary};
    }}
    
    /* 通知徽章 */
    QLabel[class="notification-badge"] {{
        background-color: {colors.error};
        color: {colors.text_on_primary};
        border-radius: {sizes.radius_full}px;
        padding: 2px 6px;
        min-width: 18px;
        min-height: 18px;
        font-size: {fonts.size_xs}px;
        font-weight: {fonts.weight_bold};
        text-align: center;
    }}
    
    /* 空状态容器 */
    QWidget[class="empty-state"] {{
        background-color: transparent;
        padding: {sizes.padding_2xl}px;
    }}
    
    QWidget[class="empty-state"] QLabel {{
        color: {colors.text_secondary};
        text-align: center;
    }}
    
    /* 加载动画容器 */
    QWidget[class="loading-container"] {{
        background-color: transparent;
    }}
    
    /* 步骤指示器 */
    QWidget[class="step-indicator"] {{
        background-color: transparent;
    }}
    
    QWidget[class="step-indicator"] QLabel {{
        min-width: 32px;
        min-height: 32px;
        border-radius: {sizes.radius_full}px;
        background-color: {colors.border};
        color: {colors.text_secondary};
        font-weight: {fonts.weight_semibold};
    }}
    
    QWidget[class="step-indicator"][completed="true"] QLabel {{
        background-color: {colors.success};
        color: {colors.text_on_primary};
    }}
    
    QWidget[class="step-indicator"][active="true"] QLabel {{
        background-color: {colors.primary};
        color: {colors.text_on_primary};
    }}
    
    /* 卡片页眉 */
    QWidget[class="card-header"] {{
        background-color: transparent;
        border-bottom: 1px solid {colors.border};
        padding-bottom: {sizes.padding_md}px;
        margin-bottom: {sizes.padding_md}px;
    }}
    
    /* 卡片内容 */
    QWidget[class="card-content"] {{
        background-color: transparent;
    }}
    
    /* 卡片页脚 */
    QWidget[class="card-footer"] {{
        background-color: transparent;
        border-top: 1px solid {colors.border};
        padding-top: {sizes.padding_md}px;
        margin-top: {sizes.padding_md}px;
    }}
    """


# =============================================================================
# 响应式布局样式
# =============================================================================

def get_responsive_styles() -> str:
    """
    获取响应式布局样式表 - 适配不同屏幕尺寸
    
    Returns:
        包含响应式布局样式的字符串
    """
    colors = Theme.Colors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       响应式布局样式
       ========================================================================== */
    
    /* -------------------------------------------------------------------------
       移动端适配 (屏幕宽度 < 600px)
       移动设备通常有较小的屏幕，需要更大的触摸目标和更简单的布局
       ------------------------------------------------------------------------- */
    
    @media (max-width: {Theme.Breakpoints.MOBILE - 1}px) {{
        /* 移动端按钮样式 - 更大的触摸目标 */
        QPushButton {{
            min-height: {sizes.button_height_lg}px;
            padding: {sizes.padding_md}px {sizes.padding_lg}px;
            font-size: {fonts.size_md}px;
        }}
        
        /* 移动端输入框 */
        QLineEdit, QComboBox {{
            min-height: {sizes.input_height_lg}px;
            font-size: {fonts.size_md}px;
        }}
        
        /* 隐藏不必要的装饰 */
        QMenuBar {{
            /* 可以选择隐藏或简化为图标 */
        }}
        
        /* 调整标签页为可滚动 */
        QTabBar::tab {{
            min-width: 80px;
            padding: {sizes.padding_sm}px {sizes.padding_md}px;
        }}
        
        /* 增大列表项的触摸区域 */
        QListWidget::item, QListView::item,
        QTreeWidget::item, QTreeView::item {{
            min-height: 44px;
            padding: {sizes.padding_md}px;
        }}
    }}
    
    /* -------------------------------------------------------------------------
       平板适配 (屏幕宽度 600px - 1024px)
       平板设备可以使用双栏布局，但需要考虑横向和纵向模式
       ------------------------------------------------------------------------- */
    
    @media (min-width: {Theme.Breakpoints.MOBILE}px) and (max-width: {Theme.Breakpoints.TABLET - 1}px) {{
        /* 平板端按钮样式 */
        QPushButton {{
            min-height: {sizes.button_height_md}px;
        }}
        
        /* 平板端输入框 */
        QLineEdit, QComboBox {{
            min-height: {sizes.input_height_md}px;
        }}
        
        /* 标签页 */
        QTabBar::tab {{
            min-width: 100px;
        }}
    }}
    
    /* -------------------------------------------------------------------------
       桌面适配 (屏幕宽度 > 1024px)
       桌面设备可以使用完整的布局和所有功能
       ------------------------------------------------------------------------- */
    
    @media (min-width: {Theme.Breakpoints.TABLET}px) {{
        /* 桌面端保持默认样式 */
        /* 这里可以添加桌面端特有的样式优化 */
        
        /* 增大最大宽度以利用大屏幕空间 */
        QWidget[class="content"] {{
            max-width: 1200px;
        }}
        
        /* 侧边栏在大屏幕上可以更宽 */
        QWidget[class="sidebar"] {{
            min-width: 240px;
            max-width: 300px;
        }}
    }}
    
    /* -------------------------------------------------------------------------
       大桌面适配 (屏幕宽度 > 1440px)
       大屏幕设备可以显示更多内容
       ------------------------------------------------------------------------- */
    
    @media (min-width: {Theme.Breakpoints.DESKTOP}px) {{
        /* 增大内容区域最大宽度 */
        QWidget[class="content"] {{
            max-width: 1400px;
        }}
        
        /* 侧边栏可以更宽 */
        QWidget[class="sidebar"] {{
            min-width: 280px;
            max-width: 360px;
        }}
    }}
    
    /* -------------------------------------------------------------------------
       高 DPI 屏幕适配
       确保在高 DPI 屏幕上的清晰显示
       ------------------------------------------------------------------------- */
    
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
        /* 增大图标和按钮的精细度 */
        QPushButton[icon="true"] {{
            /* 图标按钮样式调整 */
        }}
    }}
    
    /* -------------------------------------------------------------------------
       深色模式响应式样式
       可以在响应式断点中调整深色模式的样式
       ------------------------------------------------------------------------- */
    
    QWidget[class="mobile-sidebar"] {{
        /* 移动端侧边栏默认隐藏 */
        /* 可以通过动画显示 */
    }}
    """


# =============================================================================
# 深色主题样式
# =============================================================================

def get_dark_theme_styles() -> str:
    """
    获取深色主题样式表
    
    Returns:
        包含深色主题样式的字符串
    """
    colors = Theme.DarkColors
    fonts = Theme.Fonts
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       深色主题样式
       ========================================================================== */
    
    /* 深色主题全局样式 */
    QMainWindow[class="dark"],
    QWidget[class="dark"] {{
        background-color: {colors.background};
        color: {colors.text_primary};
    }}
    
    /* 深色主题滚动条 */
    QMainWindow[class="dark"] QScrollBar:vertical ::handle:vertical,
    QWidget[class="dark"] QScrollBar::handle:vertical {{
        background-color: {colors.scrollbar};
    }}
    
    QMainWindow[class="dark"] QScrollBar::handle:vertical:hover,
    QWidget[class="dark"] QScrollBar::handle:vertical:hover {{
        background-color: {colors.scrollbar_hover};
    }}
    
    /* 深色主题按钮 */
    QMainWindow[class="dark"] QPushButton,
    QWidget[class="dark"] QPushButton {{
        background-color: {colors.primary};
        color: {colors.text_on_primary};
    }}
    
    QMainWindow[class="dark"] QPushButton:hover,
    QWidget[class="dark"] QPushButton:hover {{
        background-color: {colors.primary_hover};
    }}
    
    /* 深色主题输入框 */
    QMainWindow[class="dark"] QLineEdit,
    QWidget[class="dark"] QLineEdit {{
        background-color: {colors.surface};
        color: {colors.text_primary};
        border-color: {colors.border};
    }}
    
    QMainWindow[class="dark"] QLineEdit:focus,
    QWidget[class="dark"] QLineEdit:focus {{
        border-color: {colors.border_focus};
    }}
    
    /* 深色主题容器 */
    QMainWindow[class="dark"] QFrame[class="card"],
    QWidget[class="dark"] QFrame[class="card"] {{
        background-color: {colors.background_card};
        border-color: {colors.border};
    }}
    
    /* 深色主题工具栏 */
    QMainWindow[class="dark"] QToolBar,
    QWidget[class="dark"] QToolBar {{
        background-color: {colors.surface};
        border-color: {colors.border};
    }}
    
    /* 深色主题状态栏 */
    QMainWindow[class="dark"] QStatusBar,
    QWidget[class="dark"] QStatusBar {{
        background-color: {colors.surface};
        border-color: {colors.border};
        color: {colors.text_secondary};
    }}
    """


# =============================================================================
# 动画和过渡效果
# =============================================================================

def get_animation_styles() -> str:
    """
    获取动画样式表 - 包含过渡效果和动画定义
    
    Returns:
        包含动画样式的字符串
    """
    colors = Theme.Colors
    sizes = Theme.Sizes
    
    return f"""
    /* ==========================================================================
       动画和过渡效果
       ========================================================================== */
    
    /* 淡入淡出效果 - 可以通过 Qt 的 QPropertyAnimation 使用 */
    
    /* 悬停过渡效果 - 使用 transition 伪类 */
    QPushButton {{
        /* 属性动画 */
    }}
    
    /* 下拉菜单展开动画 */
    QComboBox QAbstractItemView {{
        /* 可以通过 QPropertyAnimation 设置展开动画 */
    }}
    
    /* 标签切换动画 */
    QTabWidget::pane {{
        /* 可以通过 QPropertyAnimation 设置标签切换动画 */
    }}
    
    /* 工具提示延迟显示 */
    QToolTip {{
        /* 延迟由 Qt 控制 */
    }}
    
    /* 进度条动画 */
    QProgressBar::chunk {{
        /*  indeterminate 模式下的动画 */
    }}
    """


# =============================================================================
# 完整的样式表获取
# =============================================================================

def get_complete_stylesheet(theme: str = "light") -> str:
    """
    获取完整的样式表
    
    Args:
        theme: 主题名称，"light" 或 "dark"
        
    Returns:
        包含完整样式的字符串
    """
    # 根据主题选择颜色配置
    if theme == "dark":
        Theme.Manager.set_theme("dark")
    else:
        Theme.Manager.set_theme("light")
    
    # 合并所有样式
    styles = [
        get_base_styles(),
        get_button_styles(),
        get_input_styles(),
        get_container_styles(),
        get_menu_dialog_styles(),
        get_list_tree_styles(),
        get_tab_panel_styles(),
        get_custom_styles(),
        get_responsive_styles(),
    ]
    
    return "\n".join(styles)


def get_dark_stylesheet() -> str:
    """
    获取深色主题完整样式表
    
    Returns:
        包含深色主题完整样式的字符串
    """
    # 获取亮色主题样式（包含深色主题特定样式）
    light_styles = get_complete_stylesheet("light")
    
    # 获取深色主题特定样式
    dark_specific = get_dark_theme_styles()
    
    return light_styles + "\n" + dark_specific


# =============================================================================
# 便捷函数
# =============================================================================

def get_stylesheet_for_widget(widget_type: str, theme: str = "light") -> str:
    """
    获取特定组件类型的样式表
    
    Args:
        widget_type: 组件类型名称，如 "button", "input", "container" 等
        theme: 主题名称，"light" 或 "dark"
        
    Returns:
        包含指定组件样式的字符串
    """
    if theme == "dark":
        Theme.Manager.set_theme("dark")
    else:
        Theme.Manager.set_theme("light")
    
    style_map = {
        "base": get_base_styles,
        "button": get_button_styles,
        "input": get_input_styles,
        "container": get_container_styles,
        "menu": get_menu_dialog_styles,
        "list": get_list_tree_styles,
        "tab": get_tab_panel_styles,
        "custom": get_custom_styles,
        "responsive": get_responsive_styles,
    }
    
    getter = style_map.get(widget_type.lower())
    if getter:
        return getter()
    return ""


# =============================================================================
# 样式表导出
# =============================================================================

# 默认导出的样式表
DEFAULT_STYLESHEET = get_complete_stylesheet("light")
DARK_STYLESHEET = get_dark_stylesheet()
