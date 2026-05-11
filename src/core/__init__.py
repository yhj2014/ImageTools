"""
核心模块 - 图像处理核心功能

该模块包含以下子模块：
- ffmpeg_manager: FFmpeg 下载和管理
- converter: 图像格式转换
- processor: Pillow 图像处理引擎
- worker: 多线程任务处理器
- presets: 预设配置
"""

from .ffmpeg_manager import FFmpegManager
from .converter import ImageConverter, ImageFormat
from .processor import ImageProcessor, FlipDirection
from .worker import TaskWorker, Task, TaskStatus, WorkerSignals, ProgressCallback
from .presets import (
    SizePreset,
    AspectRatioPreset,
    FormatPreset,
    ImagePreset,
    PresetManager,
    get_size_presets_dict,
    get_ratio_presets_dict,
    get_format_presets_dict
)

__all__ = [
    # FFmpeg 管理器
    'FFmpegManager',

    # 图像转换器
    'ImageConverter',
    'ImageFormat',

    # 图像处理器
    'ImageProcessor',
    'FlipDirection',

    # 任务处理器
    'TaskWorker',
    'Task',
    'TaskStatus',
    'WorkerSignals',
    'ProgressCallback',

    # 预设配置
    'SizePreset',
    'AspectRatioPreset',
    'FormatPreset',
    'ImagePreset',
    'PresetManager',
    'get_size_presets_dict',
    'get_ratio_presets_dict',
    'get_format_presets_dict',
]
