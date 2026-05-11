"""
功能模块 - 各种图像处理功能
提供裁剪、水印、缩放、旋转、滤镜、GIF制作、批量重命名和PDF转换等功能
"""

from .crop import Cropper, crop_image
from .watermark import Watermarker, add_text_watermark, add_image_watermark, add_tiled_watermark
from .resize import ImageResizer, resize_image, resize_multiple_images
from .rotate import ImageRotator, rotate_image, flip_image, rotate_multiple_images
from .filter import ImageFilterProcessor, apply_brightness, apply_contrast, apply_saturation, apply_grayscale, apply_blur, apply_sharpen
from .gif_maker import GIFMaker, create_gif, images_to_gif, create_animated_gif, extract_frames, get_gif_info
from .rename import BatchRenamer, batch_rename, add_prefix_to_files, add_suffix_to_files, sequential_rename, rename_with_date
from .pdf_converter import PDFConverter, images_to_pdf, single_image_to_pdf, images_to_grid_pdf, directory_to_pdf, get_available_page_sizes

__all__ = [
    # 裁剪模块
    'Cropper',
    'crop_image',

    # 水印模块
    'Watermarker',
    'add_text_watermark',
    'add_image_watermark',
    'add_tiled_watermark',

    # 缩放模块
    'ImageResizer',
    'resize_image',
    'resize_multiple_images',

    # 旋转翻转模块
    'ImageRotator',
    'rotate_image',
    'flip_image',
    'rotate_multiple_images',

    # 滤镜模块
    'ImageFilterProcessor',
    'apply_brightness',
    'apply_contrast',
    'apply_saturation',
    'apply_grayscale',
    'apply_blur',
    'apply_sharpen',

    # GIF制作模块
    'GIFMaker',
    'create_gif',
    'images_to_gif',
    'create_animated_gif',
    'extract_frames',
    'get_gif_info',

    # 批量重命名模块
    'BatchRenamer',
    'batch_rename',
    'add_prefix_to_files',
    'add_suffix_to_files',
    'sequential_rename',
    'rename_with_date',

    # PDF转换模块
    'PDFConverter',
    'images_to_pdf',
    'single_image_to_pdf',
    'images_to_grid_pdf',
    'directory_to_pdf',
    'get_available_page_sizes',
]
