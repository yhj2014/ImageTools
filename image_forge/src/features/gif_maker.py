"""
GIF 制作功能模块
提供多图合成 GIF 的功能
支持帧延迟设置、循环次数控制、尺寸调整
使用 Pillow 库实现
"""

from PIL import Image
from typing import List, Tuple, Optional, Union
import os


class GIFMaker:
    """
    GIF 动画制作类
    支持多图合成 GIF，提供帧延迟、循环次数、尺寸调整等功能
    """
    
    def __init__(self):
        """
        初始化 GIF 制作器
        """
        self.frames: List[Image.Image] = []
        self.frame_delays: List[int] = []
    
    def load_images(
        self,
        image_paths: List[str],
        resize: Optional[Tuple[int, int]] = None
    ) -> 'GIFMaker':
        """
        加载多张图像
        
        Args:
            image_paths: 图像文件路径列表
            resize: 可选的目标尺寸 (width, height)
        
        Returns:
            self（支持链式调用）
        """
        self.frames = []
        self.frame_delays = []
        
        for path in image_paths:
            img = Image.open(path)
            # 确保图像为 RGBA 模式（支持透明度）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 如果指定了尺寸，则调整大小
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)
            
            self.frames.append(img)
        
        return self
    
    def add_frame(
        self,
        image: Image.Image,
        delay: int = 100
    ) -> 'GIFMaker':
        """
        添加单个帧
        
        Args:
            image: 图像对象
            delay: 帧延迟时间（毫秒），默认 100ms
        
        Returns:
            self（支持链式调用）
        """
        # 确保图像为 RGBA 模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        self.frames.append(image)
        self.frame_delays.append(delay)
        
        return self
    
    def set_frame_delays(self, delays: List[int]) -> 'GIFMaker':
        """
        设置所有帧的延迟时间
        
        Args:
            delays: 延迟时间列表（毫秒），长度必须与帧数量匹配
        
        Returns:
            self（支持链式调用）
        
        Raises:
            ValueError: 延迟列表长度不匹配时抛出
        """
        if len(delays) != len(self.frames):
            raise ValueError(
                f"延迟列表长度 ({len(delays)}) 与帧数量 ({len(self.frames)}) 不匹配"
            )
        
        self.frame_delays = delays
        return self
    
    def set_uniform_delay(self, delay: int) -> 'GIFMaker':
        """
        设置统一的帧延迟
        
        Args:
            delay: 延迟时间（毫秒）
        
        Returns:
            self（支持链式调用）
        """
        self.frame_delays = [delay] * len(self.frames)
        return self
    
    def resize_frames(
        self,
        size: Tuple[int, int],
        algorithm: str = 'lanczos'
    ) -> 'GIFMaker':
        """
        调整所有帧的尺寸
        
        Args:
            size: 目标尺寸 (width, height)
            algorithm: 缩放算法 ('nearest', 'bilinear', 'bicubic', 'lanczos')
        
        Returns:
            self（支持链式调用）
        """
        algorithms = {
            'nearest': Image.Resampling.NEAREST,
            'bilinear': Image.Resampling.BILINEAR,
            'bicubic': Image.Resampling.BICUBIC,
            'lanczos': Image.Resampling.LANCZOS,
        }
        
        resample = algorithms.get(algorithm, Image.Resampling.LANCZOS)
        
        for i, frame in enumerate(self.frames):
            self.frames[i] = frame.resize(size, resample)
        
        return self
    
    def optimize(self) -> 'GIFMaker':
        """
        优化 GIF，移除重复帧以减小文件大小
        
        Returns:
            self（支持链式调用）
        """
        if not self.frames:
            return self
        
        optimized_frames = [self.frames[0]]
        optimized_delays = [self.frame_delays[0]] if self.frame_delays else [100]
        
        for i in range(1, len(self.frames)):
            # 检查是否与前一帧相同
            diff = list(self.frames[i].getdata())
            diff_prev = list(self.frames[i-1].getdata())
            
            if diff != diff_prev:
                optimized_frames.append(self.frames[i])
                if i < len(self.frame_delays):
                    optimized_delays.append(self.frame_delays[i])
        
        self.frames = optimized_frames
        self.frame_delays = optimized_delays
        
        return self
    
    def create_gif(
        self,
        output_path: str,
        loop: int = 0,
        optimize: bool = True
    ) -> str:
        """
        创建 GIF 动画
        
        Args:
            output_path: 输出 GIF 文件路径
            loop: 循环次数 (0=无限循环, 1=播放一次, n=播放n次)
            optimize: 是否优化 GIF，默认 True
        
        Returns:
            输出文件路径
        
        Raises:
            ValueError: 没有帧时抛出
        """
        if not self.frames:
            raise ValueError("没有可用的帧，请先添加图像")
        
        # 确保延迟列表有值
        if not self.frame_delays:
            self.frame_delays = [100] * len(self.frames)
        
        # 如果延迟列表长度不匹配，使用第一个延迟值
        if len(self.frame_delays) != len(self.frames):
            default_delay = self.frame_delays[0] if self.frame_delays else 100
            self.frame_delays = [default_delay] * len(self.frames)
        
        # 转换帧为调色板模式（GIF 格式要求）
        converted_frames = []
        for frame in self.frames:
            # 转换为 P 模式（调色板模式）
            if frame.mode == 'RGBA':
                # 保留透明度
                frame_p = frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
            else:
                frame_p = frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
            converted_frames.append(frame_p)
        
        # 保存 GIF
        converted_frames[0].save(
            output_path,
            save_all=True,
            append_images=converted_frames[1:],
            duration=self.frame_delays,
            loop=loop,
            optimize=optimize
        )
        
        return output_path
    
    def preview_frame(self, index: int) -> Image.Image:
        """
        预览指定帧
        
        Args:
            index: 帧索引
        
        Returns:
            帧图像对象
        """
        if index < 0 or index >= len(self.frames):
            raise IndexError(f"帧索引超出范围: {index}")
        
        return self.frames[index]
    
    def get_frame_count(self) -> int:
        """
        获取帧数量
        
        Returns:
            帧数量
        """
        return len(self.frames)
    
    def get_info(self) -> dict:
        """
        获取 GIF 信息
        
        Returns:
            包含 GIF 信息的字典
        """
        if not self.frames:
            return {
                'frame_count': 0,
                'size': None,
                'duration': 0,
                'mode': None
            }
        
        size = self.frames[0].size
        total_duration = sum(self.frame_delays) if self.frame_delays else 0
        
        return {
            'frame_count': len(self.frames),
            'size': size,
            'duration': total_duration,
            'mode': self.frames[0].mode,
            'delays': self.frame_delays
        }
    
    def clear(self) -> 'GIFMaker':
        """
        清空所有帧
        
        Returns:
            self（支持链式调用）
        """
        self.frames = []
        self.frame_delays = []
        return self
    
    def close(self):
        """关闭所有图像，释放资源"""
        for frame in self.frames:
            try:
                frame.close()
            except Exception:
                pass
        self.frames = []
        self.frame_delays = []


def create_gif(
    image_paths: List[str],
    output_path: str,
    delay: int = 100,
    loop: int = 0,
    resize: Optional[Tuple[int, int]] = None
) -> str:
    """
    便捷函数：创建 GIF 动画
    
    Args:
        image_paths: 图像文件路径列表
        output_path: 输出 GIF 文件路径
        delay: 帧延迟时间（毫秒），默认 100ms
        loop: 循环次数 (0=无限循环, 1=播放一次, n=播放n次)
        resize: 可选的目标尺寸 (width, height)
    
    Returns:
        输出文件路径
    """
    maker = GIFMaker()
    
    try:
        maker.load_images(image_paths, resize)
        maker.set_uniform_delay(delay)
        return maker.create_gif(output_path, loop)
    finally:
        maker.close()


def images_to_gif(
    image_dir: str,
    output_path: str,
    pattern: str = '*.png',
    delay: int = 100,
    loop: int = 0,
    resize: Optional[Tuple[int, int]] = None
) -> str:
    """
    便捷函数：从目录中的图像创建 GIF
    
    Args:
        image_dir: 图像目录路径
        output_path: 输出 GIF 文件路径
        pattern: 文件匹配模式，默认 '*.png'
        delay: 帧延迟时间（毫秒），默认 100ms
        loop: 循环次数
        resize: 可选的目标尺寸
    
    Returns:
        输出文件路径
    """
    import glob
    
    # 获取目录中所有匹配的图像文件
    pattern_path = os.path.join(image_dir, pattern)
    image_paths = sorted(glob.glob(pattern_path))
    
    if not image_paths:
        raise ValueError(f"在目录 {image_dir} 中找不到匹配的图像文件")
    
    return create_gif(image_paths, output_path, delay, loop, resize)


def create_animated_gif(
    image_paths: List[str],
    output_path: str,
    frame_delays: List[int],
    loop: int = 0,
    resize: Optional[Tuple[int, int]] = None
) -> str:
    """
    便捷函数：创建带自定义帧延迟的 GIF
    
    Args:
        image_paths: 图像文件路径列表
        output_path: 输出 GIF 文件路径
        frame_delays: 每帧的延迟时间列表（毫秒）
        loop: 循环次数
        resize: 可选的目标尺寸
    
    Returns:
        输出文件路径
    """
    maker = GIFMaker()
    
    try:
        maker.load_images(image_paths, resize)
        maker.set_frame_delays(frame_delays)
        return maker.create_gif(output_path, loop)
    finally:
        maker.close()


def extract_frames(
    gif_path: str,
    output_dir: str,
    prefix: str = 'frame_',
    format: str = 'png'
) -> List[str]:
    """
    从 GIF 中提取所有帧
    
    Args:
        gif_path: GIF 文件路径
        output_dir: 输出目录
        prefix: 输出文件名前缀
        format: 输出图像格式 ('png', 'jpg', 'bmp')
    
    Returns:
        提取的帧文件路径列表
    """
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    gif = Image.open(gif_path)
    
    frames = []
    frame_num = 0
    
    try:
        while True:
            # 获取当前帧
            current_frame = gif.copy()
            
            # 保存帧
            output_path = os.path.join(
                output_dir, 
                f"{prefix}{frame_num:04d}.{format}"
            )
            current_frame.save(output_path)
            frames.append(output_path)
            
            frame_num += 1
            
            # 移动到下一帧
            gif.seek(gif.tell() + 1)
            
    except EOFError:
        # 已经到达 GIF 末尾
        pass
    
    gif.close()
    
    return frames


def get_gif_info(gif_path: str) -> dict:
    """
    获取 GIF 文件信息
    
    Args:
        gif_path: GIF 文件路径
    
    Returns:
        包含 GIF 信息的字典
    """
    gif = Image.open(gif_path)
    
    info = {
        'size': gif.size,
        'mode': gif.mode,
        'n_frames': 0,
        'duration': 0,
        'loop': 0
    }
    
    try:
        # 获取帧数
        while True:
            info['n_frames'] += 1
            info['duration'] += gif.info.get('duration', 100)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    
    # 获取循环信息
    info['loop'] = gif.info.get('loop', 0)
    
    gif.close()
    
    return info
