"""
图像滤镜效果模块
提供多种图像处理滤镜：亮度、对比度、饱和度调整
支持灰度转换、高斯模糊、锐化效果
使用 Pillow 库和 ImageEnhance 模块实现
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageChops
from typing import Tuple, Optional, Union


class ImageFilterProcessor:
    """
    图像滤镜处理类
    提供多种滤镜效果：亮度、对比度、饱和度、灰度、模糊、锐化等
    """
    
    def __init__(self, image_path: str):
        """
        初始化滤镜处理器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
    
    def adjust_brightness(self, factor: float) -> Image.Image:
        """
        调整图像亮度
        
        Args:
            factor: 亮度调整因子 (-100 到 +100)
                   0 = 完全黑色
                   50 = 半亮
                   100 = 原始亮度
                   150 = 1.5倍亮度
        
        Returns:
            调整后的图像对象
        """
        enhancer = ImageEnhance.Brightness(self.image)
        # 将 -100 到 +100 转换为 0 到 2 的因子
        adjusted_factor = (factor + 100) / 100
        return enhancer.enhance(adjusted_factor)
    
    def adjust_contrast(self, factor: float) -> Image.Image:
        """
        调整图像对比度
        
        Args:
            factor: 对比度调整因子 (-100 到 +100)
                   0 = 灰度
                   100 = 原始对比度
                   200 = 2倍对比度
        
        Returns:
            调整后的图像对象
        """
        enhancer = ImageEnhance.Contrast(self.image)
        # 将 -100 到 +100 转换为 0 到 2 的因子
        adjusted_factor = (factor + 100) / 100
        return enhancer.enhance(adjusted_factor)
    
    def adjust_saturation(self, factor: float) -> Image.Image:
        """
        调整图像饱和度
        
        Args:
            factor: 饱和度调整因子 (-100 到 +100)
                   0 = 灰度图像
                   100 = 原始饱和度
                   200 = 2倍饱和度
        
        Returns:
            调整后的图像对象
        """
        enhancer = ImageEnhance.Color(self.image)
        # 将 -100 到 +100 转换为 0 到 2 的因子
        adjusted_factor = (factor + 100) / 100
        return enhancer.enhance(adjusted_factor)
    
    def adjust_brightness_contrast_saturation(
        self,
        brightness: float = 0,
        contrast: float = 0,
        saturation: float = 0
    ) -> Image.Image:
        """
        同时调整亮度、对比度和饱和度
        
        Args:
            brightness: 亮度调整因子 (-100 到 +100)
            contrast: 对比度调整因子 (-100 到 +100)
            saturation: 饱和度调整因子 (-100 到 +100)
        
        Returns:
            调整后的图像对象
        """
        result = self.image.copy()
        
        # 调整亮度
        if brightness != 0:
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance((brightness + 100) / 100)
        
        # 调整对比度
        if contrast != 0:
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance((contrast + 100) / 100)
        
        # 调整饱和度
        if saturation != 0:
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance((saturation + 100) / 100)
        
        return result
    
    def to_grayscale(self, mode: str = 'luminosity') -> Image.Image:
        """
        灰度转换
        
        Args:
            mode: 灰度转换模式
                 'luminosity': 亮度灰度（加权平均），更符合人眼感知
                 'average': 平均灰度
                 'lightscape': 明度灰度
        
        Returns:
            灰度图像对象
        """
        if mode == 'luminosity':
            # 亮度灰度：人眼对绿色更敏感
            # 使用加权公式: 0.21*R + 0.72*G + 0.07*B
            return self.image.convert('L')
        elif mode == 'average':
            # 简单平均
            return self.image.convert('1')
        else:
            return self.image.convert('L')
    
    def gaussian_blur(self, radius: float = 2) -> Image.Image:
        """
        高斯模糊
        
        Args:
            radius: 模糊半径 (1-20)，值越大越模糊
        
        Returns:
            模糊后的图像对象
        """
        # 限制半径范围
        radius = max(0.1, min(radius, 250))
        return self.image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def sharpen(self, intensity: float = 1.0) -> Image.Image:
        """
        锐化效果
        
        Args:
            intensity: 锐化强度 (0.0 到 3.0)，默认 1.0
        
        Returns:
            锐化后的图像对象
        """
        # 创建锐化滤镜
        if intensity == 1.0:
            return self.image.filter(ImageFilter.SHARPEN)
        else:
            # 自定义锐化内核
            # 锐化核
            enhancer = ImageEnhance.Sharpness(self.image)
            return enhancer.enhance(intensity)
    
    def edge_enhance(self) -> Image.Image:
        """
        边缘增强
        
        Returns:
            边缘增强后的图像对象
        """
        return self.image.filter(ImageFilter.EDGE_ENHANCE)
    
    def edge_detect(self) -> Image.Image:
        """
        边缘检测
        
        Returns:
            边缘检测后的图像对象
        """
        return self.image.filter(ImageFilter.FIND_EDGES)
    
    def smooth(self, intensity: float = 1.0) -> Image.Image:
        """
        平滑处理
        
        Args:
            intensity: 平滑强度 (0.0 到 3.0)
        
        Returns:
            平滑后的图像对象
        """
        enhancer = ImageEnhance.Sharpness(self.image)
        return enhancer.enhance(1.0 / intensity)
    
    def sepia(self) -> Image.Image:
        """
        复古棕褐色调（复古滤镜）
        
        Returns:
            复古棕褐色调图像对象
        """
        # 先转换为灰度
        gray = self.image.convert('L')
        
        # 创建棕褐色调调色板
        # 亮度到棕褐色的映射
        sepia_palette = []
        for i in range(256):
            r = min(255, int(i * 1.2))
            g = min(255, int(i * 1.0))
            b = min(255, int(i * 0.8))
            sepia_palette.extend([r, g, b])
        
        # 应用调色板
        sepia = gray.convert('RGB')
        sepia.putpalette(sepia_palette)
        
        return sepia
    
    def vintage(self, strength: float = 0.5) -> Image.Image:
        """
        复古滤镜（降低饱和度 + 降低对比度 + 暖色调）
        
        Args:
            strength: 复古效果强度 (0.0 到 1.0)
        
        Returns:
            复古风格图像对象
        """
        result = self.image.copy()
        
        # 降低饱和度
        if strength > 0:
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.0 - strength * 0.5)
        
        # 降低对比度
        if strength > 0:
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1.0 - strength * 0.3)
        
        # 暖色调（增加红色和黄色）
        # 这是一个简化实现
        rgb_result = result.convert('RGB')
        pixels = rgb_result.load()
        width, height = rgb_result.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # 轻微增加暖色调
                r = min(255, int(r * (1 + strength * 0.1)))
                g = min(255, int(g * (1 + strength * 0.05)))
                b = max(0, int(b * (1 - strength * 0.1)))
                pixels[x, y] = (r, g, b)
        
        return rgb_result
    
    def vignette(self, strength: float = 0.5) -> Image.Image:
        """
        暗角效果
        
        Args:
            strength: 暗角强度 (0.0 到 1.0)
        
        Returns:
            添加暗角效果的图像对象
        """
        # 创建渐变遮罩
        width, height = self.image.size
        center_x = width // 2
        center_y = height // 2
        max_dist = ((center_x ** 2 + center_y ** 2) ** 0.5)
        
        # 创建径向渐变
        gradient = Image.new('L', (width, height), 255)
        pixels = gradient.load()
        
        for y in range(height):
            for x in range(width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = dist / max_dist
                # 使用余弦曲线创建更自然的暗角
                factor = 1 - (ratio ** 2) * strength
                pixels[x, y] = max(0, int(255 * factor))
        
        # 应用到原图
        dark_corner = self.image.copy().convert('RGB')
        dark_corner.putalpha(gradient)
        
        return dark_corner
    
    def apply_filter(
        self,
        filter_type: str,
        **kwargs
    ) -> Image.Image:
        """
        应用指定类型的滤镜
        
        Args:
            filter_type: 滤镜类型 ('brightness', 'contrast', 'saturation', 
                        'grayscale', 'blur', 'sharpen', 'sepia', 'vintage', 'vignette')
            **kwargs: 滤镜参数
        
        Returns:
            应用滤镜后的图像对象
        """
        filters = {
            'brightness': lambda: self.adjust_brightness(kwargs.get('factor', 0)),
            'contrast': lambda: self.adjust_contrast(kwargs.get('factor', 0)),
            'saturation': lambda: self.adjust_saturation(kwargs.get('factor', 0)),
            'grayscale': lambda: self.to_grayscale(kwargs.get('mode', 'luminosity')),
            'blur': lambda: self.gaussian_blur(kwargs.get('radius', 2)),
            'sharpen': lambda: self.sharpen(kwargs.get('intensity', 1.0)),
            'sepia': lambda: self.sepia(),
            'vintage': lambda: self.vintage(kwargs.get('strength', 0.5)),
            'vignette': lambda: self.vignette(kwargs.get('strength', 0.5)),
        }
        
        if filter_type not in filters:
            raise ValueError(f"不支持的滤镜类型。可选值: {list(filters.keys())}")
        
        return filters[filter_type]()
    
    def save(self, output_path: str, filtered_image: Image.Image, quality: int = 95):
        """
        保存滤镜处理后的图像
        
        Args:
            output_path: 输出文件路径
            filtered_image: 处理后的图像对象
            quality: JPEG 质量 (1-100)，默认 95
        """
        # 处理 RGBA 图像
        if filtered_image.mode == 'RGBA':
            rgb_image = filtered_image.convert('RGB')
            rgb_image.save(output_path, 'JPEG', quality=quality)
        elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            filtered_image.save(output_path, 'JPEG', quality=quality)
        else:
            filtered_image.save(output_path)
    
    def reset(self):
        """重置为原始图像"""
        if hasattr(self, 'original_image'):
            self.image = self.original_image.copy()
    
    def close(self):
        """关闭图像，释放资源"""
        if hasattr(self, 'image'):
            self.image.close()
        if hasattr(self, 'original_image'):
            self.original_image.close()


def apply_brightness(image_path: str, output_path: str, factor: float) -> str:
    """
    便捷函数：调整图像亮度并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        factor: 亮度调整因子 (-100 到 +100)
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.adjust_brightness(factor)
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()


def apply_contrast(image_path: str, output_path: str, factor: float) -> str:
    """
    便捷函数：调整图像对比度并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        factor: 对比度调整因子 (-100 到 +100)
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.adjust_contrast(factor)
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()


def apply_saturation(image_path: str, output_path: str, factor: float) -> str:
    """
    便捷函数：调整图像饱和度并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        factor: 饱和度调整因子 (-100 到 +100)
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.adjust_saturation(factor)
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()


def apply_grayscale(image_path: str, output_path: str) -> str:
    """
    便捷函数：灰度转换并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.to_grayscale()
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()


def apply_blur(image_path: str, output_path: str, radius: float = 2) -> str:
    """
    便捷函数：高斯模糊并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        radius: 模糊半径 (1-20)
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.gaussian_blur(radius)
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()


def apply_sharpen(image_path: str, output_path: str, intensity: float = 1.0) -> str:
    """
    便捷函数：锐化并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        intensity: 锐化强度 (0.0 到 3.0)
    
    Returns:
        输出文件路径
    """
    processor = ImageFilterProcessor(image_path)
    try:
        result = processor.sharpen(intensity)
        processor.save(output_path, result)
        return output_path
    finally:
        processor.close()
