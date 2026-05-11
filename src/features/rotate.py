"""
图像旋转与翻转功能模块
提供多种旋转方式：固定角度旋转、自定义角度旋转
支持水平翻转和垂直翻转
使用 Pillow 库实现
"""

from PIL import Image
from typing import Optional, Tuple, Union, Literal
import math


class ImageRotator:
    """
    图像旋转与翻转类
    支持固定角度旋转、自定义角度旋转、水平翻转和垂直翻转
    """
    
    # 固定旋转角度选项
    FIXED_ANGLES = {
        '90': 90,
        '180': 180,
        '270': 270,
    }
    
    def __init__(self, image_path: str):
        """
        初始化旋转处理器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_width, self.original_height = self.image.size
    
    def rotate_fixed(self, angle: Union[int, str]) -> Image.Image:
        """
        固定角度旋转（90°/180°/270°）
        
        Args:
            angle: 旋转角度，可以是 90, 180, 270 或对应的字符串
        
        Returns:
            旋转后的图像对象
        
        Raises:
            ValueError: 当角度无效时抛出
        """
        # 处理字符串输入
        if isinstance(angle, str):
            if angle not in self.FIXED_ANGLES:
                raise ValueError(f"无效的固定角度。可选值: 90, 180, 270")
            angle = self.FIXED_ANGLES[angle]
        
        # 验证角度
        if angle not in [90, 180, 270]:
            raise ValueError("固定角度必须是 90°, 180° 或 270°")
        
        # 执行旋转
        return self.image.rotate(angle, expand=True)
    
    def rotate_custom(self, angle: float, expand: bool = True, fillcolor: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """
        自定义角度旋转
        
        Args:
            angle: 旋转角度（度），范围 -180° 到 +180°
            expand: 是否扩展图像以容纳旋转后的内容，默认 True
            fillcolor: 旋转后空白区域的填充颜色，默认白色
        
        Returns:
            旋转后的图像对象
        
        Raises:
            ValueError: 当角度超出范围时抛出
        """
        # 验证角度范围
        if angle < -180 or angle > 180:
            raise ValueError("旋转角度必须在 -180° 到 +180° 之间")
        
        # 执行旋转
        return self.image.rotate(angle, expand=expand, fillcolor=fillcolor)
    
    def rotate_with_crop(
        self,
        angle: float,
        crop: bool = True,
        fillcolor: Tuple[int, int, int] = (255, 255, 255)
    ) -> Image.Image:
        """
        带裁剪的旋转（保持原图尺寸）
        
        旋转后自动裁剪到与原图相同的尺寸，居中显示
        
        Args:
            angle: 旋转角度（度）
            crop: 是否裁剪以保持原尺寸，默认 True
            fillcolor: 空白区域填充颜色
        
        Returns:
            旋转后的图像对象
        """
        if not crop:
            return self.rotate_custom(angle, expand=True, fillcolor=fillcolor)
        
        # 计算旋转后的图像
        rotated = self.image.rotate(angle, expand=True)
        
        # 计算中心点
        rot_width, rot_height = rotated.size
        center_x = rot_width // 2
        center_y = rot_height // 2
        
        # 裁剪到原图尺寸（居中）
        left = center_x - self.original_width // 2
        top = center_y - self.original_height // 2
        right = left + self.original_width
        bottom = top + self.original_height
        
        # 确保裁剪区域有效
        if left < 0 or top < 0 or right > rot_width or bottom > rot_height:
            # 如果原图太大无法裁剪，返回扩展后的图像
            return rotated
        
        return rotated.crop((left, top, right, bottom))
    
    def flip_horizontal(self) -> Image.Image:
        """
        水平翻转图像
        
        Returns:
            翻转后的图像对象
        """
        return self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    def flip_vertical(self) -> Image.Image:
        """
        垂直翻转图像
        
        Returns:
            翻转后的图像对象
        """
        return self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    
    def auto_orient(self) -> Image.Image:
        """
        自动校正图像方向
        根据 EXIF 数据自动旋转到正确方向
        
        Returns:
            校正后的图像对象
        """
        # 尝试获取 EXIF 信息
        try:
            exif = self.image.getexif()
            if exif:
                # 获取 Orientation 标签
                orientation = exif.get(0x0112)  # Orientation 标签号
                
                if orientation == 2:
                    return self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    return self.image.rotate(180, expand=True)
                elif orientation == 4:
                    return self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                elif orientation == 5:
                    return self.image.transpose(Image.Transpose.TRANSPOSE)
                elif orientation == 6:
                    return self.image.rotate(270, expand=True)
                elif orientation == 7:
                    return self.image.transpose(Image.Transpose.TRANSVERSE)
                elif orientation == 8:
                    return self.image.rotate(90, expand=True)
        except Exception:
            # 如果无法获取 EXIF，返回原图
            pass
        
        return self.image.copy()
    
    def rotate_90(self) -> Image.Image:
        """
        顺时针旋转 90°
        
        Returns:
            旋转后的图像对象
        """
        return self.image.rotate(90, expand=True)
    
    def rotate_180(self) -> Image.Image:
        """
        旋转 180°
        
        Returns:
            旋转后的图像对象
        """
        return self.image.rotate(180, expand=True)
    
    def rotate_270(self) -> Image.Image:
        """
        顺时针旋转 270°（逆时针旋转 90°）
        
        Returns:
            旋转后的图像对象
        """
        return self.image.rotate(270, expand=True)
    
    def save(self, output_path: str, rotated_image: Image.Image, quality: int = 95):
        """
        保存旋转后的图像
        
        Args:
            output_path: 输出文件路径
            rotated_image: 旋转后的图像对象
            quality: JPEG 质量 (1-100)，默认 95
        """
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            rotated_image.save(output_path, 'JPEG', quality=quality)
        else:
            rotated_image.save(output_path)
    
    def close(self):
        """关闭图像，释放资源"""
        if hasattr(self, 'image'):
            self.image.close()


def rotate_image(
    image_path: str,
    output_path: str,
    angle: Union[int, float],
    crop: bool = True,
    fillcolor: Tuple[int, int, int] = (255, 255, 255)
) -> str:
    """
    便捷函数：旋转图像并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        angle: 旋转角度（度），-180 到 +180
        crop: 是否裁剪以保持原尺寸，默认 True
        fillcolor: 空白区域填充颜色
    
    Returns:
        输出文件路径
    """
    rotator = ImageRotator(image_path)
    try:
        if crop:
            result = rotator.rotate_with_crop(angle, crop=crop, fillcolor=fillcolor)
        else:
            result = rotator.rotate_custom(angle, fillcolor=fillcolor)
        rotator.save(output_path, result)
        return output_path
    finally:
        rotator.close()


def flip_image(
    image_path: str,
    output_path: str,
    direction: Literal['horizontal', 'vertical']
) -> str:
    """
    便捷函数：翻转图像并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        direction: 翻转方向 ('horizontal' 水平, 'vertical' 垂直)
    
    Returns:
        输出文件路径
    """
    rotator = ImageRotator(image_path)
    try:
        if direction == 'horizontal':
            result = rotator.flip_horizontal()
        else:
            result = rotator.flip_vertical()
        rotator.save(output_path, result)
        return output_path
    finally:
        rotator.close()


def rotate_multiple_images(
    image_paths: list,
    output_dir: str,
    angle: float,
    crop: bool = True,
    prefix: str = 'rotated_'
) -> list:
    """
    批量旋转多张图像
    
    Args:
        image_paths: 输入图像路径列表
        output_dir: 输出目录
        angle: 旋转角度（度）
        crop: 是否裁剪以保持原尺寸
        prefix: 输出文件名前缀
    
    Returns:
        输出文件路径列表
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    output_paths = []
    for image_path in image_paths:
        basename = os.path.basename(image_path)
        name, ext = os.path.splitext(basename)
        output_path = os.path.join(output_dir, f"{prefix}{name}{ext}")
        
        rotate_image(image_path, output_path, angle, crop)
        output_paths.append(output_path)
    
    return output_paths
