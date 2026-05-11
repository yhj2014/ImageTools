"""
预设配置模块

该模块定义了各种图像处理的预设配置，
包括尺寸预设、比例预设、格式预设等。
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SizePreset(Enum):
    """
    尺寸预设枚举

    定义常用的图像尺寸预设。
    """
    SD_480P = ('480p', 640, 480, '标准清晰度 (480p)')
    HD_720P = ('720p', 1280, 720, '高清 (720p)')
    HD_800x600 = ('800x600', 800, 600, '标准 4:3 比例')
    HD_1024x768 = ('1024x768', 1024, 768, '标准 4:3 比例')
    FHD_1080P = ('1080p', 1920, 1080, '全高清 (1080p)')
    QHD_1440P = ('1440p', 2560, 1440, '2K 四高清')
    UHD_4K = ('4K', 3840, 2160, '超高清 4K')
    UHD_8K = ('8K', 7680, 4320, '超高清 8K')
    SQUARE_1K = ('1000x1000', 1000, 1000, '正方形 1:1')
    SQUARE_2K = ('2000x2000', 2000, 2000, '正方形 2K')

    def __init__(self, name: str, width: int, height: int, description: str):
        """初始化尺寸预设"""
        self._name = name
        self._width = width
        self._height = height
        self._description = description

    @property
    def name(self) -> str:
        """获取预设名称"""
        return self._name

    @property
    def width(self) -> int:
        """获取宽度"""
        return self._width

    @property
    def height(self) -> int:
        """获取高度"""
        return self._height

    @property
    def description(self) -> str:
        """获取描述"""
        return self._description

    def get_size(self) -> Tuple[int, int]:
        """获取 (宽度, 高度) 元组"""
        return (self._width, self._height)

    @classmethod
    def get_all_presets(cls) -> List['SizePreset']:
        """获取所有尺寸预设"""
        return list(cls)

    @classmethod
    def get_by_name(cls, name: str) -> Optional['SizePreset']:
        """根据名称获取预设"""
        for preset in cls:
            if preset.name == name:
                return preset
        return None

    @classmethod
    def get_by_size(cls, width: int, height: int) -> Optional['SizePreset']:
        """根据尺寸获取预设"""
        for preset in cls:
            if preset.width == width and preset.height == height:
                return preset
        return None


class AspectRatioPreset(Enum):
    """
    比例预设枚举

    定义常用的图像宽高比预设。
    """
    RATIO_1_1 = ('1:1', 1.0, '正方形')
    RATIO_4_3 = ('4:3', 4/3, '标准显示器')
    RATIO_3_2 = ('3:2', 3/2, '经典照片')
    RATIO_16_9 = ('16:9', 16/9, '宽屏/视频')
    RATIO_16_10 = ('16:10', 16/10, '宽屏显示器')
    RATIO_2_3 = ('2:3', 2/3, '人像照片')
    RATIO_9_16 = ('9:16', 9/16, '竖屏/手机')
    RATIO_21_9 = ('21:9', 21/9, '超宽屏')
    RATIO_3_4 = ('3:4', 3/4, '竖屏 4:3')
    RATIO_9_10 = ('9:10', 9/10, '手机比例')

    def __init__(self, name: str, ratio: float, description: str):
        """初始化比例预设"""
        self._name = name
        self._ratio = ratio
        self._description = description

    @property
    def name(self) -> str:
        """获取预设名称"""
        return self._name

    @property
    def ratio(self) -> float:
        """获取宽高比 (width/height)"""
        return self._ratio

    @property
    def description(self) -> str:
        """获取描述"""
        return self._description

    def get_size_by_height(self, height: int) -> Tuple[int, int]:
        """
        根据高度计算宽度

        Args:
            height: 高度值

        Returns:
            (宽度, 高度) 元组
        """
        width = int(height * self._ratio)
        return (width, height)

    def get_size_by_width(self, width: int) -> Tuple[int, int]:
        """
        根据宽度计算高度

        Args:
            width: 宽度值

        Returns:
            (宽度, 高度) 元组
        """
        height = int(width / self._ratio)
        return (width, height)

    def get_size_by_long_edge(self, long_edge: int) -> Tuple[int, int]:
        """
        根据长边计算尺寸（保持比例）

        Args:
            long_edge: 长边长度

        Returns:
            (宽度, 高度) 元组
        """
        if self._ratio >= 1.0:
            # 宽大于高，长边是宽度
            return (long_edge, int(long_edge / self._ratio))
        else:
            # 高大于宽，长边是高度
            return (int(long_edge * self._ratio), long_edge)

    @classmethod
    def get_all_presets(cls) -> List['AspectRatioPreset']:
        """获取所有比例预设"""
        return list(cls)

    @classmethod
    def get_by_name(cls, name: str) -> Optional['AspectRatioPreset']:
        """根据名称获取预设"""
        for preset in cls:
            if preset.name == name:
                return preset
        return None

    @classmethod
    def get_by_ratio(cls, ratio: float, tolerance: float = 0.01) -> Optional['AspectRatioPreset']:
        """
        根据比例获取预设

        Args:
            ratio: 宽高比
            tolerance: 容差，默认为 0.01

        Returns:
            对应的预设，如果没有匹配的返回 None
        """
        for preset in cls:
            if abs(preset.ratio - ratio) <= tolerance:
                return preset
        return None


class FormatPreset(Enum):
    """
    格式预设枚举

    定义图像输出格式的预设配置。
    """
    PNG_STANDARD = ('png', 'png', 95, '标准 PNG 格式，无损压缩')
    PNG_SMALL = ('png_small', 'png', 75, 'PNG 小文件，压缩率高')
    PNG_LARGE = ('png_large', 'png', 100, 'PNG 高质量，几乎无损')

    JPG_STANDARD = ('jpg_standard', 'jpg', 85, '标准 JPEG 格式')
    JPG_HIGH = ('jpg_high', 'jpg', 95, 'JPEG 高质量')
    JPG_WEB = ('jpg_web', 'jpg', 70, 'JPEG 网页优化')
    JPG_THUMB = ('jpg_thumb', 'jpg', 60, 'JPEG 缩略图')

    WEBP_STANDARD = ('webp_standard', 'webp', 80, '标准 WebP 格式')
    WEBP_HIGH = ('webp_high', 'webp', 90, 'WebP 高质量')
    WEBP_LOSSLESS = ('webp_lossless', 'webp', 100, 'WebP 无损格式')

    BMP_STANDARD = ('bmp', 'bmp', 100, 'BMP 位图格式')
    TIFF_STANDARD = ('tiff', 'tiff', 95, 'TIFF 格式')
    TIFF_COMPRESSED = ('tiff_compressed', 'tiff', 85, 'TIFF 压缩格式')
    GIF_ANIMATED = ('gif', 'gif', 100, 'GIF 格式')
    TGA_STANDARD = ('tga', 'tga', 100, 'TGA 格式')

    def __init__(self, name: str, format: str, quality: int, description: str):
        """初始化格式预设"""
        self._name = name
        self._format = format
        self._quality = quality
        self._description = description

    @property
    def name(self) -> str:
        """获取预设名称"""
        return self._name

    @property
    def format(self) -> str:
        """获取输出格式"""
        return self._format

    @property
    def quality(self) -> int:
        """获取质量值 (1-100)"""
        return self._quality

    @property
    def description(self) -> str:
        """获取描述"""
        return self._description

    def get_extension(self) -> str:
        """获取文件扩展名"""
        return f'.{self._format}'

    @classmethod
    def get_all_presets(cls) -> List['FormatPreset']:
        """获取所有格式预设"""
        return list(cls)

    @classmethod
    def get_by_format(cls, format: str) -> List['FormatPreset']:
        """获取指定格式的所有预设"""
        format = format.lower().strip('.')
        return [p for p in cls if p.format == format]

    @classmethod
    def get_by_name(cls, name: str) -> Optional['FormatPreset']:
        """根据名称获取预设"""
        for preset in cls:
            if preset.name == name:
                return preset
        return None


@dataclass
class ImagePreset:
    """
    综合图像预设数据类

    组合尺寸、比例和格式预设。
    """
    name: str
    width: int
    height: int
    format: str
    quality: int
    keep_aspect_ratio: bool = True
    description: str = ''


class PresetManager:
    """
    预设管理器类

    提供预设的查询、过滤和管理功能。
    """

    # 常用社交媒体预设
    SOCIAL_MEDIA_PRESETS = {
        'instagram_square': ImagePreset(
            name='Instagram 正方形',
            width=1080,
            height=1080,
            format='jpg',
            quality=90,
            keep_aspect_ratio=False,
            description='Instagram 正方形帖子'
        ),
        'instagram_portrait': ImagePreset(
            name='Instagram 竖版',
            width=1080,
            height=1350,
            format='jpg',
            quality=90,
            keep_aspect_ratio=False,
            description='Instagram 竖版帖子'
        ),
        'instagram_story': ImagePreset(
            name='Instagram 故事',
            width=1080,
            height=1920,
            format='jpg',
            quality=90,
            keep_aspect_ratio=False,
            description='Instagram 故事/Stories'
        ),
        'facebook_post': ImagePreset(
            name='Facebook 帖子',
            width=1200,
            height=630,
            format='jpg',
            quality=85,
            keep_aspect_ratio=False,
            description='Facebook 链接预览图'
        ),
        'twitter_post': ImagePreset(
            name='Twitter 帖子',
            width=1200,
            height=675,
            format='jpg',
            quality=85,
            keep_aspect_ratio=False,
            description='Twitter 图片帖子'
        ),
        'youtube_thumbnail': ImagePreset(
            name='YouTube 缩略图',
            width=1280,
            height=720,
            format='jpg',
            quality=90,
            keep_aspect_ratio=False,
            description='YouTube 视频缩略图'
        ),
        'wechat_moment': ImagePreset(
            name='微信朋友圈',
            width=1080,
            height=1080,
            format='jpg',
            quality=85,
            keep_aspect_ratio=False,
            description='微信朋友圈图片'
        ),
        'xiaohongshu': ImagePreset(
            name='小红书',
            width=1080,
            height=1430,
            format='jpg',
            quality=90,
            keep_aspect_ratio=False,
            description='小红书笔记图片'
        ),
    }

    # 常用文档预设
    DOCUMENT_PRESETS = {
        'a4_300dpi': ImagePreset(
            name='A4 300 DPI',
            width=2480,
            height=3508,
            format='png',
            quality=100,
            keep_aspect_ratio=True,
            description='A4 纸张 300 DPI'
        ),
        'a4_150dpi': ImagePreset(
            name='A4 150 DPI',
            width=1240,
            height=1754,
            format='png',
            quality=95,
            keep_aspect_ratio=True,
            description='A4 纸张 150 DPI'
        ),
        'letter_300dpi': ImagePreset(
            name='Letter 300 DPI',
            width=2550,
            height=3300,
            format='png',
            quality=100,
            keep_aspect_ratio=True,
            description='美国 Letter 纸张 300 DPI'
        ),
    }

    @classmethod
    def get_all_social_presets(cls) -> Dict[str, ImagePreset]:
        """获取所有社交媒体预设"""
        return cls.SOCIAL_MEDIA_PRESETS.copy()

    @classmethod
    def get_all_document_presets(cls) -> Dict[str, ImagePreset]:
        """获取所有文档预设"""
        return cls.DOCUMENT_PRESETS.copy()

    @classmethod
    def get_all_presets(cls) -> Dict[str, Dict[str, ImagePreset]]:
        """获取所有预设分类"""
        return {
            'social_media': cls.SOCIAL_MEDIA_PRESETS,
            'document': cls.DOCUMENT_PRESETS
        }

    @classmethod
    def get_preset(cls, category: str, name: str) -> Optional[ImagePreset]:
        """
        获取指定分类和名称的预设

        Args:
            category: 预设分类 ('social_media' 或 'document')
            name: 预设名称

        Returns:
            ImagePreset 对象，如果不存在返回 None
        """
        categories = cls.get_all_presets()
        if category in categories:
            return categories[category].get(name)
        return None

    @classmethod
    def create_custom_preset(
        cls,
        name: str,
        width: int,
        height: int,
        format: str = 'jpg',
        quality: int = 85,
        keep_aspect_ratio: bool = True,
        description: str = ''
    ) -> ImagePreset:
        """
        创建自定义预设

        Args:
            name: 预设名称
            width: 宽度
            height: 高度
            format: 输出格式
            quality: 质量
            keep_aspect_ratio: 是否保持宽高比
            description: 描述

        Returns:
            ImagePreset 对象
        """
        return ImagePreset(
            name=name,
            width=width,
            height=height,
            format=format.lower(),
            quality=quality,
            keep_aspect_ratio=keep_aspect_ratio,
            description=description
        )

    @classmethod
    def get_preset_display_list(cls) -> List[Dict[str, str]]:
        """
        获取预设显示列表（用于 UI 列表显示）

        Returns:
            包含预设信息的字典列表
        """
        result = []

        # 添加尺寸预设
        for preset in SizePreset.get_all_presets():
            result.append({
                'category': '尺寸',
                'name': preset.name,
                'display': f"{preset.name} ({preset.width}x{preset.height})",
                'description': preset.description,
                'width': preset.width,
                'height': preset.height
            })

        # 添加比例预设
        for preset in AspectRatioPreset.get_all_presets():
            result.append({
                'category': '比例',
                'name': preset.name,
                'display': f"{preset.name} - {preset.description}",
                'description': f"比例: {preset.ratio:.2f}",
                'ratio': preset.ratio
            })

        # 添加格式预设
        for preset in FormatPreset.get_all_presets():
            result.append({
                'category': '格式',
                'name': preset.name,
                'display': f"{preset.name} ({preset.format.upper()}, 质量 {preset.quality}%)",
                'description': preset.description,
                'format': preset.format,
                'quality': preset.quality
            })

        # 添加社交媒体预设
        for name, preset in cls.SOCIAL_MEDIA_PRESETS.items():
            result.append({
                'category': '社交媒体',
                'name': preset.name,
                'display': f"{preset.name} ({preset.width}x{preset.height})",
                'description': preset.description,
                'width': preset.width,
                'height': preset.height,
                'format': preset.format,
                'quality': preset.quality
            })

        # 添加文档预设
        for name, preset in cls.DOCUMENT_PRESETS.items():
            result.append({
                'category': '文档',
                'name': preset.name,
                'display': f"{preset.name} ({preset.width}x{preset.height})",
                'description': preset.description,
                'width': preset.width,
                'height': preset.height,
                'format': preset.format,
                'quality': preset.quality
            })

        return result


def get_size_presets_dict() -> Dict[str, Tuple[int, int]]:
    """
    获取尺寸预设字典（简化版本）

    Returns:
        名称到尺寸的字典
    """
    return {
        '800x600': (800, 600),
        '1024x768': (1024, 768),
        '1920x1080': (1920, 1080),
        '4K': (3840, 2160),
        '1280x720': (1280, 720),
        '2560x1440': (2560, 1440),
    }


def get_ratio_presets_dict() -> Dict[str, float]:
    """
    获取比例预设字典（简化版本）

    Returns:
        名称到比例的字典
    """
    return {
        '1:1': 1.0,
        '4:3': 4/3,
        '16:9': 16/9,
        '3:2': 3/2,
        '2:3': 2/3,
        '9:16': 9/16,
        '16:10': 16/10,
    }


def get_format_presets_dict() -> Dict[str, Tuple[str, int]]:
    """
    获取格式预设字典（简化版本）

    Returns:
        名称到 (格式, 质量) 的字典
    """
    return {
        'PNG 标准': ('png', 95),
        'PNG 高质量': ('png', 100),
        'JPEG 标准': ('jpg', 85),
        'JPEG 高质量': ('jpg', 95),
        'JPEG 网页': ('jpg', 70),
        'WebP 高质量': ('webp', 90),
        'WebP 标准': ('webp', 80),
        'BMP': ('bmp', 100),
        'TIFF': ('tiff', 95),
        'GIF': ('gif', 100),
        'TGA': ('tga', 100),
    }
