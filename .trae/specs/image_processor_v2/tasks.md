# ImageForge 开发任务清单

## 项目初始化

- [x] 使用 UV 初始化项目结构 `uv init`
- [x] 创建 `pyproject.toml` 配置依赖 (PySide6, Pillow, requests)
- [x] 创建 src 目录结构
- [x] 创建所有 `__init__.py` 文件

## 核心模块开发

- [x] **core/ffmpeg_manager.py**: FFmpeg 下载和管理器
  - 实现自动下载 FFmpeg
  - 实现版本检测和更新检查
  - 实现跨平台支持

- [x] **core/converter.py**: 图像格式转换
  - 封装 FFmpeg 调用
  - 实现质量控制
  - 实现元数据处理

- [x] **core/processor.py**: 图像处理引擎
  - 封装 Pillow 操作
  - 实现裁剪、缩放、旋转
  - 实现滤镜效果

- [x] **core/worker.py**: 多线程任务处理器
  - 实现任务队列
  - 实现进度报告
  - 实现取消/暂停功能

- [x] **core/presets.py**: 预设配置管理
  - 尺寸预设
  - 格式预设
  - 用户自定义预设

## 功能模块开发

- [x] **features/crop.py**: 裁剪功能
  - 预设比例裁剪
  - 自定义尺寸裁剪
  - 自由裁剪区域

- [x] **features/watermark.py**: 水印功能
  - 文字水印
  - 图片水印
  - 位置控制
  - 透明度控制

- [x] **features/resize.py**: 缩放功能
  - 预设尺寸缩放
  - 自定义尺寸缩放
  - 缩放算法选择

- [x] **features/rotate.py**: 旋转翻转
  - 固定角度旋转
  - 自定义角度旋转
  - 水平/垂直翻转

- [x] **features/filter.py**: 滤镜效果
  - 亮度/对比度/饱和度
  - 灰度/模糊/锐化

- [x] **features/gif_maker.py**: GIF 制作
  - 多图合成 GIF
  - 帧延迟设置
  - 循环次数控制

- [x] **features/rename.py**: 批量重命名
  - 模板化命名
  - 序号生成
  - 预览效果

- [x] **features/pdf_converter.py**: PDF 转换
  - 图片转 PDF
  - 页面布局选项

## UI 模块开发

- [x] **ui/main_window.py**: 主窗口
  - 响应式布局
  - 侧边栏导航
  - 状态栏

- [x] **ui/widgets/file_list.py**: 文件列表组件
  - 拖拽支持
  - 多选支持
  - 右键菜单

- [x] **ui/widgets/preview.py**: 预览组件
  - 图像预览
  - 效果预览

- [x] **ui/widgets/slider.py**: 滑块组件
  - 带数值显示
  - 样式定制

- [x] **ui/widgets/tabs.py**: 功能标签页
  - 裁剪标签页
  - 水印标签页
  - 缩放标签页
  - 旋转标签页
  - 滤镜标签页
  - GIF 标签页
  - 重命名标签页
  - PDF 标签页

- [x] **ui/styles/theme.py**: 主题配置
  - 颜色配置
  - 字体配置
  - 尺寸配置

- [x] **ui/styles/qss.py**: QSS 样式表
  - 现代简洁风格
  - 响应式适配

## 工具模块开发

- [x] **utils/logger.py**: 日志系统
  - 文件日志
  - 控制台日志
  - 日志级别

- [x] **utils/config.py**: 配置管理
  - 用户配置读写
  - 默认配置
  - 配置验证

- [x] **utils/helpers.py**: 辅助函数
  - 文件操作
  - 路径处理
  - 格式转换

## 主程序入口

- [x] **main.py**: 应用入口
  - 初始化日志
  - 初始化 UI
  - 事件循环

- [x] **app.py**: 应用主类
  - 生命周期管理
  - 窗口管理

## 测试与验证

- [x] 语法检查 - 所有文件编译通过
- [ ] 功能测试 - 格式转换
- [ ] 功能测试 - 裁剪功能
- [ ] 功能测试 - 水印功能
- [ ] 功能测试 - 缩放功能
- [ ] 功能测试 - 旋转翻转
- [ ] 功能测试 - 滤镜效果
- [ ] 功能测试 - GIF 制作
- [ ] 功能测试 - 批量重命名
- [ ] 功能测试 - PDF 转换
- [ ] 响应式布局测试
- [ ] FFmpeg 自动下载测试
- [ ] 错误处理测试

## 依赖任务

### 任务依赖关系

```
项目初始化
    ↓
核心模块 (可并行)
    ├── ffmpeg_manager.py
    ├── converter.py
    ├── processor.py
    ├── worker.py
    └── presets.py
    ↓
功能模块 (可并行)
    ├── crop.py
    ├── watermark.py
    ├── resize.py
    ├── rotate.py
    ├── filter.py
    ├── gif_maker.py
    ├── rename.py
    └── pdf_converter.py
    ↓
UI 模块
    ├── main_window.py
    ├── widgets/ (可并行)
    └── styles/ (可并行)
    ↓
工具模块 (可与核心模块并行)
    ├── logger.py
    ├── config.py
    └── helpers.py
    ↓
主程序入口
    ↓
测试与验证
```
