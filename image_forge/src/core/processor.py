"""
Pillow 图像处理引擎

该模块使用 Pillow (PIL) 库进行本地图像处理，
支持裁剪、缩放、旋转、翻转、亮度/对比度/饱和度调整、
灰度转换、模糊和锐化等常用图像处理操作。
"""

import os
from pathlib import Path
from typing import Optional, Tuple, Union, List
from enum import Enum
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class FlipDirection(Enum):
    """翻转方向枚举"""
    HORIZONTAL = 'horizontal'  # 水平翻转（左右镜像）
    VERTICAL = 'vertical'      # 垂直翻转（上下镜像）
    BOTH = 'both'              # 同时水平和垂直翻转


class ImageProcessor:
    """Pillow 图像处理引擎类"""

    def __init__(self):
        """初始化图像处理器"""
        pass

    def open_image(self, file_path: Union[str, Path]) -> Optional[Image.Image]:
        """
        打开图像文件

        Args:
            file_path: 图像文件路径

        Returns:
            PIL Image 对象，失败返回 None
        """
        try:
            return Image.open(file_path)
        except Exception as e:
            print(f"打开图像失败: {e}")
            return None

    def save_image(
        self,
        image: Image.Image,
        output_path: Union[str, Path],
        quality: int = 95,
        format: Optional[str] = None
    ) -> bool:
        """
        保存图像到文件

        Args:
            image: PIL Image 对象
            output_path: 输出文件路径
            quality: 图像质量 (1-100)
            format: 输出格式，如果为 None 则根据文件扩展名自动确定

        Returns:
            是否保存成功
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 确定保存格式
            if format is None:
                format = output_path.suffix.lower().strip('.')

            # JPEG 格式需要 RGB 模式
            if format in ('jpg', 'jpeg') and image.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = background
            elif format == 'png' and image.mode == 'RGB':
                image = image.convert('RGBA')

            # 根据格式设置保存参数
            save_kwargs = {}
            if format in ('jpg', 'jpeg'):
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif format == 'webp':
                save_kwargs['quality'] = quality
            elif format == 'png':
                # PNG 压缩级别
                save_kwargs['optimize'] = True

            image.save(str(output_path), format=format.upper() if format else None, **save_kwargs)
            return True

        except Exception as e:
            print(f"保存图像失败: {e}")
            return False

    def crop(
        self,
        image: Image.Image,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> Optional[Image.Image]:
        """
        裁剪图像

        Args:
            image: PIL Image 对象
            x: 裁剪区域左上角 x 坐标
            y: 裁剪区域左上角 y 坐标
            width: 裁剪区域宽度
            height: 裁剪区域高度

        Returns:
            裁剪后的图像，失败返回 None
        """
        try:
            # 验证参数
            if x < 0 or y < 0 or width <= 0 or height <= 0:
                print("裁剪参数无效")
                return None

            # 确保裁剪区域在图像范围内
            img_width, img_height = image.size
            x = min(x, img_width)
            y = min(y, img_height)
            width = min(width, img_width - x)
            height = min(height, img_height - y)

            if width <= 0 or height <= 0:
                print("裁剪区域无效")
                return None

            # 执行裁剪: (left, top, right, bottom)
            return image.crop((x, y, x + width, y + height))

        except Exception as e:
            print(f"裁剪失败: {e}")
            return None

    def resize(
        self,
        image: Image.Image,
        width: int,
        height: int,
        keep_aspect_ratio: bool = False,
        resample: int = Image.LANCZOS
    ) -> Optional[Image.Image]:
        """
        缩放图像

        Args:
            image: PIL Image 对象
            width: 目标宽度
            height: 目标高度
            keep_aspect_ratio: 是否保持宽高比，默认为 False
            resample: 重采样滤镜，默认为 LANCZOS

        Returns:
            缩放后的图像，失败返回 None
        """
        try:
            if keep_aspect_ratio:
                # 保持宽高比缩放
                image.thumbnail((width, height), resample)
                return image
            else:
                # 拉伸缩放
                return image.resize((width, height), resample)

        except Exception as e:
            print(f"缩放失败: {e}")
            return None

    def rotate(
        self,
        image: Image.Image,
        angle: float,
        expand: bool = True,
        fillcolor: Optional[Tuple[int, int, int]] = None
    ) -> Optional[Image.Image]:
        """
        旋转图像

        Args:
            image: PIL Image 对象
            angle: 旋转角度（度），正值逆时针，负值顺时针
            expand: 是否扩展画布以容纳旋转后的图像，默认为 True
            fillcolor: 填充颜色，默认为 None（透明）

        Returns:
            旋转后的图像，失败返回 None
        """
        try:
            # 归一化角度到 0-360 范围
            angle = angle % 360

            # 处理填充颜色
            if fillcolor is None and image.mode in ('RGBA', 'LA'):
                fillcolor = (0, 0, 0, 0)  # 透明
            elif fillcolor is None:
                fillcolor = (0, 0, 0)  # 黑色

            return image.rotate(angle, expand=expand, fillcolor=fillcolor, resample=Image.BICUBIC)

        except Exception as e:
            print(f"旋转失败: {e}")
            return None

    def flip(
        self,
        image: Image.Image,
        direction: Union[FlipDirection, str]
    ) -> Optional[Image.Image]:
        """
        翻转图像

        Args:
            image: PIL Image 对象
            direction: 翻转方向，可以是 FlipDirection 枚举或字符串

        Returns:
            翻转后的图像，失败返回 None
        """
        try:
            # 处理字符串输入
            if isinstance(direction, str):
                if direction.lower() in ('h', 'horizontal', 'horizontally'):
                    direction = FlipDirection.HORIZONTAL
                elif direction.lower() in ('v', 'vertical', 'vertically'):
                    direction = FlipDirection.VERTICAL
                elif direction.lower() in ('both', 'b', 'hv', 'vh'):
                    direction = FlipDirection.BOTH
                else:
                    print(f"未知的翻转方向: {direction}")
                    return None

            if direction == FlipDirection.HORIZONTAL:
                return image.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == FlipDirection.VERTICAL:
                return image.transpose(Image.FLIP_TOP_BOTTOM)
            elif direction == FlipDirection.BOTH:
                return image.transpose(Image.ROTATE_180)

        except Exception as e:
            print(f"翻转失败: {e}")
            return None

    def adjust_brightness_contrast_saturation(
        self,
        image: Image.Image,
        brightness: float = 1.0,
        contrast: float = 1.0,
        saturation: float = 1.0
    ) -> Optional[Image.Image]:
        """
        调整图像的亮度、对比度和饱和度

        Args:
            image: PIL Image 对象
            brightness: 亮度因子，1.0 表示不变，0.5 为一半亮度，2.0 为两倍亮度
            contrast: 对比度因子，1.0 表示不变，0.5 为降低对比度，2.0 为增强对比度
            saturation: 饱和度因子，1.0 表示不变，0.5 为灰度化，2.0 为增强饱和度

        Returns:
            调整后的图像，失败返回 None
        """
        try:
            # 确保图像在 RGB 或 RGBA 模式
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGB')

            result = image

            # 调整亮度
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(result)
                result = enhancer.enhance(brightness)

            # 调整对比度
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(result)
                result = enhancer.enhance(contrast)

            # 调整饱和度（仅对 RGB 有效）
            if saturation != 1.0:
                if result.mode == 'RGBA':
                    # 分离通道，调整饱和度，再合并
                    r, g, b, a = result.split()
                    rgb = Image.merge('RGB', (r, g, b))
                    enhancer = ImageEnhance.Color(rgb)
                    rgb = enhancer.enhance(saturation)
                    result = Image.merge('RGBA', (*rgb.split(), a))
                else:
                    enhancer = ImageEnhance.Color(result)
                    result = enhancer.enhance(saturation)

            return result

        except Exception as e:
            print(f"调整亮度/对比度/饱和度失败: {e}")
            return None

    def apply_gray(self, image: Image.Image, mode: str = 'L') -> Optional[Image.Image]:
        """
        将图像转换为灰度图

        Args:
            image: PIL Image 对象
            mode: 灰度模式，'L' 为灰度（0-255），'LA' 为灰度+透明通道

        Returns:
            灰度图像，失败返回 None
        """
        try:
            if mode == 'L':
                return image.convert('L')
            elif mode == 'LA':
                return image.convert('LA')
            elif mode == 'RGB':
                # 转为灰度后再转回 RGB（灰度伪彩色）
                gray = image.convert('L')
                return gray.convert('RGB')
            else:
                print(f"不支持的灰度模式: {mode}")
                return None

        except Exception as e:
            print(f"灰度转换失败: {e}")
            return None

    def apply_blur(
        self,
        image: Image.Image,
        radius: float = 2.0,
        method: str = 'gaussian'
    ) -> Optional[Image.Image]:
        """
        对图像应用模糊效果

        Args:
            image: PIL Image 对象
            radius: 模糊半径，值越大越模糊
            method: 模糊方法，可选 'gaussian'（高斯模糊）或 'box'（盒子模糊）

        Returns:
            模糊后的图像，失败返回 None
        """
        try:
            if radius <= 0:
                return image.copy()

            if method == 'gaussian':
                return image.filter(ImageFilter.GaussianBlur(radius=radius))
            elif method == 'box':
                # 盒子模糊的半径需要是整数
                return image.filter(ImageFilter.BLUR)
            elif method == 'median':
                # 中值模糊
                return image.filter(ImageFilter.MedianFilter(size=int(radius) * 2 + 1))
            elif method == 'smooth':
                # 平滑模糊
                return image.filter(ImageFilter.SMOOTH_MORE)
            else:
                # 默认使用高斯模糊
                return image.filter(ImageFilter.GaussianBlur(radius=radius))

        except Exception as e:
            print(f"模糊处理失败: {e}")
            return None

    def apply_sharpen(
        self,
        image: Image.Image,
        factor: float = 1.5,
        method: str = 'detail'
    ) -> Optional[Image.Image]:
        """
        对图像应用锐化效果

        Args:
            image: PIL Image 对象
            factor: 锐化强度因子，1.0 表示不变，大于 1.0 表示锐化
            method: 锐化方法，可选 'detail'（细节增强）、'edge'（边缘增强）

        Returns:
            锐化后的图像，失败返回 None
        """
        try:
            if factor <= 1.0:
                return image.copy()

            if method == 'detail':
                # 细节增强
                enhancer = ImageEnhance.Sharpness(image)
                return enhancer.enhance(factor)
            elif method == 'edge':
                # 边缘增强（先USM锐化）
                from PIL import ImageFilter
                return image.filter(ImageFilter.UnsharpMask(radius=2, percent=int(factor * 50), threshold=3))
            elif method == 'smooth':
                # 平滑（锐化的反效果）
                enhancer = ImageEnhance.Sharpness(image)
                return enhancer.enhance(1.0 / factor)
            else:
                # 默认使用细节增强
                enhancer = ImageEnhance.Sharpness(image)
                return enhancer.enhance(factor)

        except Exception as e:
            print(f"锐化处理失败: {e}")
            return None

    def batch_process(
        self,
        file_paths: List[Union[str, Path]],
        output_dir: Union[str, Path],
        process_func,
        **kwargs
    ) -> Tuple[int, int, List[str]]:
        """
        批量处理图像

        Args:
            file_paths: 输入文件路径列表
            output_dir: 输出目录路径
            process_func: 处理函数，接受 Image 对象和 kwargs，返回处理后的 Image 对象
            **kwargs: 传递给处理函数的其他参数

        Returns:
            (成功数量, 失败数量, 错误消息列表) 元组
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        fail_count = 0
        errors = []

        for file_path in file_paths:
            try:
                file_path = Path(file_path)

                # 打开图像
                image = self.open_image(file_path)
                if image is None:
                    errors.append(f"{file_path.name}: 无法打开图像")
                    fail_count += 1
                    continue

                # 执行处理
                processed = process_func(image, **kwargs)
                if processed is None:
                    errors.append(f"{file_path.name}: 处理失败")
                    fail_count += 1
                    continue

                # 保存结果
                output_path = output_dir / file_path.name
                if self.save_image(processed, output_path):
                    success_count += 1
                else:
                    errors.append(f"{file_path.name}: 保存失败")
                    fail_count += 1

            except Exception as e:
                errors.append(f"{file_path.name}: {str(e)}")
                fail_count += 1

        return success_count, fail_count, errors
