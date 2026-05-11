# ImageProcessor 增强版规格说明书

## Why
当前批量图像处理工具仅支持基础格式转换，缺乏高级图像处理功能。用户需要更丰富的功能如裁剪、水印、缩放等，同时要求：
1. 消除对外部 FFmpeg 依赖，实现自包含
2. 使用 Python UV 进行现代化项目管理
3. 支持移动端响应式布局

## What Changes

### 新增核心功能
- **图片裁剪**: 支持自定义裁剪区域、预设比例裁剪（1:1、4:3、16:9 等）
- **批量水印**: 文字水印、图片水印、位置控制、透明度调整
- **图片缩放**: 按比例/尺寸缩放、保持/忽略宽高比
- **批量重命名**: 支持模板变量（序号、日期、原文件名等）
- **格式压缩**: JPEG/PNG 压缩级别控制
- **批量旋转**: 90°/180°/270° 旋转、自定义角度
- **元数据处理**: EXIF 信息保留/剥离、创建时间设置

### 架构变更
- **FFmpeg 自包含**: 使用 `imageio-ffmpeg` 或编译版 FFmpeg二进制
- **项目管理**: 从 pip 迁移到 Python UV
- **UI 响应式**: 移动端适配，支持触屏操作

### 界面重构
- 从单一窗口改为多标签页布局
- 添加操作历史/撤销功能
- 增加处理预览功能

## Impact

### 受影响的规格
- 原规格: 基础格式转换 → 扩展为全功能图像处理套件

### 受影响的代码
- `core/converter.py` → 扩展图像处理引擎
- `core/worker.py` → 新增任务队列管理
- `ui/main_window.py` → 全新多标签 UI
- `main.py` → 入口重构
- `requirements.txt` → 新增依赖

## ADDED Requirements

### Requirement: 图片裁剪功能
系统应提供灵活的图像裁剪能力，支持多种裁剪模式。

#### Scenario: 预设比例裁剪
- **WHEN** 用户选择"1:1 方形裁剪"并应用
- **THEN** 所有图片按 1:1 比例从中心裁剪

#### Scenario: 自定义区域裁剪
- **WHEN** 用户在预览图上手动框选裁剪区域
- **THEN** 系统记录裁剪坐标并应用到所有图片

### Requirement: 水印功能
系统应支持添加文字和图片水印。

#### Scenario: 文字水印
- **WHEN** 用户输入"© 2024 Demo"并设置位置为右下角
- **THEN** 所有处理后的图片右下角显示该文字水印

#### Scenario: 图片水印
- **WHEN** 用户选择 logo.png 并设置透明度 50%
- **THEN** 所有图片叠加该 logo 水印

### Requirement: 自包含 FFmpeg
系统应内置 FFmpeg，无需用户手动安装。

#### Scenario: 首次启动
- **WHEN** 用户首次启动程序
- **THEN** 系统自动检测/下载 FFmpeg 二进制文件到用户数据目录

### Requirement: 移动端适配
系统应在移动设备上提供可用体验。

#### Scenario: 手机访问
- **WHEN** 用户在手机浏览器打开应用
- **THEN** 布局自动调整为单列模式，触控区域放大

## MODIFIED Requirements

### Requirement: 格式转换
**原版**: 仅支持 PNG、JPG、WEBP 等基础格式  
**新版**: 支持所有常见格式，增加质量/压缩级别控制

### Requirement: 批量处理
**原版**: 直接处理所有文件  
**新版**: 支持任务队列、预览确认、分批处理

## REMOVED Requirements

### Requirement: 外部 FFmpeg 依赖
**Reason**: 用户安装门槛过高，不符合开箱即用原则  
**Migration**: 迁移到内置 FFmpeg 二进制库

## Technical Architecture

### 项目结构
```
image_processor/
├── pyproject.toml              # UV 项目配置
├── src/
│   └── image_processor/
│       ├── __init__.py
│       ├── main.py             # 入口
│       ├── ffmpeg_core.py      # 内置 FFmpeg 封装
│       ├── engine.py           # 图像处理引擎
│       ├── worker.py           # 多线程工作器
│       └── utils/
│           ├── logger.py
│           └── config.py
├── ui/
│   ├── main_window.py          # 主窗口
│   ├── pages/
│   │   ├── convert_page.py     # 转换页
│   │   ├── crop_page.py        # 裁剪页
│   │   ├── watermark_page.py   # 水印页
│   │   └── resize_page.py      # 缩放页
│   └── components/
│       ├── file_list.py
│       ├── preview.py
│       └── progress.py
├── assets/
│   └── ffmpeg/                 # 内置 FFmpeg
└── tests/
```

### 技术选型
- **FFmpeg**: imageio-ffmpeg (Python 包自带二进制)
- **UI**: PySide6 + QSS 自定义样式
- **响应式**: Qt Layout 响应式设计
- **项目管理**: UV (替代 pip)

### 关键依赖
```toml
[project]
dependencies = [
    "PySide6>=6.5.0",
    "imageio-ffmpeg>=0.4.0",
    "Pillow>=10.0.0",
    "opencv-python>=4.8.0",  # 图像处理
]
```
