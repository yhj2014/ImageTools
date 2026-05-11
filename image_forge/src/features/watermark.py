"""
水印功能模块
提供文字水印和图片水印功能
支持多种位置设置和平铺模式
使用纯 Pillow 库实现
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from typing import Tuple, Optional, Union, List
import os


class Watermarker:
    """
    水印处理类
    支持文字水印和图片水印，提供九宫格位置设置和平铺模式
    """
    
    # 九宫格位置定义
    POSITIONS = {
        '左上': (0, 0),
        '中上': (0.5, 0),
        '右上': (1, 0),
        '左中': (0, 0.5),
        '居中': (0.5, 0.5),
        '右中': (1, 0.5),
        '左下': (0, 1),
        '中下': (0.5, 1),
        '右下': (1, 1),
    }
    
    def __init__(self, image_path: str):
        """
        初始化水印处理器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = Image.open(image_path).convert('RGBA')
        self.width, self.height = self.image.size
    
    def add_text_watermark(
        self,
        text: str,
        position: str = '右下',
        font_size: int = 36,
        font_color: Tuple[int, int, int, int] = (255, 255, 255, 128),
        font_path: Optional[str] = None,
        rotation: int = 0,
        opacity: int = 128,
        margin: Tuple[int, int] = (20, 20)
    ) -> Image.Image:
        """
        添加文字水印
        
        Args:
            text: 水印文本内容
            position: 位置名称 ('左上', '中上', '右上', '左中', '居中', '右中', '左下', '中下', '右下')
            font_size: 字体大小，默认 36
            font_color: 字体颜色 RGBA，默认半透明白色 (255, 255, 255, 128)
            font_path: 字体文件路径，None 则使用默认字体
            rotation: 旋转角度（度），默认 0 不旋转
            opacity: 透明度 0-255，默认 128
            margin: 边距 (水平边距, 垂直边距)，默认 (20, 20)
        
        Returns:
            添加水印后的图像对象
        """
        # 创建文字层
        txt_layer = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        # 尝试加载字体
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # 使用默认字体，大小受限于系统
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except Exception:
            # 如果找不到指定字体，使用默认字体
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算水印位置
        x, y = self._calculate_position(
            text_width, text_height, position, margin
        )
        
        # 调整颜色透明度
        adjusted_color = (font_color[0], font_color[1], font_color[2], opacity)
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=adjusted_color)
        
        # 应用旋转
        if rotation != 0:
            txt_layer = txt_layer.rotate(rotation, expand=True)
        
        # 合并图层
        return Image.alpha_composite(self.image, txt_layer)
    
    def add_image_watermark(
        self,
        watermark_path: str,
        position: str = '右下',
        scale: float = 1.0,
        opacity: int = 128,
        margin: Tuple[int, int] = (20, 20)
    ) -> Image.Image:
        """
        添加图片水印
        
        Args:
            watermark_path: 水印图片路径（支持 PNG 透明图片）
            position: 位置名称 ('左上', '中上', '右上', '左中', '居中', '右中', '左下', '中下', '右下')
            scale: 缩放比例，默认 1.0
            opacity: 透明度 0-255，默认 128
            margin: 边距 (水平边距, 垂直边距)，默认 (20, 20)
        
        Returns:
            添加水印后的图像对象
        """
        # 加载水印图片
        watermark = Image.open(watermark_path).convert('RGBA')
        
        # 根据缩放比例调整水印大小
        if scale != 1.0:
            new_width = int(watermark.width * scale)
            new_height = int(watermark.height * scale)
            watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 调整透明度
        if opacity != 255:
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 255)
            watermark.putalpha(alpha)
        
        # 计算水印位置
        x, y = self._calculate_position(
            watermark.width, watermark.height, position, margin
        )
        
        # 创建临时画布（大于原图以容纳旋转等效果）
        result = self.image.copy()
        
        # 将水印放置到对应位置
        if x + watermark.width <= self.width and y + watermark.height <= self.height:
            result.paste(watermark, (x, y), watermark)
        else:
            # 如果水印超出边界，裁剪后再放置
            result.paste(watermark, (x, y), watermark)
        
        return result
    
    def add_tiled_watermark(
        self,
        watermark_path: Optional[str] = None,
        text: Optional[str] = None,
        spacing: Tuple[int, int] = (100, 100),
        opacity: int = 50,
        rotation: int = -30
    ) -> Image.Image:
        """
        添加平铺水印（整图平铺模式）
        
        Args:
            watermark_path: 水印图片路径（与 text 二选一）
            text: 水印文字（与 watermark_path 二选一）
            spacing: 平铺间距 (水平间距, 垂直间距)，默认 (100, 100)
            opacity: 透明度 0-255，默认 50
            rotation: 旋转角度（度），默认 -30
        
        Returns:
            添加水印后的图像对象
        """
        if not watermark_path and not text:
            raise ValueError("必须提供 watermark_path 或 text 参数")
        
        # 创建平铺水印层
        tile_layer = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        
        if watermark_path:
            # 使用图片作为水印
            watermark = Image.open(watermark_path).convert('RGBA')
            if opacity != 255:
                alpha = watermark.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 255)
                watermark.putalpha(alpha)
            
            if rotation != 0:
                watermark = watermark.rotate(rotation, expand=True)
            
            # 平铺水印
            for y in range(-watermark.height, self.height + watermark.height, spacing[1] + watermark.height):
                for x in range(-watermark.width, self.width + watermark.width, spacing[0] + watermark.width):
                    if x + watermark.width > 0 and y + watermark.height > 0:
                        tile_layer.paste(watermark, (x, y), watermark)
        else:
            # 使用文字作为水印
            draw = ImageDraw.Draw(tile_layer)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except Exception:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 创建单个文字水印图像
            single_watermark = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))
            single_draw = ImageDraw.Draw(single_watermark)
            single_draw.text((5, 5), text, font=font, fill=(255, 255, 255, opacity))
            
            if rotation != 0:
                single_watermark = single_watermark.rotate(rotation, expand=True)
            
            # 平铺文字水印
            total_width = spacing[0] + single_watermark.width
            total_height = spacing[1] + single_watermark.height
            
            for y in range(-single_watermark.height, self.height + single_watermark.height, total_height):
                for x in range(-single_watermark.width, self.width + single_watermark.width, total_width):
                    if x + single_watermark.width > 0 and y + single_watermark.height > 0:
                        tile_layer.paste(single_watermark, (x, y), single_watermark)
        
        # 合并图层
        return Image.alpha_composite(self.image, tile_layer)
    
    def _calculate_position(
        self,
        element_width: int,
        element_height: int,
        position: str,
        margin: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
        计算元素的位置坐标
        
        Args:
            element_width: 元素宽度
            element_height: 元素高度
            position: 位置名称
            margin: 边距
        
        Returns:
            (x, y) 位置坐标
        """
        if position not in self.POSITIONS:
            position = '右下'  # 默认位置
        
        x_ratio, y_ratio = self.POSITIONS[position]
        
        # 计算位置，考虑边距
        if x_ratio == 0:
            x = margin[0]
        elif x_ratio == 1:
            x = self.width - element_width - margin[0]
        else:
            x = int((self.width - element_width) * x_ratio)
        
        if y_ratio == 0:
            y = margin[1]
        elif y_ratio == 1:
            y = self.height - element_height - margin[1]
        else:
            y = int((self.height - element_height) * y_ratio)
        
        return max(0, x), max(0, y)
    
    def save(self, output_path: str, watermarked_image: Image.Image, quality: int = 95):
        """
        保存添加水印后的图像
        
        Args:
            output_path: 输出文件路径
            watermarked_image: 添加水印后的图像对象
            quality: JPEG 质量 (1-100)，默认 95
        """
        # 转换为 RGB 模式（如果需要保存为 JPEG）
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            rgb_image = watermarked_image.convert('RGB')
            rgb_image.save(output_path, 'JPEG', quality=quality)
        else:
            watermarked_image.save(output_path)
    
    def close(self):
        """关闭图像，释放资源"""
        if hasattr(self, 'image'):
            self.image.close()


def add_text_watermark(
    image_path: str,
    output_path: str,
    text: str,
    position: str = '右下',
    font_size: int = 36,
    font_color: Tuple[int, int, int, int] = (255, 255, 255, 128),
    rotation: int = 0,
    opacity: int = 128,
    margin: Tuple[int, int] = (20, 20)
) -> str:
    """
    便捷函数：添加文字水印并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        text: 水印文本
        position: 位置
        font_size: 字体大小
        font_color: 字体颜色
        rotation: 旋转角度
        opacity: 透明度
        margin: 边距
    
    Returns:
        输出文件路径
    """
    watermarker = Watermarker(image_path)
    try:
        result = watermarker.add_text_watermark(
            text=text,
            position=position,
            font_size=font_size,
            font_color=font_color,
            rotation=rotation,
            opacity=opacity,
            margin=margin
        )
        watermarker.save(output_path, result)
        return output_path
    finally:
        watermarker.close()


def add_image_watermark(
    image_path: str,
    output_path: str,
    watermark_path: str,
    position: str = '右下',
    scale: float = 1.0,
    opacity: int = 128,
    margin: Tuple[int, int] = (20, 20)
) -> str:
    """
    便捷函数：添加图片水印并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        watermark_path: 水印图片路径
        position: 位置
        scale: 缩放比例
        opacity: 透明度
        margin: 边距
    
    Returns:
        输出文件路径
    """
    watermarker = Watermarker(image_path)
    try:
        result = watermarker.add_image_watermark(
            watermark_path=watermark_path,
            position=position,
            scale=scale,
            opacity=opacity,
            margin=margin
        )
        watermarker.save(output_path, result)
        return output_path
    finally:
        watermarker.close()


def add_tiled_watermark(
    image_path: str,
    output_path: str,
    watermark_path: Optional[str] = None,
    text: Optional[str] = None,
    spacing: Tuple[int, int] = (100, 100),
    opacity: int = 50,
    rotation: int = -30
) -> str:
    """
    便捷函数：添加平铺水印并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        watermark_path: 水印图片路径
        text: 水印文字
        spacing: 平铺间距
        opacity: 透明度
        rotation: 旋转角度
    
    Returns:
        输出文件路径
    """
    watermarker = Watermarker(image_path)
    try:
        result = watermarker.add_tiled_watermark(
            watermark_path=watermark_path,
            text=text,
            spacing=spacing,
            opacity=opacity,
            rotation=rotation
        )
        watermarker.save(output_path, result)
        return output_path
    finally:
        watermarker.close()
