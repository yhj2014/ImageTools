# ImageForge - 专业图像处理工具规格说明

## 一、项目概述

**项目名称**: ImageForge (图像锻造工坊)
**项目类型**: 跨平台桌面/移动端图像处理应用
**核心功能**: 批量图像处理工具箱，支持格式转换、裁剪、水印、滤镜、批量重命名等
**目标用户**: 设计师、摄影师、内容创作者、电商从业者等需要频繁处理图像的人群

## 二、核心功能需求

### 2.1 图像格式转换
- **输入格式**: PNG, JPG/JPEG, WEBP, BMP, TIFF, GIF, TGA, PSD, EXR, HDR, DDS, SVG
- **输出格式**: PNG, JPG/JPEG, WEBP, BMP, TIFF, GIF, TGA
- **质量控制**: 1-100% 可调质量滑块
- **元数据处理**: 可选保留/删除 EXIF 信息

### 2.2 图片裁剪
- **预设比例**: 1:1, 4:3, 16:9, 3:2, 2:3, 9:16 (移动端竖屏)
- **自定义尺寸**: 宽度 × 高度输入
- **自由裁剪**: 拖拽裁剪区域
- **智能裁剪**: 自动主体检测裁剪 (基于 Pillow)

### 2.3 批量水印
- **文字水印**:
  - 自定义文本内容
  - 字体选择 (系统字体)
  - 字号、颜色、透明度
  - 旋转角度
  - 位置: 九宫格 (左上/中上/右上/左中/居中/右中/左下/中下/右下) + 自定义坐标
- **图片水印**:
  - 支持 PNG 透明水印
  - 透明度控制
  - 缩放比例
  - 位置控制
- **平铺水印**: 全图平铺模式

### 2.4 图片缩放
- **预设尺寸**: 缩放到 800×600, 1024×768, 1920×1080, 4K
- **自定义尺寸**: 宽度/高度输入
- **等比缩放**: 保持宽高比
- **缩放算法**: 最近邻、双线性、双三次、Lanczos

### 2.5 图片旋转与翻转
- **固定旋转**: 90°/180°/270°
- **自定义旋转**: -180° 到 +180°
- **水平翻转**: 左右镜像
- **垂直翻转**: 上下镜像
- **自动旋转**: 根据 EXIF 方向信息

### 2.6 图像滤镜
- **亮度调整**: -100 到 +100
- **对比度调整**: -100 到 +100
- **饱和度调整**: -100 到 +100
- **灰度转换**: 灰度、黑白
- **模糊效果**: 高斯模糊 (1-20 半径)
- **锐化效果**: USM 锐化
- **噪点效果**: 添加噪点

### 2.7 GIF 制作
- **多图合成 GIF**: 支持多张图片合成动画
- **帧延迟设置**: 每帧延迟时间 (毫秒)
- **循环次数**: 无限循环 / 指定次数
- **尺寸调整**: 缩放到指定尺寸

### 2.8 批量重命名
- **命名模板**:
  - `{name}` - 原文件名
  - `{date}` - 日期
  - `{index}` - 序号
  - `{time}` - 时间
- **前缀/后缀**: 自定义添加
- **序号格式**: 001, 002 或 1, 2

### 2.9 PDF 转换
- **图片转 PDF**: 单张或多张合成 PDF
- **页面布局**: 单张单页 / 多张单页 / 2×2, 3×3 网格

## 三、技术架构

### 3.1 项目结构 (src 目录)
```
image_forge/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 入口点
│   ├── app.py                  # 应用主类
│   ├── core/                   # 核心模块
│   │   ├── __init__.py
│   │   ├── ffmpeg_manager.py   # FFmpeg 下载和管理
│   │   ├── converter.py        # 格式转换
│   │   ├── processor.py        # 图像处理引擎
│   │   ├── worker.py           # 多线程工作器
│   │   └── presets.py          # 预设配置
│   ├── features/               # 功能模块
│   │   ├── __init__.py
│   │   ├── crop.py             # 裁剪功能
│   │   ├── watermark.py        # 水印功能
│   │   ├── resize.py           # 缩放功能
│   │   ├── rotate.py           # 旋转翻转
│   │   ├── filter.py           # 滤镜效果
│   │   ├── gif_maker.py        # GIF 制作
│   │   ├── rename.py           # 批量重命名
│   │   └── pdf_converter.py    # PDF 转换
│   ├── ui/                     # UI 模块
│   │   ├── __init__.py
│   │   ├── main_window.py      # 主窗口
│   │   ├── widgets/            # 自定义组件
│   │   │   ├── __init__.py
│   │   │   ├── file_list.py    # 文件列表组件
│   │   │   ├── preview.py      # 预览组件
│   │   │   ├── slider.py       # 滑块组件
│   │   │   └── tabs.py         # 功能标签页
│   │   └── styles/             # 样式
│   │       ├── __init__.py
│   │       ├── theme.py        # 主题配置
│   │       └── qss.py          # QSS 样式表
│   └── utils/                  # 工具模块
│       ├── __init__.py
│       ├── logger.py           # 日志
│       ├── config.py           # 配置管理
│       └── helpers.py          # 辅助函数
├── pyproject.toml              # UV 项目配置
└── README.md
```

### 3.2 技术栈
- **GUI**: PySide6 (Qt for Python) - 跨平台支持
- **图像处理**: Pillow (PIL Fork) + FFmpeg
- **并发**: ThreadPoolExecutor + QThread
- **项目管理**: Python UV
- **打包**: PyInstaller / Nuitka
- **UI 适配**: PySide6 响应式布局 + 断点系统

### 3.3 FFmpeg 自包含方案
```python
class FFmpegManager:
    # 下载源: GitHub releases 或官方静态构建
    FFmpeg_URLS = {
        "windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
        "macos": "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip",
        "linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64.tar.xz"
    }

    def download_if_needed(self) -> Path: ...
    def get_path(self) -> str: ...
```

### 3.4 移动端适配
- **响应式布局**: 基于 QLayout 动态调整
- **断点系统**:
  - 移动端: < 600px (垂直布局)
  - 平板: 600-1024px (混合布局)
  - 桌面: > 1024px (标准布局)
- **手势支持**: 拖拽、捏合缩放
- **触摸优化**: 更大的点击区域

## 四、界面设计

### 4.1 布局结构 (全中文界面)
```
┌──────────────────────────────────────────────────────────┐
│  标题栏 (ImageForge Logo + 窗口控制)                       │
├────────────┬─────────────────────────────────────────────┤
│            │                                             │
│  侧边栏     │   主工作区                                   │
│  ────────  │   ─────────                                  │
│  📁 文件    │   [文件列表 / 预览 / 设置面板]                 │
│  ✂️ 裁剪    │                                             │
│  💧 水印    │                                             │
│  📐 缩放    │                                             │
│  🔄 旋转    │                                             │
│  🎨 滤镜    │                                             │
│  🎬 GIF    │                                             │
│  📝 重命名  │                                             │
│  📄 PDF    │                                             │
│  ────────  │                                             │
│  ⚙️ 设置    │                                             │
│            │                                             │
├────────────┴─────────────────────────────────────────────┤
│  底部状态栏 (进度条 + 日志 + 状态信息)                       │
└──────────────────────────────────────────────────────────┘
```

### 4.2 配色方案
```python
THEME = {
    "primary": "#2196F3",      # 主色 - 蓝色
    "secondary": "#FFC107",    # 辅助色 - 琥珀色
    "success": "#4CAF50",      # 成功色 - 绿色
    "warning": "#FF9800",      # 警告色 - 橙色
    "error": "#F44336",        # 错误色 - 红色
    "background": "#FAFAFA",   # 背景色
    "surface": "#FFFFFF",      # 表面色
    "text_primary": "#212121",  # 主文字
    "text_secondary": "#757575",# 次文字
    "border": "#E0E0E0"        # 边框色
}
```

## 五、模块接口设计

### 5.1 FFmpegManager
```python
class FFmpegManager:
    def download_if_needed(self) -> tuple[bool, str]
    def check_update(self) -> bool
    def get_path(self) -> str
    def get_version(self) -> str
    def execute(self, cmd: list) -> tuple[int, str, str]
```

### 5.2 ImageProcessor
```python
class ImageProcessor:
    def convert(input: Path, output: Path, fmt: str, quality: int) -> bool
    def crop(image: Image, box: tuple) -> Image
    def add_watermark(image: Image, watermark: Image, position: str) -> Image
    def resize(image: Image, size: tuple, mode: str) -> Image
    def rotate(image: Image, angle: float) -> Image
    def apply_filter(image: Image, filter_type: str, params: dict) -> Image
```

### 5.3 TaskWorker
```python
class TaskWorker(QObject):
    progress = Signal(int, int, str)
    log = Signal(str, str)
    finished = Signal(bool, int, int)
    error = Signal(str)

    def start(self, tasks: list[Task]) -> None
    def cancel(self) -> None
    def pause(self) -> None
    def resume(self) -> None
```

## 六、用户体验

### 6.1 工作流程
1. **添加文件**: 拖拽/点击/快捷键 (Ctrl+O)
2. **选择功能**: 点击侧边栏功能项
3. **配置参数**: 调整各项设置
4. **预览效果**: 实时预览 (可选)
5. **开始处理**: 点击执行按钮
6. **查看结果**: 进度显示 + 日志 + 打开输出目录

### 6.2 快捷键
- `Ctrl+O`: 打开文件
- `Ctrl+Shift+O`: 打开文件夹
- `Ctrl+S`: 开始转换
- `Ctrl+,`: 设置
- `Delete`: 删除选中文件
- `Ctrl+A`: 全选
- `Ctrl+Z`: 撤销

### 6.3 错误处理
- 文件不存在: 提示并跳过
- 格式不支持: 显示警告
- 磁盘空间不足: 预检测 + 警告
- FFmpeg 下载失败: 重试机制 + 手动下载指引
- 处理失败: 记录错误 + 继续处理其他文件

## 七、扩展功能 (未来版本)

- **批量处理预设**: 保存/加载处理配置
- **处理队列**: 管理多个处理任务
- **历史记录**: 查看处理历史
- **云同步**: 同步设置和预设到云端
- **插件系统**: 支持第三方插件扩展

## 八、验收标准

### 8.1 功能验收
- [ ] 可以添加单个/多个图像文件
- [ ] 可以拖拽添加文件
- [ ] 可以添加整个文件夹
- [ ] 支持所有声明的输入/输出格式
- [ ] 格式转换正常工作
- [ ] 裁剪功能正常工作
- [ ] 水印功能正常工作 (文字 + 图片)
- [ ] 缩放功能正常工作
- [ ] 旋转翻转功能正常工作
- [ ] 滤镜功能正常工作
- [ ] GIF 制作功能正常工作
- [ ] 批量重命名功能正常工作
- [ ] PDF 转换功能正常工作

### 8.2 技术验收
- [ ] FFmpeg 自动下载安装
- [ ] UI 响应式适配移动端
- [ ] 多线程处理不阻塞 UI
- [ ] 错误处理完善
- [ ] 日志记录完整
- [ ] 内存使用合理

### 8.3 性能验收
- [ ] 启动时间 < 3 秒
- [ ] UI 流畅不卡顿
- [ ] 批量处理性能优良
- [ ] 内存占用合理 (< 500MB)
