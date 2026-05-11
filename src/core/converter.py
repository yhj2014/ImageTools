"""
图像格式转换模块

该模块使用 FFmpeg 进行图像格式转换，
支持多种常见的图像格式之间的相互转换。
"""

import os
from pathlib import Path
from typing import Optional, Tuple, List
from enum import Enum


class ImageFormat(Enum):
    """支持的图像格式枚举"""
    PNG = 'png'
    JPG = 'jpg'
    JPEG = 'jpeg'
    WEBP = 'webp'
    BMP = 'bmp'
    TIFF = 'tiff'
    TIF = 'tif'
    GIF = 'gif'
    TGA = 'tga'

    @classmethod
    def from_extension(cls, ext: str) -> Optional['ImageFormat']:
        """
        根据文件扩展名获取格式枚举

        Args:
            ext: 文件扩展名（包含或不包含点均可）

        Returns:
            对应的 ImageFormat 枚举值，如果不支持返回 None
        """
        ext = ext.lower().strip('.')
        for format in cls:
            if format.value.lower() == ext:
                return format
            # 处理 TIFF/TIF 特殊映射
            if ext in ('tiff', 'tif') and format == cls.TIFF:
                return cls.TIFF
        return None

    @classmethod
    def get_all_formats(cls) -> List[str]:
        """
        获取所有支持的格式列表

        Returns:
            格式字符串列表
        """
        return [f.value for f in cls]


class ImageConverter:
    """图像格式转换器类"""

    # 支持的输入格式集合
    SUPPORTED_INPUT_FORMATS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'tif', 'gif', 'tga'}

    # 支持的输出格式集合
    SUPPORTED_OUTPUT_FORMATS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'tif', 'gif', 'tga'}

    # FFmpeg 像素格式映射（用于不同格式转换）
    PIXEL_FORMATS = {
        'png': 'rgba',
        'jpg': 'rgb24',
        'jpeg': 'rgb24',
        'webp': 'rgba',
        'bmp': 'rgb24',
        'tiff': 'rgba',
        'tif': 'rgba',
        'gif': 'pal8',
        'tga': 'rgb24'
    }

    def __init__(self, ffmpeg_manager):
        """
        初始化图像转换器

        Args:
            ffmpeg_manager: FFmpegManager 实例
        """
        self.ffmpeg = ffmpeg_manager

    def is_format_supported(self, format_str: str) -> bool:
        """
        检查格式是否支持

        Args:
            format_str: 格式字符串

        Returns:
            如果支持返回 True，否则返回 False
        """
        format_str = format_str.lower().strip('.')
        return format_str in self.SUPPORTED_INPUT_FORMATS

    def convert(
        self,
        input_path: str | Path,
        output_path: str | Path,
        quality: int = 85,
        overwrite: bool = True
    ) -> Tuple[bool, str]:
        """
        将图像从一种格式转换为另一种格式

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            quality: 图像质量 (1-100)，默认为 85
            overwrite: 是否覆盖已存在的输出文件，默认为 True

        Returns:
            (成功标志, 消息) 元组
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        # 验证输入文件存在
        if not input_path.exists():
            return False, f"输入文件不存在: {input_path}"

        # 获取输入和输出格式
        input_format = input_path.suffix.lower().strip('.')
        output_format = output_path.suffix.lower().strip('.')

        # 验证格式支持
        if input_format not in self.SUPPORTED_INPUT_FORMATS:
            return False, f"不支持的输入格式: {input_format}"

        if output_format not in self.SUPPORTED_OUTPUT_FORMATS:
            return False, f"不支持的输出格式: {output_format}"

        # 检查输出目录是否存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 如果输出文件已存在且不覆盖，则返回错误
        if output_path.exists() and not overwrite:
            return False, f"输出文件已存在: {output_path}"

        # 限制 quality 范围
        quality = max(1, min(100, quality))

        try:
            # 构建 FFmpeg 命令
            args = self._build_ffmpeg_args(input_path, output_path, quality, overwrite)

            # 执行转换
            returncode, stdout, stderr = self.ffmpeg.execute(args)

            if returncode == 0:
                # 验证输出文件是否生成
                if output_path.exists():
                    return True, f"转换成功: {output_path}"
                else:
                    return False, "转换完成但未找到输出文件"
            else:
                error_msg = stderr if stderr else "未知错误"
                return False, f"转换失败: {error_msg}"

        except Exception as e:
            return False, f"转换异常: {str(e)}"

    def _build_ffmpeg_args(
        self,
        input_path: Path,
        output_path: Path,
        quality: int,
        overwrite: bool
    ) -> List[str]:
        """
        构建 FFmpeg 命令参数

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            quality: 图像质量
            overwrite: 是否覆盖

        Returns:
            FFmpeg 参数列表
        """
        args = ['-y'] if overwrite else []

        # 添加输入文件
        args.extend(['-i', str(input_path)])

        # 根据输出格式添加参数
        output_format = output_path.suffix.lower().strip('.')

        # JPEG/JPG 格式需要特殊处理质量
        if output_format in ('jpg', 'jpeg'):
            args.extend(['-q:v', str(self._quality_to_ffmpeg_qv(quality))])
        # PNG 格式不支持质量参数，使用默认压缩
        elif output_format == 'png':
            # PNG 压缩级别 0-9，数字越大压缩越高
            compression_level = min(9, max(0, (100 - quality) // 11))
            args.extend(['-compression_level', str(compression_level)])
        # WebP 格式支持质量参数
        elif output_format == 'webp':
            args.extend(['-quality', str(quality)])
        # TIFF 格式可以设置压缩
        elif output_format in ('tiff', 'tif'):
            args.extend(['-compression_algo', 'lzw'])
        # GIF 格式特殊处理
        elif output_format == 'gif':
            # GIF 设置质量参数
            args.extend(['-loop', '0'])
        # 其他格式使用默认设置

        # 添加输出文件
        args.append(str(output_path))

        return args

    def _quality_to_ffmpeg_qv(self, quality: int) -> int:
        """
        将 1-100 的质量值转换为 FFmpeg 的 q:v 值

        FFmpeg 的 q:v 范围是 1-31，数字越小质量越高
        质量 100 -> q:v 1
        质量 1 -> q:v 31

        Args:
            quality: 质量值 (1-100)

        Returns:
            FFmpeg q:v 值 (1-31)
        """
        # 线性映射：quality=100 -> qv=1, quality=1 -> qv=31
        qv = int(32 - (quality * 31 / 100))
        return max(1, min(31, qv))

    def batch_convert(
        self,
        input_files: List[Path | str],
        output_dir: Path | str,
        output_format: str,
        quality: int = 85,
        overwrite: bool = True,
        progress_callback=None
    ) -> Tuple[int, int, List[str]]:
        """
        批量转换图像格式

        Args:
            input_files: 输入文件路径列表
            output_dir: 输出目录路径
            output_format: 输出格式（如 'png', 'jpg' 等）
            quality: 图像质量 (1-100)
            overwrite: 是否覆盖已存在的输出文件
            progress_callback: 进度回调函数，接收 (current, total, message) 参数

        Returns:
            (成功数量, 失败数量, 错误消息列表) 元组
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        fail_count = 0
        errors = []

        total = len(input_files)

        for index, input_file in enumerate(input_files):
            input_file = Path(input_file)

            # 生成输出文件名
            output_name = input_file.stem + '.' + output_format.lower().strip('.')
            output_path = output_dir / output_name

            # 执行转换
            success, message = self.convert(input_file, output_path, quality, overwrite)

            if success:
                success_count += 1
            else:
                fail_count += 1
                errors.append(f"{input_file.name}: {message}")

            # 调用进度回调
            if progress_callback:
                progress_callback(index + 1, total, message)

        return success_count, fail_count, errors

    def get_format_info(self, file_path: Path | str) -> Optional[dict]:
        """
        获取图像格式信息（使用 FFprobe）

        注意: 该功能需要 ffmpeg 安装包含 ffprobe，
        如果不可用则返回基本信息

        Args:
            file_path: 图像文件路径

        Returns:
            格式信息字典，如果失败返回 None
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return None

        format_str = file_path.suffix.lower().strip('.')

        return {
            'format': format_str,
            'format_name': ImageFormat.from_extension(format_str).name if ImageFormat.from_extension(format_str) else 'UNKNOWN',
            'size_bytes': file_path.stat().st_size,
            'supported_input': format_str in self.SUPPORTED_INPUT_FORMATS,
            'supported_output': format_str in self.SUPPORTED_OUTPUT_FORMATS
        }
