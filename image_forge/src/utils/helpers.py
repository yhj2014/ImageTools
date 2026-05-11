"""
辅助函数模块 - 提供常用的文件操作、路径处理和图片信息获取功能

功能特性:
- 文件操作 (读取、写入、复制、移动、删除)
- 路径处理 (归一化、相对路径、绝对路径)
- 文件格式检测 (基于扩展名和文件头)
- 文件大小格式化 (B, KB, MB, GB 等)
- 图片信息获取 (尺寸、格式、文件大小、颜色模式)
- EXIF 信息读取和解析

使用方法:
    # 文件操作
    from utils.helpers import FileHelper
    
    content = FileHelper.read('test.txt')
    FileHelper.write('output.txt', 'Hello World')
    FileHelper.copy('source.txt', 'dest.txt')
    
    # 路径处理
    from utils.helpers import PathHelper
    
    abs_path = PathHelper.normalize('relative/path')
    rel_path = PathHelper.relative('/home/user/file.txt', '/home/user')
    
    # 图片信息
    from utils.helpers import ImageHelper
    
    info = ImageHelper.get_info('image.png')
    print(f"尺寸: {info['width']}x{info['height']}")
    exif = ImageHelper.get_exif('photo.jpg')
"""

import os
import shutil
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union
from datetime import datetime

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class FileHelper:
    """
    文件操作辅助类
    
    提供常用的文件读写、复制、移动、删除等功能
    """
    
    # 支持的图片格式
    IMAGE_EXTENSIONS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.ico', '.ppm', '.pgm', '.pbm', '.pnm'
    }
    
    # 支持的视频格式
    VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'
    }
    
    # 支持的文档格式
    DOCUMENT_EXTENSIONS = {
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'
    }
    
    @staticmethod
    def read(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        读取文本文件内容
        
        Args:
            file_path: 文件路径
            encoding: 文本编码,默认为 UTF-8
            
        Returns:
            str: 文件内容
            
        Raises:
            FileNotFoundError: 文件不存在
            IOError: 读取失败
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def read_bytes(file_path: Union[str, Path]) -> bytes:
        """
        以二进制模式读取文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bytes: 文件内容
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(path, 'rb') as f:
            return f.read()
    
    @staticmethod
    def write(
        file_path: Union[str, Path],
        content: str,
        encoding: str = 'utf-8',
        create_dirs: bool = True
    ) -> bool:
        """
        写入文本内容到文件
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            encoding: 文本编码,默认为 UTF-8
            create_dirs: 是否创建目录,默认为 True
            
        Returns:
            bool: 是否成功写入
        """
        path = Path(file_path)
        
        # 创建父目录
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except IOError as e:
            print(f"写入文件失败: {e}")
            return False
    
    @staticmethod
    def write_bytes(file_path: Union[str, Path], content: bytes) -> bool:
        """
        以二进制模式写入内容到文件
        
        Args:
            file_path: 文件路径
            content: 要写入的二进制内容
            
        Returns:
            bool: 是否成功写入
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'wb') as f:
                f.write(content)
            return True
        except IOError as e:
            print(f"写入文件失败: {e}")
            return False
    
    @staticmethod
    def copy(
        src: Union[str, Path],
        dst: Union[str, Path],
        overwrite: bool = False
    ) -> bool:
        """
        复制文件或目录
        
        Args:
            src: 源路径
            dst: 目标路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            bool: 是否成功复制
        """
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            print(f"源文件不存在: {src}")
            return False
        
        # 创建目标目录
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if src_path.is_dir():
                # 复制目录
                if dst_path.exists() and not overwrite:
                    dst_path = dst_path / src_path.name
                shutil.copytree(src_path, dst_path, dirs_exist_ok=overwrite)
            else:
                # 复制文件
                if dst_path.exists() and not overwrite:
                    dst_path = dst_path.parent / f"{dst_path.stem}_copy{dst_path.suffix}"
                shutil.copy2(src_path, dst_path)
            return True
        except (IOError, shutil.Error) as e:
            print(f"复制失败: {e}")
            return False
    
    @staticmethod
    def move(src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False) -> bool:
        """
        移动文件或目录
        
        Args:
            src: 源路径
            dst: 目标路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            bool: 是否成功移动
        """
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            print(f"源文件不存在: {src}")
            return False
        
        # 创建目标目录
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果目标已存在且不是目录
        if dst_path.exists() and not dst_path.is_dir():
            if overwrite:
                dst_path.unlink()
            else:
                dst_path = dst_path.parent / f"{dst_path.stem}_moved{dst_path.suffix}"
        
        try:
            shutil.move(str(src_path), str(dst_path))
            return True
        except (IOError, shutil.Error) as e:
            print(f"移动失败: {e}")
            return False
    
    @staticmethod
    def delete(file_path: Union[str, Path], use_trash: bool = False) -> bool:
        """
        删除文件或目录
        
        Args:
            file_path: 要删除的路径
            use_trash: 是否移动到回收站(如果支持)
            
        Returns:
            bool: 是否成功删除
        """
        path = Path(file_path)
        
        if not path.exists():
            return True  # 文件不存在,认为删除成功
        
        try:
            if use_trash:
                # 尝试使用 send2trash(如果可用)
                try:
                    import send2trash
                    send2trash.send2trash(str(path))
                except ImportError:
                    # 回退到直接删除
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
            else:
                # 直接删除
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            return True
        except (IOError, OSError) as e:
            print(f"删除失败: {e}")
            return False
    
    @staticmethod
    def exists(file_path: Union[str, Path]) -> bool:
        """
        检查文件或目录是否存在
        
        Args:
            file_path: 要检查的路径
            
        Returns:
            bool: 是否存在
        """
        return Path(file_path).exists()
    
    @staticmethod
    def get_size(file_path: Union[str, Path]) -> int:
        """
        获取文件大小(字节)
        
        Args:
            file_path: 文件路径
            
        Returns:
            int: 文件大小,文件不存在返回 0
        """
        path = Path(file_path)
        
        if not path.exists():
            return 0
        
        if path.is_dir():
            # 计算目录总大小
            total = 0
            for item in path.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
            return total
        
        return path.stat().st_size
    
    @staticmethod
    def get_mtime(file_path: Union[str, Path]) -> Optional[datetime]:
        """
        获取文件修改时间
        
        Args:
            file_path: 文件路径
            
        Returns:
            datetime: 修改时间,文件不存在返回 None
        """
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        timestamp = path.stat().st_mtime
        return datetime.fromtimestamp(timestamp)
    
    @staticmethod
    def list_files(
        directory: Union[str, Path],
        pattern: str = '*',
        recursive: bool = False
    ) -> List[Path]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件名匹配模式(glob)
            recursive: 是否递归搜索子目录
            
        Returns:
            List[Path]: 文件路径列表
        """
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        
        if recursive:
            return sorted([p for p in dir_path.rglob(pattern) if p.is_file()])
        else:
            return sorted([p for p in dir_path.glob(pattern) if p.is_file()])
    
    @staticmethod
    def list_dirs(
        directory: Union[str, Path],
        recursive: bool = False
    ) -> List[Path]:
        """
        列出目录中的子目录
        
        Args:
            directory: 目录路径
            recursive: 是否递归搜索子目录
            
        Returns:
            List[Path]: 子目录路径列表
        """
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        
        if recursive:
            return sorted([p for p in dir_path.rglob('*') if p.is_dir()])
        else:
            return sorted([p for p in dir_path.glob('*') if p.is_dir()])


class PathHelper:
    """
    路径处理辅助类
    
    提供路径归一化、相对路径转换等功能
    """
    
    @staticmethod
    def normalize(path: Union[str, Path]) -> Path:
        """
        归一化路径
        
        解析 . 和 .. ,转换为绝对路径
        
        Args:
            path: 要归一化的路径
            
        Returns:
            Path: 归一化后的路径对象
        """
        return Path(path).resolve()
    
    @staticmethod
    def is_absolute(path: Union[str, Path]) -> bool:
        """
        检查路径是否为绝对路径
        
        Args:
            path: 要检查的路径
            
        Returns:
            bool: 是否为绝对路径
        """
        return Path(path).is_absolute()
    
    @staticmethod
    def relative(path: Union[str, Path], start: Optional[Union[str, Path]] = None) -> Path:
        """
        获取相对路径
        
        Args:
            path: 目标路径
            start: 起始路径,默认为当前目录
            
        Returns:
            Path: 相对路径
        """
        if start is None:
            start = Path.cwd()
        
        path = Path(path)
        start = Path(start)
        
        try:
            return path.relative_to(start)
        except ValueError:
            # 如果无法计算相对路径,返回绝对路径
            return path.resolve()
    
    @staticmethod
    def absolute(path: Union[str, Path], base: Optional[Union[str, Path]] = None) -> Path:
        """
        转换为绝对路径
        
        Args:
            path: 路径
            base: 基础目录(如果 path 是相对路径)
            
        Returns:
            Path: 绝对路径
        """
        path = Path(path)
        
        if path.is_absolute():
            return path.resolve()
        
        if base is not None:
            return (Path(base) / path).resolve()
        
        return path.resolve()
    
    @staticmethod
    def join(*paths: Union[str, Path]) -> Path:
        """
        连接多个路径组件
        
        Args:
            *paths: 路径组件
            
        Returns:
            Path: 连接后的路径
        """
        result = Path(paths[0]) if paths else Path()
        
        for p in paths[1:]:
            result = result / p
        
        return result
    
    @staticmethod
    def get_extension(path: Union[str, Path]) -> str:
        """
        获取文件扩展名
        
        Args:
            path: 文件路径
            
        Returns:
            str: 扩展名(包含点号),如 '.png'
        """
        return Path(path).suffix.lower()
    
    @staticmethod
    def get_stem(path: Union[str, Path]) -> str:
        """
        获取文件名(不含扩展名)
        
        Args:
            path: 文件路径
            
        Returns:
            str: 文件名(不含扩展名)
        """
        return Path(path).stem
    
    @staticmethod
    def get_name(path: Union[str, Path]) -> str:
        """
        获取文件名(含扩展名)
        
        Args:
            path: 文件路径
            
        Returns:
            str: 文件名(含扩展名)
        """
        return Path(path).name
    
    @staticmethod
    def get_parent(path: Union[str, Path]) -> Path:
        """
        获取父目录
        
        Args:
            path: 文件或目录路径
            
        Returns:
            Path: 父目录路径
        """
        return Path(path).parent
    
    @staticmethod
    def change_extension(path: Union[str, Path], new_ext: str) -> Path:
        """
        更改文件扩展名
        
        Args:
            path: 原文件路径
            new_ext: 新扩展名(可以带或不带点号)
            
        Returns:
            Path: 新文件路径
        """
        path = Path(path)
        
        # 确保新扩展名以点开头
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        
        return path.with_suffix(new_ext)


class FormatHelper:
    """
    格式检测辅助类
    
    提供文件格式检测功能
    """
    
    # 图片文件头标识(Magic Numbers)
    IMAGE_HEADERS = {
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xff\xd8\xff',
        'gif87a': b'GIF87a',
        'gif89a': b'GIF89a',
        'bmp': b'BM',
        'tiff_le': b'II\x2a\x00',  # Little-endian
        'tiff_be': b'MM\x00\x2a',  # Big-endian
        'webp': b'RIFF',
        'ico': b'\x00\x00\x01\x00',
    }
    
    @staticmethod
    def is_image(file_path: Union[str, Path]) -> bool:
        """
        检查文件是否为图片
        
        通过扩展名和文件头双重检测
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为图片文件
        """
        path = Path(file_path)
        
        # 首先检查扩展名
        if path.suffix.lower() in FileHelper.IMAGE_EXTENSIONS:
            return True
        
        # 检查文件头
        return FormatHelper._check_image_header(path)
    
    @staticmethod
    def _check_image_header(file_path: Path) -> bool:
        """
        通过文件头检测图片格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为已知的图片格式
        """
        if not file_path.exists() or file_path.stat().st_size < 12:
            return False
        
        try:
            with open(file_path, 'rb') as f:
                header = f.read(12)
            
            # 检查所有已知的图片文件头
            for magic in FormatHelper.IMAGE_HEADERS.values():
                if header.startswith(magic):
                    return True
            
            return False
        except (IOError, OSError):
            return False
    
    @staticmethod
    def get_format(file_path: Union[str, Path]) -> str:
        """
        获取文件格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件格式(扩展名),未知返回空字符串
        """
        path = Path(file_path)
        
        # 优先使用扩展名
        if path.suffix.lower():
            return path.suffix.lower()[1:]  # 去掉点号
        
        # 尝试通过文件头检测
        if path.exists() and path.stat().st_size >= 12:
            try:
                with open(path, 'rb') as f:
                    header = f.read(12)
                
                for fmt, magic in FormatHelper.IMAGE_HEADERS.items():
                    if header.startswith(magic):
                        # 特殊处理 RIFF(可能是 WebP)
                        if fmt == 'webp':
                            # WebP 需要检查更多字节
                            f.seek(0)
                            riff_header = f.read(16)
                            if riff_header[8:12] == b'WEBP':
                                return 'webp'
                        else:
                            return fmt
            except (IOError, OSError):
                pass
        
        return ''
    
    @staticmethod
    def get_mime_type(file_path: Union[str, Path]) -> str:
        """
        获取文件的 MIME 类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: MIME 类型,未知返回 'application/octet-stream'
        """
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'
    
    @staticmethod
    def is_video(file_path: Union[str, Path]) -> bool:
        """
        检查文件是否为视频
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为视频文件
        """
        return Path(file_path).suffix.lower() in FileHelper.VIDEO_EXTENSIONS
    
    @staticmethod
    def is_document(file_path: Union[str, Path]) -> bool:
        """
        检查文件是否为文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为文档文件
        """
        return Path(file_path).suffix.lower() in FileHelper.DOCUMENT_EXTENSIONS


class SizeHelper:
    """
    文件大小格式化辅助类
    
    提供人类可读的文件大小格式化功能
    """
    
    # 大小单位列表
    UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    # 单位转换基数
    BASE = 1024
    
    @staticmethod
    def format_size(size_bytes: int, precision: int = 2) -> str:
        """
        格式化文件大小
        
        Args:
            size_bytes: 文件大小(字节)
            precision: 小数精度,默认为 2
            
        Returns:
            str: 格式化后的大小字符串,如 '1.23 MB'
        """
        if size_bytes < 0:
            return '0 B'
        
        for unit in SizeHelper.UNITS:
            if size_bytes < SizeHelper.BASE:
                if unit == 'B':
                    return f"{size_bytes} {unit}"
                return f"{size_bytes:.{precision}f} {unit}"
            size_bytes /= SizeHelper.BASE
        
        # 超过 PB,使用最后一个单位
        return f"{size_bytes:.{precision}f} {SizeHelper.UNITS[-1]}"
    
    @staticmethod
    def parse_size(size_str: str) -> int:
        """
        解析大小字符串为字节数
        
        Args:
            size_str: 大小字符串,如 '1.5 MB', '2GB'
            
        Returns:
            int: 字节数,解析失败返回 0
        """
        if not size_str:
            return 0
        
        size_str = size_str.strip().upper()
        
        # 提取数字和单位
        import re
        match = re.match(r'([\d.]+)\s*([A-Z]*)', size_str)
        
        if not match:
            return 0
        
        try:
            value = float(match.group(1))
            unit = match.group(2)
            
            # 标准化单位
            if unit == '' or unit == 'B':
                return int(value)
            elif unit == 'K' or unit == 'KB':
                return int(value * SizeHelper.BASE)
            elif unit == 'M' or unit == 'MB':
                return int(value * SizeHelper.BASE ** 2)
            elif unit == 'G' or unit == 'GB':
                return int(value * SizeHelper.BASE ** 3)
            elif unit == 'T' or unit == 'TB':
                return int(value * SizeHelper.BASE ** 4)
            elif unit == 'P' or unit == 'PB':
                return int(value * SizeHelper.BASE ** 5)
            else:
                return 0
        except (ValueError, AttributeError):
            return 0


class ImageHelper:
    """
    图片信息辅助类
    
    提供图片尺寸、格式、EXIF 信息获取功能
    """
    
    # 支持的图片格式
    SUPPORTED_FORMATS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico'}
    
    @staticmethod
    def is_supported(file_path: Union[str, Path]) -> bool:
        """
        检查图片格式是否支持
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持
        """
        if not HAS_PIL:
            return False
        
        path = Path(file_path)
        ext = path.suffix.lower().lstrip('.')
        
        return ext in ImageHelper.SUPPORTED_FORMATS
    
    @staticmethod
    def get_info(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        获取图片基本信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict: 包含图片信息的字典,获取失败返回 None
                - width: 宽度(像素)
                - height: 高度(像素)
                - format: 图片格式
                - mode: 颜色模式(如 'RGB', 'RGBA', 'L')
                - size: 文件大小(字节)
                - size_formatted: 格式化的文件大小
        """
        if not HAS_PIL:
            print("Pillow 库未安装,无法获取图片信息")
            return None
        
        path = Path(file_path)
        
        if not path.exists():
            print(f"文件不存在: {file_path}")
            return None
        
        try:
            with Image.open(path) as img:
                info = {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format or FormatHelper.get_format(path),
                    'mode': img.mode,
                    'size': path.stat().st_size,
                    'size_formatted': SizeHelper.format_size(path.stat().st_size),
                    'path': str(path),
                    'name': path.name,
                }
                
                # 添加更多信息
                if hasattr(img, 'info'):
                    info['info'] = img.info
                
                return info
        except Exception as e:
            print(f"获取图片信息失败: {e}")
            return None
    
    @staticmethod
    def get_dimensions(file_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """
        获取图片尺寸
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Tuple[int, int]: (宽度, 高度),获取失败返回 None
        """
        if not HAS_PIL:
            return None
        
        path = Path(file_path)
        
        try:
            with Image.open(path) as img:
                return (img.width, img.height)
        except Exception:
            return None
    
    @staticmethod
    def get_exif(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        获取图片的 EXIF 信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict: EXIF 信息字典,获取失败返回 None
        """
        if not HAS_PIL:
            return None
        
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        try:
            with Image.open(path) as img:
                exif_data = img.getexif()
                
                if not exif_data:
                    return None
                
                # 解析 EXIF 标签
                exif_dict = {}
                
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, f'Unknown_{tag_id}')
                    exif_dict[tag_name] = value
                
                return exif_dict
        except Exception as e:
            print(f"获取 EXIF 信息失败: {e}")
            return None
    
    @staticmethod
    def get_gps_info(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        获取图片的 GPS 信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict: GPS 信息字典,获取失败返回 None
                - latitude: 纬度
                - longitude: 经度
                - altitude: 海拔(如果有)
        """
        if not HAS_PIL:
            return None
        
        path = Path(file_path)
        
        try:
            with Image.open(path) as img:
                exif_data = img.getexif()
                
                if not exif_data:
                    return None
                
                # 查找 GPS IFD
                gps_ifd = exif_data.get_ifd(0x8825)
                
                if not gps_ifd:
                    return None
                
                gps_dict = {}
                
                for tag_id, value in gps_ifd.items():
                    tag_name = GPSTAGS.get(tag_id, f'GPS_{tag_id}')
                    gps_dict[tag_name] = value
                
                # 解析经纬度
                latitude = gps_dict.get('GPSLatitude')
                latitude_ref = gps_dict.get('GPSLatitudeRef')
                longitude = gps_dict.get('GPSLongitude')
                longitude_ref = gps_dict.get('GPSLongitudeRef')
                altitude = gps_dict.get('GPSAltitude')
                
                if latitude and longitude:
                    lat = ImageHelper._convert_gps_coordinate(latitude)
                    lon = ImageHelper._convert_gps_coordinate(longitude)
                    
                    if latitude_ref == 'S':
                        lat = -lat
                    if longitude_ref == 'W':
                        lon = -lon
                    
                    result = {
                        'latitude': lat,
                        'longitude': lon,
                    }
                    
                    if altitude is not None:
                        result['altitude'] = float(altitude)
                    
                    return result
                
                return gps_dict if gps_dict else None
        except Exception:
            return None
    
    @staticmethod
    def _convert_gps_coordinate(coord: Tuple) -> float:
        """
        将 GPS 坐标(度分秒)转换为十进制度
        
        Args:
            coord: GPS 坐标元组 (度, 分, 秒)
            
        Returns:
            float: 十进制度
        """
        if not coord or len(coord) != 3:
            return 0.0
        
        degrees = float(coord[0])
        minutes = float(coord[1])
        seconds = float(coord[2])
        
        return degrees + minutes / 60 + seconds / 3600
    
    @staticmethod
    def get_color_mode(file_path: Union[str, Path]) -> Optional[str]:
        """
        获取图片颜色模式
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            str: 颜色模式(如 'RGB', 'RGBA', 'L'),获取失败返回 None
        """
        if not HAS_PIL:
            return None
        
        path = Path(file_path)
        
        try:
            with Image.open(path) as img:
                return img.mode
        except Exception:
            return None
    
    @staticmethod
    def get_thumbnail(
        file_path: Union[str, Path],
        max_size: Tuple[int, int] = (128, 128)
    ) -> Optional[Image.Image]:
        """
        获取图片缩略图
        
        Args:
            file_path: 图片文件路径
            max_size: 最大尺寸 (宽度, 高度)
            
        Returns:
            Image: 缩略图对象,获取失败返回 None
        """
        if not HAS_PIL:
            return None
        
        path = Path(file_path)
        
        try:
            with Image.open(path) as img:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                return img.copy()
        except Exception:
            return None
    
    @staticmethod
    def get_all_metadata(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        获取图片的所有元数据
        
        包含基本信息、EXIF 信息和格式特定的信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict: 包含所有元数据的字典,获取失败返回 None
        """
        if not HAS_PIL:
            return None
        
        result = {
            'basic': ImageHelper.get_info(file_path),
            'exif': ImageHelper.get_exif(file_path),
            'gps': ImageHelper.get_gps_info(file_path),
        }
        
        # 移除为 None 的项
        result = {k: v for k, v in result.items() if v is not None}
        
        return result if result else None


# 便捷函数
def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    获取文件的完整信息摘要
    
    Args:
        file_path: 文件路径
        
    Returns:
        Dict: 文件信息字典
    """
    path = Path(file_path)
    
    if not path.exists():
        return {'exists': False}
    
    info = {
        'exists': True,
        'is_file': path.is_file(),
        'is_dir': path.is_dir(),
        'name': path.name,
        'stem': path.stem,
        'suffix': path.suffix,
        'size': path.stat().st_size,
        'size_formatted': SizeHelper.format_size(path.stat().st_size),
        'modified': datetime.fromtimestamp(path.stat().st_mtime),
        'created': datetime.fromtimestamp(path.stat().st_ctime),
        'path': str(path),
        'absolute_path': str(path.resolve()),
    }
    
    # 如果是图片,添加图片信息
    if info['is_file']:
        info['is_image'] = FormatHelper.is_image(path)
        info['is_video'] = FormatHelper.is_video(path)
        info['is_document'] = FormatHelper.is_document(path)
        info['mime_type'] = FormatHelper.get_mime_type(path)
        
        if info['is_image']:
            img_info = ImageHelper.get_info(path)
            if img_info:
                info.update(img_info)
    
    return info


if __name__ == '__main__':
    # 测试辅助函数
    print("=" * 50)
    print("测试辅助函数模块")
    print("=" * 50)
    
    # 测试路径处理
    print("\n1. 测试路径处理:")
    test_path = './test/../file.txt'
    print(f"   原始路径: {test_path}")
    print(f"   归一化: {PathHelper.normalize(test_path)}")
    print(f"   获取扩展名: {PathHelper.get_extension(test_path)}")
    print(f"   获取文件名: {PathHelper.get_stem(test_path)}")
    
    # 测试文件大小格式化
    print("\n2. 测试文件大小格式化:")
    test_sizes = [0, 512, 1024, 1024 * 1024, 1024 * 1024 * 5.5]
    for size in test_sizes:
        print(f"   {size} 字节 = {SizeHelper.format_size(size)}")
    
    # 测试格式检测
    print("\n3. 测试格式检测:")
    print(f"   PNG 格式标识: {FormatHelper.IMAGE_HEADERS['png']}")
    print(f"   JPG 格式标识: {FormatHelper.IMAGE_HEADERS['jpg']}")
    
    # 测试 Pillow 可用性
    print("\n4. Pillow 库状态:")
    if HAS_PIL:
        print("   Pillow 已安装")
        
        # 尝试创建一个测试图片
        try:
            test_img_path = Path('/tmp/test_image.png')
            test_img = Image.new('RGB', (100, 100), color='red')
            test_img.save(test_img_path)
            
            # 测试获取图片信息
            info = ImageHelper.get_info(test_img_path)
            if info:
                print(f"   图片宽度: {info['width']}")
                print(f"   图片高度: {info['height']}")
                print(f"   图片格式: {info['format']}")
                print(f"   颜色模式: {info['mode']}")
            
            # 清理测试文件
            test_img_path.unlink()
            print("   图片信息测试通过")
        except Exception as e:
            print(f"   测试失败: {e}")
    else:
        print("   Pillow 未安装,部分功能不可用")
    
    print("\n" + "=" * 50)
    print("辅助函数模块测试完成!")
    print("=" * 50)
