"""
裁剪功能模块
提供多种裁剪方式：预设比例裁剪和自定义尺寸裁剪
使用 Pillow 库实现图像裁剪功能
"""

from PIL import Image
from typing import Tuple, Optional, Union


class Cropper:
    """
    图像裁剪类
    支持预设比例裁剪和自定义尺寸裁剪
    """
    
    # 预设裁剪比例
    ASPECT_RATIOS = {
        '1:1': 1.0,           # 正方形 1:1
        '4:3': 4/3,           # 标准比例 4:3
        '16:9': 16/9,         # 宽屏比例 16:9
        '3:2': 3/2,           # 摄影标准 3:2
        '2:3': 2/3,           # 竖向摄影 2:3
        '9:16': 9/16          # 竖屏视频 9:16
    }
    
    def __init__(self, image_path: str):
        """
        初始化裁剪器
        
        Args:
            image_path: 图像文件路径
        """
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_width, self.original_height = self.image.size
    
    def crop_by_ratio(self, ratio_name: str, position: str = 'center') -> Image.Image:
        """
        根据预设比例裁剪图像
        
        Args:
            ratio_name: 裁剪比例名称 ('1:1', '4:3', '16:9', '3:2', '2:3', '9:16')
            position: 裁剪位置 ('center', 'top', 'bottom', 'left', 'right')
        
        Returns:
            裁剪后的图像对象
        
        Raises:
            ValueError: 当比例名称无效时抛出
        """
        if ratio_name not in self.ASPECT_RATIOS:
            raise ValueError(f"无效的裁剪比例。可选值: {list(self.ASPECT_RATIOS.keys())}")
        
        target_ratio = self.ASPECT_RATIOS[ratio_name]
        current_ratio = self.original_width / self.original_height
        
        # 根据比例计算裁剪区域
        if current_ratio > target_ratio:
            # 图像太宽，需要裁剪宽度
            new_width = int(self.original_height * target_ratio)
            new_height = self.original_height
        else:
            # 图像太高，需要裁剪高度
            new_width = self.original_width
            new_height = int(self.original_width / target_ratio)
        
        # 根据位置参数计算裁剪坐标
        left, top = self._calculate_crop_position(
            new_width, new_height, position
        )
        right = left + new_width
        bottom = top + new_height
        
        # 执行裁剪
        return self.image.crop((left, top, right, bottom))
    
    def crop_custom(
        self, 
        width: int, 
        height: int, 
        position: str = 'center'
    ) -> Image.Image:
        """
        自定义尺寸裁剪
        
        Args:
            width: 目标宽度（像素）
            height: 目标高度（像素）
            position: 裁剪位置 ('center', 'top', 'bottom', 'left', 'right', 'top-left', 
                     'top-right', 'bottom-left', 'bottom-right')
        
        Returns:
            裁剪后的图像对象
        """
        # 确保目标尺寸不超过原图尺寸
        if width > self.original_width:
            width = self.original_width
        if height > self.original_height:
            height = self.original_height
        
        # 计算裁剪位置
        left, top = self._calculate_crop_position(width, height, position)
        right = left + width
        bottom = top + height
        
        # 执行裁剪
        return self.image.crop((left, top, right, bottom))
    
    def _calculate_crop_position(
        self, 
        crop_width: int, 
        crop_height: int, 
        position: str
    ) -> Tuple[int, int]:
        """
        根据位置参数计算裁剪起点坐标
        
        Args:
            crop_width: 裁剪区域宽度
            crop_height: 裁剪区域高度
            position: 位置名称
        
        Returns:
            左上角坐标 (left, top)
        """
        # 计算可裁剪的范围
        max_left = self.original_width - crop_width
        max_top = self.original_height - crop_height
        
        # 根据位置参数确定裁剪起点
        position_lower = position.lower()
        
        if 'left' in position_lower:
            left = 0
        elif 'right' in position_lower:
            left = max_left
        else:  # center 或其他默认居中
            left = max_left // 2
        
        if 'top' in position_lower:
            top = 0
        elif 'bottom' in position_lower:
            top = max_top
        else:  # center 或其他默认居中
            top = max_top // 2
        
        return max(0, left), max(0, top)
    
    def crop_region(
        self, 
        left: int, 
        top: int, 
        right: int, 
        bottom: int
    ) -> Image.Image:
        """
        通过坐标区域裁剪图像
        
        Args:
            left: 左边距
            top: 顶边距
            right: 右边距
            bottom: 底边距
        
        Returns:
            裁剪后的图像对象
        """
        # 确保坐标在有效范围内
        left = max(0, min(left, self.original_width))
        right = max(0, min(right, self.original_width))
        top = max(0, min(top, self.original_height))
        bottom = max(0, min(bottom, self.original_height))
        
        # 确保裁剪区域有效
        if right <= left or bottom <= top:
            raise ValueError("裁剪区域无效：右边界必须大于左边界，下边界必须大于上边界")
        
        return self.image.crop((left, top, right, bottom))
    
    def smart_crop(
        self, 
        target_width: int, 
        target_height: int
    ) -> Image.Image:
        """
        智能裁剪 - 自动检测图像主体并裁剪到目标尺寸
        
        Args:
            target_width: 目标宽度
            target_height: 目标高度
        
        Returns:
            裁剪后的图像对象
        """
        # 计算目标比例和当前比例
        target_ratio = target_width / target_height
        current_ratio = self.original_width / self.original_height
        
        if current_ratio > target_ratio:
            # 图像太宽，以高度为基准裁剪
            new_height = self.original_height
            new_width = int(new_height * target_ratio)
        else:
            # 图像太高，以宽度为基准裁剪
            new_width = self.original_width
            new_height = int(new_width / target_ratio)
        
        # 使用中心裁剪
        return self.crop_custom(new_width, new_height, 'center')
    
    def save(self, output_path: str, cropped_image: Image.Image, quality: int = 95):
        """
        保存裁剪后的图像
        
        Args:
            output_path: 输出文件路径
            cropped_image: 裁剪后的图像对象
            quality: JPEG 质量 (1-100)，默认 95
        """
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            cropped_image.save(output_path, 'JPEG', quality=quality)
        else:
            cropped_image.save(output_path)
    
    def close(self):
        """关闭图像，释放资源"""
        if hasattr(self, 'image'):
            self.image.close()


def crop_image(
    image_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    ratio: Optional[str] = None,
    position: str = 'center'
) -> str:
    """
    便捷函数：裁剪图像并保存
    
    Args:
        image_path: 输入图像路径
        output_path: 输出图像路径
        width: 目标宽度（与 height 配合使用）
        height: 目标高度（与 width 配合使用）
        ratio: 预设比例 ('1:1', '4:3', '16:9', '3:2', '2:3', '9:16')
        position: 裁剪位置
    
    Returns:
        输出文件路径
    
    Raises:
        ValueError: 参数无效时抛出
    """
    cropper = Cropper(image_path)
    
    try:
        if ratio:
            # 使用预设比例裁剪
            result = cropper.crop_by_ratio(ratio, position)
        elif width and height:
            # 使用自定义尺寸裁剪
            result = cropper.crop_custom(width, height, position)
        else:
            raise ValueError("必须提供 ratio 或 (width 和 height) 参数")
        
        cropper.save(output_path, result)
        return output_path
    finally:
        cropper.close()
