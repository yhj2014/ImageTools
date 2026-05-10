import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

from utils.logger import logger


SUPPORTED_IMAGE_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'tif',
    'gif', 'tga', 'psd', 'exr', 'hdr', 'dds', 'svg'
}

OUTPUT_FORMATS = ['png', 'jpg', 'webp', 'bmp', 'tiff', 'gif', 'tga']


class ImageConverter:
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self._ffmpeg_path = ffmpeg_path
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        try:
            result = subprocess.run(
                [self._ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                logger.info(f"FFmpeg 已就绪: {version_line}")
                return True
        except FileNotFoundError:
            logger.error("未找到 FFmpeg，请确保已安装 FFmpeg 并添加到系统 PATH")
            return False
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg 版本检查超时")
            return False
        except Exception as e:
            logger.error(f"检查 FFmpeg 时出错: {e}")
            return False
        return False

    def is_ffmpeg_available(self) -> bool:
        return shutil.which(self._ffmpeg_path) is not None

    def get_supported_formats(self) -> List[str]:
        return OUTPUT_FORMATS.copy()

    @staticmethod
    def get_input_formats() -> List[str]:
        return list(SUPPORTED_IMAGE_EXTENSIONS)

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        path = Path(file_path)
        return path.suffix.lstrip('.').lower() in SUPPORTED_IMAGE_EXTENSIONS

    def convert(
        self,
        input_path: str,
        output_path: str,
        quality: int = 85,
        overwrite: bool = True
    ) -> Tuple[bool, str]:
        input_file = Path(input_path)
        output_file = Path(output_path)

        if not input_file.exists():
            return False, f"输入文件不存在: {input_path}"

        if not self.is_image_file(input_path):
            return False, f"不支持的图片格式: {input_file.suffix}"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        output_ext = output_file.suffix.lstrip('.').lower()

        cmd = [self._ffmpeg_path, "-y" if overwrite else "-n"]

        if output_ext in ['jpg', 'jpeg']:
            cmd.extend(["-i", str(input_file)])
            cmd.extend(["-q:v", str(max(1, min(31, 100 - quality)))])
        elif output_ext == 'webp':
            cmd.extend(["-i", str(input_file)])
            cmd.extend(["-quality", str(quality)])
        elif output_ext == 'png':
            cmd.extend(["-i", str(input_file)])
            cmd.extend(["-compression_level", "6"])
        elif output_ext == 'gif':
            cmd.extend(["-i", str(input_file)])
            cmd.extend(["-loop", "0"])
        else:
            cmd.extend(["-i", str(input_file)])

        cmd.append(str(output_file))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                if output_file.exists():
                    return True, f"转换成功: {output_file.name}"
                else:
                    return False, "FFmpeg 执行成功但输出文件未生成"
            else:
                error_msg = result.stderr.strip()
                if not error_msg:
                    error_msg = f"FFmpeg 返回错误码: {result.returncode}"
                return False, error_msg

        except subprocess.TimeoutExpired:
            return False, "转换超时 (60秒)"
        except FileNotFoundError:
            return False, "FFmpeg 未找到"
        except PermissionError:
            return False, "权限不足，无法写入文件"
        except Exception as e:
            return False, f"转换出错: {str(e)}"

    def get_output_filename(self, input_path: str, output_format: str, output_dir: str) -> str:
        input_file = Path(input_path)
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        return str(output_dir_path / f"{input_file.stem}.{output_format}")
