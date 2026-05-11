# ImageForge

专业图像批量处理工具 - 基于 PySide6 + FFmpeg + Pillow

## 功能特性

### 🖼️ 格式转换
- 支持格式: PNG, JPG/JPEG, WEBP, BMP, TIFF, GIF, TGA
- 质量控制: 1-100% 可调
- 批量转换: 支持多文件同时处理

### ✂️ 图片裁剪
- 预设比例: 1:1, 4:3, 16:9, 3:2, 2:3, 9:16
- 自定义尺寸: 自由输入宽高
- 位置选择: 九宫格定位

### 💧 批量水印
- **文字水印**: 字体、字号、颜色、透明度、旋转
- **图片水印**: PNG透明水印、缩放、透明度
- **平铺模式**: 全图平铺水印

### 📐 图片缩放
- 预设尺寸: 800×600, 1024×768, 1920×1080, 4K
- 自定义尺寸: 自由设置
- 等比缩放: 保持宽高比
- 缩放算法: 最近邻、双线性、双三次、Lanczos

### 🔄 旋转翻转
- 固定旋转: 90°/180°/270°
- 自定义角度: -180° 到 +180°
- 水平/垂直翻转

### 🎨 图像滤镜
- 亮度调整: -100 到 +100
- 对比度调整: -100 到 +100
- 饱和度调整: -100 到 +100
- 灰度转换
- 高斯模糊: 1-20 半径
- 锐化效果

### 🎬 GIF 制作
- 多图合成GIF
- 帧延迟设置
- 循环次数控制

### 📝 批量重命名
- 模板变量: `{name}`, `{date}`, `{index}`, `{time}`
- 前缀/后缀添加
- 序号格式自定义

### 📄 PDF 转换
- 图片转PDF
- 单张单页/多张单页
- 2×2, 3×3 网格布局

## 技术架构

- **GUI框架**: PySide6 (Qt for Python)
- **图像处理**: Pillow (PIL Fork) + FFmpeg
- **并发处理**: ThreadPoolExecutor
- **项目管理**: Python UV

## 项目结构

```
├── pyproject.toml          # UV 项目配置
├── src/
│   ├── main.py             # 应用入口
│   ├── app.py              # 应用主类
│   ├── core/               # 核心模块
│   │   ├── ffmpeg_manager.py   # FFmpeg 下载管理
│   │   ├── converter.py         # 格式转换
│   │   ├── processor.py         # 图像处理引擎
│   │   ├── worker.py           # 多线程工作器
│   │   └── presets.py          # 预设配置
│   ├── features/           # 功能模块
│   │   ├── crop.py             # 裁剪功能
│   │   ├── watermark.py        # 水印功能
│   │   ├── resize.py           # 缩放功能
│   │   ├── rotate.py           # 旋转翻转
│   │   ├── filter.py           # 滤镜效果
│   │   ├── gif_maker.py        # GIF 制作
│   │   ├── rename.py           # 批量重命名
│   │   └── pdf_converter.py    # PDF 转换
│   ├── ui/                 # UI 模块
│   │   ├── main_window.py      # 主窗口
│   │   ├── widgets/            # 自定义组件
│   │   └── styles/             # 样式配置
│   └── utils/               # 工具模块
│       ├── logger.py           # 日志系统
│       ├── config.py           # 配置管理
│       └── helpers.py          # 辅助函数
└── README.md
```

## 安装与运行

### 环境要求

- Python 3.10+
- FFmpeg (程序会自动下载)

### 安装依赖

```bash
# 使用 UV (推荐)
uv sync

# 或使用 pip
pip install PySide6 Pillow requests
```

### 运行程序

```bash
# 使用 UV
uv run python -m src.main

# 或直接运行
python -m src.main
```

### 打包为可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --name ImageForge --onefile --windowed src/main.py
```

## 使用说明

1. **添加文件**: 点击"添加文件"或直接拖拽图片到文件列表
2. **选择功能**: 在侧边栏选择要使用的功能 (格式转换/裁剪/水印等)
3. **配置参数**: 根据需要调整各项参数
4. **开始处理**: 点击"开始处理"按钮
5. **查看结果**: 处理完成后可打开输出目录查看

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+O | 打开文件 |
| Ctrl+Shift+O | 打开文件夹 |
| Ctrl+S | 开始处理 |
| Delete | 删除选中文件 |
| Ctrl+A | 全选 |

## License

MIT License
