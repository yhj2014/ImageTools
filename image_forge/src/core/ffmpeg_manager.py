"""
FFmpeg 下载和管理器

该模块负责自动下载和管理 FFmpeg 静态二进制文件，
支持 Windows、Mac 和 Linux 三个平台。
"""

import os
import sys
import stat
import shutil
import zipfile
import tarfile
import platform
import urllib.request
from pathlib import Path
from typing import Optional, Tuple


class FFmpegManager:
    """FFmpeg 下载和管理器类"""

    # 各平台的 FFmpeg 下载 URL
    DOWNLOAD_URLS = {
        'windows': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'mac': 'https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip',
        'linux': 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64.tar.xz'
    }

    # 各平台的二进制文件名
    BINARY_NAMES = {
        'windows': 'ffmpeg.exe',
        'mac': 'ffmpeg',
        'linux': 'ffmpeg'
    }

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        初始化 FFmpeg 管理器

        Args:
            cache_dir: 缓存目录路径，默认为用户数据目录下的 ffmpeg_cache
        """
        # 确定缓存目录
        if cache_dir is None:
            # 使用用户数据目录
            if sys.platform == 'win32':
                base_dir = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
            elif sys.platform == 'darwin':
                base_dir = Path.home() / 'Library' / 'Application Support'
            else:
                base_dir = Path.home() / '.local' / 'share'

            cache_dir = base_dir / 'image_forge' / 'ffmpeg_cache'

        self.cache_dir = Path(cache_dir)
        self.platform_name = self._get_platform_name()
        self.binary_name = self.BINARY_NAMES.get(self.platform_name, 'ffmpeg')
        self.download_url = self.DOWNLOAD_URLS.get(self.platform_name)

    def _get_platform_name(self) -> str:
        """
        获取当前平台名称

        Returns:
            平台名称字符串: 'windows', 'mac' 或 'linux'
        """
        system = platform.system().lower()
        if system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'mac'
        else:
            return 'linux'

    def _get_binary_path(self) -> Path:
        """
        获取 FFmpeg 二进制文件的完整路径

        Returns:
            FFmpeg 二进制文件的路径
        """
        return self.cache_dir / self.binary_name

    def _get_version_file_path(self) -> Path:
        """
        获取版本信息文件路径

        Returns:
            版本信息文件路径
        """
        return self.cache_dir / 'version.txt'

    def is_installed(self) -> bool:
        """
        检查 FFmpeg 是否已安装

        Returns:
            如果已安装返回 True，否则返回 False
        """
        binary_path = self._get_binary_path()

        # 检查文件是否存在
        if not binary_path.exists():
            return False

        # 检查文件是否有执行权限（Linux/Mac）
        if self.platform_name != 'windows':
            file_stat = binary_path.stat()
            # 检查所有者执行权限
            if not (file_stat.st_mode & stat.S_IXUSR):
                return False

        # 尝试获取版本信息验证
        try:
            result = self.check_version()
            return result is not None
        except Exception:
            return False

    def check_version(self) -> Optional[str]:
        """
        检测 FFmpeg 版本

        Returns:
            FFmpeg 版本字符串，失败返回 None
        """
        if not self.is_installed():
            return None

        try:
            ffmpeg_path = self._get_binary_path()
            # 使用 -version 参数获取版本信息
            result = subprocess_run([str(ffmpeg_path), '-version'], capture_output=True, text=True)

            if result.returncode == 0:
                # 解析版本信息，第一行通常包含版本号
                # 例如: ffmpeg version 4.4.1
                first_line = result.stdout.split('\n')[0]
                return first_line
            return None

        except Exception as e:
            print(f"检查 FFmpeg 版本失败: {e}")
            return None

    def download(self, progress_callback=None) -> Tuple[bool, str]:
        """
        下载并安装 FFmpeg

        Args:
            progress_callback: 进度回调函数，接收 (current, total, status) 参数

        Returns:
            (成功标志, 消息) 元组
        """
        if self.is_installed():
            return True, "FFmpeg 已安装"

        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        try:
            if progress_callback:
                progress_callback(0, 100, "开始下载...")

            # 下载文件
            downloaded_file = self.cache_dir / 'download_temp'

            with urllib.request.urlopen(self.download_url) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                block_size = 8192

                with open(downloaded_file, 'wb') as f:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        downloaded += len(buffer)
                        f.write(buffer)

                        if progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress, 100, f"下载中... {progress}%")

            if progress_callback:
                progress_callback(90, 100, "解压中...")

            # 解压文件
            self._extract(downloaded_file)

            # 清理下载的临时文件
            if downloaded_file.exists():
                downloaded_file.unlink()

            if progress_callback:
                progress_callback(100, 100, "完成")

            # 验证安装
            if self.is_installed():
                return True, "FFmpeg 安装成功"
            else:
                return False, "FFmpeg 安装失败：无法验证安装"

        except Exception as e:
            # 清理失败的文件
            downloaded_file = self.cache_dir / 'download_temp'
            if downloaded_file.exists():
                downloaded_file.unlink()

            return False, f"下载失败: {str(e)}"

    def _extract(self, archive_path: Path):
        """
        解压下载的压缩文件

        Args:
            archive_path: 压缩文件路径
        """
        if self.platform_name == 'windows':
            self._extract_zip(archive_path)
        elif self.platform_name == 'mac':
            self._extract_zip(archive_path)
        else:
            self._extract_tar_xz(archive_path)

    def _extract_zip(self, archive_path: Path):
        """
        解压 ZIP 文件（Windows 和 Mac）

        Args:
            archive_path: ZIP 文件路径
        """
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            # 获取所有文件
            file_list = zip_ref.namelist()

            # 查找 ffmpeg 可执行文件
            for file_info in file_list:
                # Windows 下查找 ffmpeg.exe，Mac 下查找 ffmpeg
                if file_info.endswith(self.binary_name) or file_info.endswith(self.binary_name + '.exe'):
                    # 解压到缓存目录
                    zip_ref.extract(file_info, self.cache_dir)

                    # 移动到目标位置（去掉可能的 bin 前缀目录）
                    source = self.cache_dir / file_info
                    target = self._get_binary_path()

                    # 如果已存在，先删除
                    if target.exists():
                        target.unlink()

                    # 移动文件
                    shutil.move(str(source), str(target))

                    # 删除解压产生的空目录
                    extracted_dir = source.parent
                    if extracted_dir.exists():
                        try:
                            extracted_dir.rmdir()
                        except OSError:
                            pass
                    return

            # 如果没找到带目录的 ffmpeg，尝试直接解压同名文件
            for file_info in file_list:
                if file_info.endswith(self.binary_name + '/'):
                    # 这是一个目录，继续处理
                    pass

    def _extract_tar_xz(self, archive_path: Path):
        """
        解压 TAR.XZ 文件（Linux）

        Args:
            archive_path: TAR.XZ 文件路径
        """
        with tarfile.open(archive_path, 'r:xz') as tar_ref:
            # 获取所有成员
            members = tar_ref.getmembers()

            for member in members:
                # 查找 ffmpeg 可执行文件
                if member.name.endswith(f'/bin/{self.binary_name}') or member.name == self.binary_name:
                    # 解压文件
                    tar_ref.extract(member, self.cache_dir)

                    # 移动到目标位置
                    source = self.cache_dir / member.name
                    target = self._get_binary_path()

                    # 如果已存在，先删除
                    if target.exists():
                        target.unlink()

                    # 移动文件
                    shutil.move(str(source), str(target))

                    # 设置执行权限
                    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    return

    def get_path(self) -> Optional[str]:
        """
        获取 FFmpeg 路径

        Returns:
            FFmpeg 完整路径字符串，如果未安装返回 None
        """
        if not self.is_installed():
            return None
        return str(self._get_binary_path())

    def execute(self, args: list, capture_output: bool = True) -> Tuple[int, str, str]:
        """
        执行 FFmpeg 命令

        Args:
            args: FFmpeg 命令参数列表
            capture_output: 是否捕获输出，默认为 True

        Returns:
            (返回码, 标准输出, 标准错误) 元组
        """
        ffmpeg_path = self.get_path()
        if not ffmpeg_path:
            raise RuntimeError("FFmpeg 未安装，请先调用 download() 方法安装")

        return subprocess_run([ffmpeg_path] + args, capture_output=capture_output, text=True)


def subprocess_run(args, capture_output: bool = False, text: bool = False):
    """
    跨平台 subprocess.run 封装

    Args:
        args: 命令参数列表
        capture_output: 是否捕获输出
        text: 是否使用文本模式

    Returns:
        subprocess.CompletedProcess 对象
    """
    import subprocess

    # 在 Windows 上，使用 creationflags 避免创建控制台窗口
    kwargs = {
        'capture_output': capture_output,
        'text': text
    }

    if sys.platform == 'win32':
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

    return subprocess.run(args, **kwargs)
