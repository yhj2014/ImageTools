# -*- coding: utf-8 -*-
"""
主题配置文件 - 定义应用程序的颜色、字体、尺寸和断点配置

本模块提供统一的主题管理，确保整个应用程序的视觉风格一致性
"""

# =============================================================================
# 颜色配置
# =============================================================================

class Colors:
    """
    颜色配置类 - 定义应用程序使用的所有颜色值
    
    颜色遵循 Material Design 设计规范，提供良好的对比度和可访问性
    """
    
    # 主要颜色 - 用于主要按钮、链接、强调元素
    # 采用蓝色系，给人专业、可靠的感觉
    primary = "#2563EB"           # 主色调 - 蓝色，用于主要操作按钮和链接
    primary_hover = "#1D4ED8"      # 主色调悬停状态 - 深蓝色
    primary_light = "#3B82F6"     # 主色调浅色 - 浅蓝色，用于背景
    primary_dark = "#1E40AF"      # 主色调深色 - 深蓝色
    
    # 次要颜色 - 用于次要按钮、辅助元素
    # 采用紫色系，与主色形成对比但不冲突
    secondary = "#7C3AED"         # 次要色调 - 紫色
    secondary_hover = "#6D28D9"   # 次要色调悬停状态
    secondary_light = "#A78BFA"  # 次要色调浅色
    
    # 成功颜色 - 用于成功提示、操作完成
    success = "#059669"           # 成功色 - 绿色
    success_hover = "#047857"     # 成功色悬停状态
    success_light = "#10B981"     # 成功色浅色
    
    # 警告颜色 - 用于警告提示、需要用户注意
    warning = "#D97706"           # 警告色 - 橙色
    warning_hover = "#B45309"     # 警告色悬停状态
    warning_light = "#F59E0B"     # 警告色浅色
    
    # 错误颜色 - 用于错误提示、操作失败
    error = "#DC2626"             # 错误色 - 红色
    error_hover = "#B91C1C"       # 错误色悬停状态
    error_light = "#EF4444"       # 错误色浅色
    
    # 信息颜色 - 用于信息提示、一般性信息
    info = "#0891B2"              # 信息色 - 青色
    info_hover = "#0E7490"        # 信息色悬停状态
    
    # 背景颜色 - 页面和组件的背景色
    background = "#F8FAFC"        # 页面背景 - 浅灰色
    background_dark = "#F1F5F9"   # 深色背景 - 用于卡片、分区
    background_card = "#FFFFFF"   # 卡片背景 - 纯白色
    
    # 表面颜色 - 覆盖层、对话框、下拉菜单
    surface = "#FFFFFF"           # 表面层 - 纯白色
    surface_elevated = "#FFFFFF"   # 提升表面 - 有阴影的表面
    
    # 文本颜色
    text_primary = "#1E293B"      # 主要文本 - 深灰，几乎为黑色
    text_secondary = "#64748B"   # 次要文本 - 中灰色
    text_tertiary = "#94A3B8"    # 第三文本 - 浅灰色，用于占位符
    text_on_primary = "#FFFFFF"  # 主色上的文本 - 白色
    text_disabled = "#CBD5E1"     # 禁用文本 - 非常浅的灰色
    
    # 边框颜色
    border = "#E2E8F0"            # 默认边框 - 浅灰色
    border_hover = "#CBD5E1"      # 边框悬停状态
    border_focus = "#2563EB"     # 聚焦边框 - 主色
    border_disabled = "#F1F5F9"   # 禁用边框
    
    # 分隔线颜色
    divider = "#E2E8F0"          # 分隔线 - 与边框同色
    
    # 阴影颜色
    shadow = "rgba(0, 0, 0, 0.1)"    # 默认阴影
    shadow_strong = "rgba(0, 0, 0, 0.15)"  # 强阴影
    shadow_primary = "rgba(37, 99, 235, 0.2)"  # 主色阴影
    
    # 遮罩颜色 - 用于模态框背景
    overlay = "rgba(0, 0, 0, 0.5)"
    
    # 滚动条颜色
    scrollbar = "#CBD5E1"        # 滚动条轨道
    scrollbar_hover = "#94A3B8"  # 滚动条悬停


class DarkColors:
    """
    深色主题颜色配置类
    
    适用于深色模式，提供舒适的暗色视觉体验
    """
    
    # 主要颜色 - 在深色背景下调整
    primary = "#3B82F6"          # 主色调 - 亮蓝色
    primary_hover = "#60A5FA"    # 主色调悬停状态
    primary_light = "#2563EB"    # 主色调浅色
    primary_dark = "#1D4ED8"     # 主色调深色
    
    # 次要颜色
    secondary = "#8B5CF6"        # 紫色
    secondary_hover = "#A78BFA"
    
    # 成功颜色
    success = "#10B981"          # 绿色
    success_hover = "#34D399"
    
    # 警告颜色
    warning = "#FBBF24"          # 橙色（浅色以适应深色背景）
    warning_hover = "#F59E0B"
    
    # 错误颜色
    error = "#EF4444"            # 红色
    error_hover = "#F87171"
    
    # 信息颜色
    info = "#06B6D4"             # 青色
    info_hover = "#22D3EE"
    
    # 背景颜色 - 深色主题使用深色背景
    background = "#0F172A"       # 页面背景 - 深蓝黑色
    background_dark = "#1E293B"  # 深色背景 - 用于卡片、分区
    background_card = "#1E293B"  # 卡片背景
    
    # 表面颜色
    surface = "#1E293B"          # 表面层
    surface_elevated = "#334155" # 提升表面
    
    # 文本颜色
    text_primary = "#F8FAFC"     # 主要文本 - 白色
    text_secondary = "#94A3B8"   # 次要文本 - 灰色
    text_tertiary = "#64748B"    # 第三文本
    text_on_primary = "#FFFFFF"  # 主色上的文本
    text_disabled = "#475569"    # 禁用文本
    
    # 边框颜色 - 在深色主题中边框也更深
    border = "#334155"           # 默认边框
    border_hover = "#475569"     # 边框悬停状态
    border_focus = "#3B82F6"     # 聚焦边框
    border_disabled = "#1E293B"  # 禁用边框
    
    # 分隔线颜色
    divider = "#334155"
    
    # 阴影颜色 - 深色主题阴影更微妙
    shadow = "rgba(0, 0, 0, 0.3)"
    shadow_strong = "rgba(0, 0, 0, 0.5)"
    shadow_primary = "rgba(59, 130, 246, 0.3)"
    
    # 遮罩颜色
    overlay = "rgba(0, 0, 0, 0.7)"
    
    # 滚动条颜色
    scrollbar = "#475569"
    scrollbar_hover = "#64748B"


# =============================================================================
# 字体配置
# =============================================================================

class Fonts:
    """
    字体配置类 - 定义应用程序使用的字体
    
    字体栈确保在不同操作系统上都有良好的显示效果
    Windows 优先使用微软雅黑，Mac 优先使用苹方，Linux 使用思源黑体
    """
    
    # 主字体栈 - 用于大多数文本
    # 按优先级排列，确保在各平台都有合适的字体显示
    primary = (
        "Microsoft YaHei UI",    # Windows 微软雅黑
        "PingFang SC",           # macOS 苹方
        "Source Han Sans CN",    # Linux 思源黑体简体中文
        "Noto Sans CJK SC",      # 备选思源黑体
        "Segoe UI",              # Windows 英文
        "SF Pro Display",        # macOS 英文
        "-apple-system",         # macOS 系统字体
        "sans-serif"             # 最终备选
    )
    
    # 等宽字体栈 - 用于代码、数字、路径等
    mono = (
        "JetBrains Mono",        # JetBrains 出品的高质量编程字体
        "Cascadia Code",         # Windows Cascadia
        "Fira Code",             # Fira 编程字体
        "Source Code Pro",       # Adobe 源代码字体
        "Consolas",              # Windows 控制台字体
        "Monaco",                # macOS 等宽字体
        "Courier New",           # 备选
        "monospace"
    )
    
    # 字体大小定义（单位：px）
    # 提供从超小到超大的完整尺寸范围
    size_xxs = 10    # 超小 - 用于非常次要的信息
    size_xs = 11     # 极小 - 标签、徽章
    size_sm = 12     # 小 - 次要文本、辅助说明
    size_base = 13   # 基础 - 正文文本
    size_md = 14     # 中等 - 稍大的正文
    size_lg = 16     # 大 - 标题、按钮文字
    size_xl = 18     # 特大 - 页面标题
    size_xxl = 20    # 超大 - 主标题
    size_xxxl = 24   # 超超大 - 大标题
    
    # 字体粗细
    weight_thin = 100
    weight_light = 300
    weight_normal = 400
    weight_medium = 500
    weight_semibold = 600
    weight_bold = 700
    weight_extrabold = 800
    weight_black = 900
    
    # 行高 - 控制文本行之间的垂直间距
    line_height_tight = 1.2    # 紧凑行高 - 用于标题
    line_height_normal = 1.5   # 正常行高 - 用于正文
    line_height_relaxed = 1.8  # 宽松行高 - 用于需要更好可读性的文本
    
    # 字间距
    letter_spacing_tight = -0.5    # 紧凑字间距 - 用于大标题
    letter_spacing_normal = 0       # 正常字间距
    letter_spacing_wide = 0.5       # 宽松字间距 - 用于大写文本


# =============================================================================
# 尺寸配置
# =============================================================================

class Sizes:
    """
    尺寸配置类 - 定义应用程序使用的各种尺寸值
    
    尺寸值基于 4px 网格系统，确保元素之间有良好的视觉节奏感
    """
    
    # 边框圆角
    # 圆角大小影响整体视觉风格：越小越现代，越大越圆润
    radius_none = 0            # 无圆角 - 用于需要方正感的元素
    radius_xs = 2              # 超小圆角
    radius_sm = 4              # 小圆角 - 用于小按钮、输入框
    radius_md = 6              # 中等圆角 - 用于按钮、卡片
    radius_lg = 8              # 大圆角 - 用于模态框、大卡片
    radius_xl = 12             # 特大圆角
    radius_2xl = 16            # 超大圆角
    radius_full = 9999         # 全圆角 - 用于圆形按钮、头像
    
    # 间距 - 基于 4px 网格
    space_0 = 0
    space_1 = 4                 # 1 单位 - 紧凑间距
    space_2 = 8                 # 2 单位 - 元素内部
    space_3 = 12                # 3 单位 - 相关元素间
    space_4 = 16                # 4 单位 - 标准间距
    space_5 = 20                # 5 单位
    space_6 = 24                # 6 单位 - 分组间
    space_8 = 32                # 8 单位 - 大间距
    space_10 = 40               # 10 单位
    space_12 = 48               # 12 单位 - 区块间
    space_16 = 64               # 16 单位 - 大区块
    
    # 内边距
    padding_xs = 4             # 超小内边距
    padding_sm = 8             # 小内边距
    padding_md = 12            # 中等内边距
    padding_lg = 16            # 大内边距
    padding_xl = 20            # 特大内边距
    padding_2xl = 24           # 超大内边距
    
    # 外边距
    margin_xs = 4
    margin_sm = 8
    margin_md = 12
    margin_lg = 16
    margin_xl = 20
    margin_2xl = 24
    
    # 图标尺寸
    icon_xs = 12                # 超小图标
    icon_sm = 16                # 小图标
    icon_md = 20                # 中等图标
    icon_lg = 24                # 大图标
    icon_xl = 32                # 特大图标
    icon_2xl = 48               # 超大图标
    
    # 按钮尺寸
    button_height_sm = 28      # 小按钮高度
    button_height_md = 36      # 中等按钮高度
    button_height_lg = 44       # 大按钮高度
    button_height_xl = 52      # 特大按钮高度
    
    button_padding_horizontal_sm = 12   # 小按钮水平内边距
    button_padding_horizontal_md = 16   # 中等按钮水平内边距
    button_padding_horizontal_lg = 20   # 大按钮水平内边距
    
    # 输入框尺寸
    input_height_sm = 28       # 小输入框高度
    input_height_md = 36       # 中等输入框高度
    input_height_lg = 44       # 大输入框高度
    
    # 边框宽度
    border_width_none = 0
    border_width_thin = 1       # 细边框
    border_width_medium = 2     # 中等边框
    border_width_thick = 3      # 粗边框
    
    # 阴影级别
    shadow_sm = "0 1px 2px rgba(0, 0, 0, 0.05)"           # 小阴影
    shadow_md = "0 4px 6px rgba(0, 0, 0, 0.1)"           # 中等阴影
    shadow_lg = "0 10px 15px rgba(0, 0, 0, 0.1)"         # 大阴影
    shadow_xl = "0 20px 25px rgba(0, 0, 0, 0.15)"        # 特大阴影
    shadow_2xl = "0 25px 50px rgba(0, 0, 0, 0.25)"       # 超大阴影
    
    # Z-index 层级 - 确保正确的堆叠顺序
    z_dropdown = 100            # 下拉菜单
    z_sticky = 200              # 粘性元素
    z_fixed = 300               # 固定元素
    z_modal_backdrop = 400      # 模态框背景
    z_modal = 500               # 模态框
    z_popover = 600            # 弹出框
    z_tooltip = 700            # 工具提示
    z_toast = 800              # 吐司通知


# =============================================================================
# 断点配置 - 用于响应式设计
# =============================================================================

class Breakpoints:
    """
    断点配置类 - 定义响应式设计的尺寸断点
    
    断点将屏幕宽度分为不同的范围，每个范围可以应用不同的样式
    设计遵循移动优先原则
    """
    
    # 移动端 - 手机竖屏
    # 屏幕宽度小于 600px
    MOBILE = 600
    
    # 平板设备 - 手机横屏、平板竖屏
    # 屏幕宽度 600px - 1024px
    TABLET = 1024
    
    # 桌面设备 - 普通显示器
    # 屏幕宽度大于 1024px
    DESKTOP = 1440
    
    # 大桌面设备 - 大型显示器
    # 屏幕宽度大于 1440px
    LARGE_DESKTOP = 1920
    
    # 断点范围的名称
    RANGE_MOBILE = "mobile"         # 移动端
    RANGE_TABLET = "tablet"         # 平板
    RANGE_DESKTOP = "desktop"       # 桌面
    RANGE_LARGE_DESKTOP = "large"   # 大桌面
    
    @classmethod
    def get_range(cls, width: int) -> str:
        """
        根据宽度获取断点范围名称
        
        Args:
            width: 屏幕宽度（像素）
            
        Returns:
            断点范围名称字符串
        """
        if width < cls.MOBILE:
            return cls.RANGE_MOBILE
        elif width < cls.TABLET:
            return cls.RANGE_TABLET
        elif width < cls.DESKTOP:
            return cls.RANGE_DESKTOP
        else:
            return cls.RANGE_LARGE_DESKTOP
    
    @classmethod
    def is_mobile(cls, width: int) -> bool:
        """判断是否为移动端"""
        return width < cls.MOBILE
    
    @classmethod
    def is_tablet(cls, width: int) -> bool:
        """判断是否为平板设备"""
        return cls.MOBILE <= width < cls.TABLET
    
    @classmethod
    def is_desktop(cls, width: int) -> bool:
        """判断是否为桌面设备"""
        return width >= cls.TABLET
    
    @classmethod
    def is_large_desktop(cls, width: int) -> bool:
        """判断是否为大型桌面设备"""
        return width >= cls.DESKTOP


# =============================================================================
# 主题管理器
# =============================================================================

class ThemeManager:
    """
    主题管理器 - 管理亮色和暗色主题的切换
    
    提供统一的主题访问接口，支持动态切换主题
    """
    
    _current_theme = "light"  # 当前主题：light 或 dark
    _colors = Colors         # 当前使用的颜色类
    
    @classmethod
    def set_theme(cls, theme: str) -> None:
        """
        设置当前主题
        
        Args:
            theme: 主题名称，"light" 或 "dark"
        """
        if theme == "dark":
            cls._current_theme = "dark"
            cls._colors = DarkColors
        else:
            cls._current_theme = "light"
            cls._colors = Colors
    
    @classmethod
    def get_theme(cls) -> str:
        """获取当前主题名称"""
        return cls._current_theme
    
    @classmethod
    def get_colors(cls) -> type:
        """获取当前主题的颜色配置类"""
        return cls._colors
    
    @classmethod
    def is_dark(cls) -> bool:
        """判断当前是否为深色主题"""
        return cls._current_theme == "dark"
    
    @classmethod
    def is_light(cls) -> bool:
        """判断当前是否为浅色主题"""
        return cls._current_theme == "light"


# 导出便捷访问
# 允许直接通过 theme.Colors 访问颜色，而不是 theme.Colors.Colors
Theme = type('Theme', (), {
    'Colors': Colors,
    'DarkColors': DarkColors,
    'Fonts': Fonts,
    'Sizes': Sizes,
    'Breakpoints': Breakpoints,
    'Manager': ThemeManager
})
