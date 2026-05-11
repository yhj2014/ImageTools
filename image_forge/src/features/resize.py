"""
图像缩放功能模块
提供多种缩放方式：预设尺寸、自定义尺寸和等比缩放
支持多种缩放算法
使用 Pillow 库实现
"""

from PIL import Image
from typing import Tuple, Optional, Union, Literal


class ImageResizer:
    """
    图像缩放类
    支持预设尺寸、自定义尺寸、等比缩放和多种缩放算法
    """
    
    # 预设缩放尺寸
    PRESET_SIZES = {
        '800x600': (800, 600),
        '1024x768': (1024, 768),
        '1920x1080': (1920, 1080),  # Full HD
        '4K': (3840, 2160),
        '720p': (1280, 720),
        '1080p': (1920, 1080),
        '1440p': (2560, 1440),
    }
    
    # 缩放算法映射
    RESAMPLING_METHODS = {
        'nearest': Image.Resampling.NEAREST,      # 最近邻插值
        'bilinear': Image.Resampling.BILINEAR,    # 双线性插值
        'bicubic': Image.Resampling.BICUBIC,      # 双三次插值
        'lanczos': Image.Resampling.LANCZOS,      # Lanczos 插值
    }
    
    def __init__(self, image_path: str):
        """
        初始化缩放器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_width, self.original_height = self.image.size
    
    def resize_by_preset(
        self,
        preset_name: str,
        algorithm: str = 'lanczos',
        maintain_aspect: bool = True
    ) -> Image.Image:
        """
        使用预设尺寸缩放图像
        
        Args:
            preset_name: 预设尺寸名称 ('800x600', '1024x768', '1920x1080', '4K')
            algorithm: 缩放算法 ('nearest', 'bilinear', 'bicubic', 'lanczos')
            maintain_aspect: 是否保持宽高比，默认 True
        
        Returns:
            缩放后的图像对象
        
        Raises:
            ValueError: 当预设名称无效时抛出
        """
        if preset_name not in self.PRESET_SIZES:
            raise ValueError(f"无效的预设尺寸。可选值: {list(self.PRESET_SIZES.keys())}")
        
        target_width, target_height = self.PRESET_SIZES[preset_name]
        return self.resize(target_width, target_height, algorithm, maintain_aspect)
    
    def resize(
        self,
        width: int,
        height: int,
        algorithm: str = 'lanczos',
        maintain_aspect: bool = False
    ) -> Image.Image:
        """
        自定义尺寸缩放
        
        Args:
            width: 目标宽度（像素）
            height: 目标高度（像素）
            algorithm: 缩放算法 ('nearest', 'bilinear', 'bicubic', 'lanczos')
            maintain_aspect: 是否保持宽高比，默认 False
        
        Returns:
            缩放后的图像对象
        """
        # 获取缩放算法
        if algorithm not in self.RESAMPLING_METHODS:
            algorithm = 'lanczos'
        resample = self.RESAMPLING_METHODS[algorithm]
        
        # 如果需要保持宽高比
        if maintain_aspect:
            width, height = self._calculate_proportional_size(width, height)
        
        # 执行缩放
        return self.image.resize((width, height), resample)
    
    def resize_proportional(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        percentage: Optional[float] = None,
        algorithm: str = 'lanczos'
    ) -> Image.Image:
        """
        等比缩放图像
        
        Args:
            width: 目标宽度（像素），与 percentage 二选一
            height: 目标高度（像素），与 percentage 二选一
            percentage: 缩放百分比 (0.1 - 10.0)，与 width/height 二选一
            algorithm: 缩放算法 ('nearest', 'bilinear', 'bicubic', 'lanczos')
        
        Returns:
            缩放后的图像对象
        
        Raises:
            ValueError: 参数无效时抛出
        """
        if algorithm not in self.RESAMPLING_METHODS:
            algorithm = 'lanczos'
        resample = self.RESAMPLING_METHODS[algorithm]
        
        if percentage is not None:
            # 按百分比缩放
            if percentage <= 0 or percentage > 10:
                raise ValueError("百分比必须在 0.1 到 10.0 之间")
            new_width = int(self.original_width * percentage)
            new_height = int(self.original_height * percentage)
        elif width is not None:
            # 按宽度缩放
            aspect_ratio = self.original_height / self.original_width
            new_width = width
            new_height = int(width * aspect_ratio)
        elif height is not None:
            # 按高度缩放
            aspect_ratio = self.original_width / self.original_height
            new_width = int(height * aspect_ratio)
            new_height = height
        else:
            raise ValueError("必须提供 width, height 或 percentage 参数")
        
        return self.image.resize((new_width, new_height), resample)
    
    def fit_within(
        self,
        max_width: int,
        max_height: int,
        algorithm: str = 'lanczos'
    ) -> Image.Image:
        """
        将图像缩放到最大尺寸范围内（保持宽高比）
        
        Args:
            max_width: 最大宽度
            max_height: 最大高度
            algorithm: 缩放算法
        
        Returns:
            缩放后的图像对象
        """
        # 计算缩放后的尺寸，确保不超出最大尺寸
        width_ratio = max_width / self.original_width
        height_ratio = max_height / self.original_height
        ratio = min(width_ratio, height_ratio, 1.0)  # 不放大
        
        new_width = int(self.original_width * ratio)
        new_height = int(self.original_height * ratio)
        
        if algorithm not in self.RESAMPLING_METHODS:
            algorithm = 'lanczos'
        resample = self.RESAMPLING_METHODS[algorithm]
        
        return self.image.resize((new_width, new_height), resample)
    
    def _calculate_proportional_size(
        self,
        target_width: int,
        target_height: int
    ) -> Tuple[int, int]:
        """
        计算保持宽高比的尺寸
        
        Args:
            target_width: 目标宽度
            target_height: 目标高度
        
        Returns:
            (width, height) 调整后的尺寸
        """
        aspect_ratio = self.original_width / self.original_height
        target_aspect = target_width / target_height
        
        if aspect_ratio > target_aspect:
            # 原图更宽，以宽度为准
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # 原图更高，以高度为准
            new_height = target_height
            new_width = int(target_height * aspect_ratio)
        
        return new_width, new_height
    
    def get_algorithm_name(self, algorithm: str) -> str:
        """
        获取算法的中文名称
        
        Args:
            algorithm: 算法名称
        
        Returns:
            中文名称
        """
        names = {
            'nearest': '最近邻插值',
            'bilinear': '双线性插值',
            'bicubic': '双三次插值',
            'lanczos': 'Lanczos 插值'
        }
        return names.get(algorithm, algorithm)
    
    def save(self, output_path: str, resized_image: Image.Image, quality: int = 95):
        """
        保存缩放后的图像
        
        Args:
            output_path: 输出文件路径
            resized_image: 缩放后的图像对象
            quality: JPEG 质量 (1-100)，默认 95
        """
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            resized_image.save(output_path, 'JPEG', quality=quality)
        else:
            resized_image.save(output_path)
    
    def close(self):
        """关闭图像，释放资源"""
        if hasattr(self, 'image'):
            self.image.close()


def resize_image(
    image_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    percentage: Optional[float] = None,
    preset: Optional[str] = None,
    algorithm: str = 'lanczos',
    maintain_aspect: bool = True
) -> str:
    """
    便捷函数：缩放图像并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        width: 目标宽度
        height: 目标高度
        percentage: 缩放百分比
        preset: 预设尺寸名称
        algorithm: 缩放算法
        maintain_aspect: 是否保持宽高比
    
    Returns:
        输出文件路径
    """
    resizer = ImageResizer(image_path)
    
    try:
        if preset:
            result = resizer.resize_by_preset(preset, algorithm, maintain_aspect)
        elif percentage is not None:
            result = resizer.resize_proportional(percentage=percentage, algorithm=algorithm)
        elif width and height:
            result = resizer.resize(width, height, algorithm, maintain_aspect)
        elif width:
            result = resizer.resize_proportional(width=width, algorithm=algorithm)
        elif height:
            result = resizer.resize_proportional(height=height, algorithm=algorithm)
        else:
            raise ValueError("必须提供 preset, percentage, width, height 之一")
        
        resizer.save(output_path, result)
        return output_path
    finally:
        resizer.close()


def resize_multiple_images(
    image_paths: list,
    output_dir: str,
    width: int,
    height: int,
    algorithm: str = 'lanczos',
    maintain_aspect: bool = True,
    prefix: str = 'resized_'
) -> list:
    """
    批量缩放多张图像
    
    Args:
        image_paths: 输入图像路径列表
        output_dir: 输出目录
        width: 目标宽度
        height: 目标高度
        algorithm: 缩放算法
        maintain_aspect: 是否保持宽高比
        prefix: 输出文件名前缀
    
    Returns:
        输出文件路径列表
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_paths = []
    for image_path in image_paths:
        # 提取文件名
        basename = os.path.basename(image_path)
        name, ext = os.path.splitext(basename)
        output_path = os.path.join(output_dir, f"{prefix}{name}{ext}")
        
        resize_image(image_path, output_path, width, height, algorithm=algorithm, 
                    maintain_aspect=maintain_aspect)
        output_paths.append(output_path)
    
    return output_paths
