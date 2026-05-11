# -*- coding: utf-8 -*-
"""
UI 样式模块

提供应用程序的主题配置和 QSS 样式表。

子模块:
    - theme: 主题配置（颜色、字体、尺寸、断点）
    - qss: QSS 样式表（所有 PySide6 组件的样式）
"""

from .theme import (
    Colors,
    DarkColors,
    Fonts,
    Sizes,
    Breakpoints,
    ThemeManager,
    Theme,
)

from .qss import (
    get_complete_stylesheet,
    get_dark_stylesheet,
    get_stylesheet_for_widget,
    DEFAULT_STYLESHEET,
    DARK_STYLESHEET,
    get_base_styles,
    get_button_styles,
    get_input_styles,
    get_container_styles,
    get_menu_dialog_styles,
    get_list_tree_styles,
    get_tab_panel_styles,
    get_custom_styles,
    get_responsive_styles,
)

__all__ = [
    # 主题相关
    "Colors",
    "DarkColors",
    "Fonts",
    "Sizes",
    "Breakpoints",
    "ThemeManager",
    "Theme",
    # QSS 相关
    "get_complete_stylesheet",
    "get_dark_stylesheet",
    "get_stylesheet_for_widget",
    "DEFAULT_STYLESHEET",
    "DARK_STYLESHEET",
    # QSS 生成函数
    "get_base_styles",
    "get_button_styles",
    "get_input_styles",
    "get_container_styles",
    "get_menu_dialog_styles",
    "get_list_tree_styles",
    "get_tab_panel_styles",
    "get_custom_styles",
    "get_responsive_styles",
]
