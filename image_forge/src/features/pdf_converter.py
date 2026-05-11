"""
PDF 转换功能模块
提供图像转 PDF 的功能
支持单张单页、多张单页、网格布局（如 2x2, 3x3）等模式
使用 Pillow 库和 PyPDF2/pypdf 实现
"""

from PIL import Image
from typing import List, Tuple, Optional, Union, Literal
import os


class PDFConverter:
    """
    PDF 转换类
    支持图像转 PDF，提供多种布局模式
    """
    
    # PDF 标准尺寸（单位：英寸，72 DPI）
    PAGE_SIZES = {
        'A4': (595.27, 841.89),      # 210 x 297 mm
        'A3': (841.89, 1190.55),    # 297 x 420 mm
        'Letter': (612, 792),        # 8.5 x 11 英寸
        'Legal': (612, 1008),        # 8.5 x 14 英寸
        '4x6': (288, 432),           # 4 x 6 英寸
        'Custom': None,              # 自定义尺寸
    }
    
    def __init__(self):
        """
        初始化 PDF 转换器
        """
        self.images: List[Image.Image] = []
        self.image_paths: List[str] = []
    
    def load_images(self, image_paths: List[str]) -> 'PDFConverter':
        """
        加载要转换的图像
        
        Args:
            image_paths: 图像文件路径列表
        
        Returns:
            self（支持链式调用）
        """
        self.images = []
        self.image_paths = list(image_paths)
        
        for path in image_paths:
            img = Image.open(path)
            self.images.append(img)
        
        return self
    
    def images_to_pdf(
        self,
        output_path: str,
        page_size: Tuple[float, float] = None,
        margin: float = 0,
        mode: Literal['fit', 'fill', 'stretch'] = 'fit',
        quality: int = 95
    ) -> str:
        """
        将多张图像转换为一个 PDF 文件（每张图像一页）
        
        Args:
            output_path: 输出 PDF 文件路径
            page_size: 页面尺寸 (width, height)，单位像素，默认 A4
            margin: 页边距，单位像素，默认 0
            mode: 图像适应模式 ('fit' 自适应填充, 'fill' 填充裁剪, 'stretch' 拉伸)
            quality: JPEG 压缩质量 (1-100)
        
        Returns:
            输出文件路径
        """
        if not self.images:
            raise ValueError("没有加载图像，请先调用 load_images")
        
        # 默认使用 A4 尺寸
        if page_size is None:
            page_size = self.PAGE_SIZES['A4']
        
        # 导入 pdf 相关库（尝试多种实现）
        pdf_writer = self._get_pdf_writer()
        
        for i, img in enumerate(self.images):
            # 调整图像以适应页面
            adjusted_img = self._fit_image_to_page(
                img, page_size, margin, mode
            )
            
            # 创建单页 PDF
            pdf_page = self._create_pdf_page(adjusted_img, page_size, quality)
            pdf_writer.add_page(pdf_page)
        
        # 保存 PDF
        self._save_pdf(pdf_writer, output_path)
        
        return output_path
    
    def images_to_grid_pdf(
        self,
        output_path: str,
        grid: Tuple[int, int] = (2, 2),
        page_size: Tuple[float, float] = None,
        margin: float = 10,
        spacing: float = 5,
        quality: int = 95
    ) -> str:
        """
        将多张图像转换为网格布局 PDF
        
        Args:
            output_path: 输出 PDF 文件路径
            grid: 网格布局 (行数, 列数)，如 (2, 2) 表示 2x2 网格
            page_size: 页面尺寸，默认 A4
            margin: 页边距，单位像素
            spacing: 网格间距，单位像素
            quality: JPEG 压缩质量
        
        Returns:
            输出文件路径
        """
        if not self.images:
            raise ValueError("没有加载图像，请先调用 load_images")
        
        if page_size is None:
            page_size = self.PAGE_SIZES['A4']
        
        rows, cols = grid
        pdf_writer = self._get_pdf_writer()
        
        # 计算每个网格单元的尺寸
        available_width = page_size[0] - 2 * margin
        available_height = page_size[1] - 2 * margin
        
        cell_width = (available_width - spacing * (cols - 1)) / cols
        cell_height = (available_height - spacing * (rows - 1)) / rows
        
        # 计算每页可容纳的图像数
        images_per_page = rows * cols
        
        # 分页处理
        for page_start in range(0, len(self.images), images_per_page):
            page_images = self.images[page_start:page_start + images_per_page]
            
            # 创建页面图像
            page_img = self._create_grid_image(
                page_images,
                rows, cols,
                cell_width, cell_height,
                spacing
            )
            
            # 创建 PDF 页面
            pdf_page = self._create_pdf_page(page_img, page_size, quality)
            pdf_writer.add_page(pdf_page)
            
            # 关闭临时图像
            page_img.close()
        
        # 保存 PDF
        self._save_pdf(pdf_writer, output_path)
        
        return output_path
    
    def single_image_to_pdf(
        self,
        output_path: str,
        page_size: Tuple[float, float] = None,
        margin: float = 0,
        mode: Literal['fit', 'fill', 'stretch'] = 'fit',
        quality: int = 95
    ) -> str:
        """
        将单张图像转换为 PDF
        
        Args:
            output_path: 输出 PDF 文件路径
            page_size: 页面尺寸，默认 A4
            margin: 页边距，单位像素
            mode: 图像适应模式
            quality: JPEG 压缩质量
        
        Returns:
            输出文件路径
        """
        if not self.images:
            raise ValueError("没有加载图像，请先调用 load_images")
        
        if len(self.images) > 1:
            raise ValueError("单图转换模式只能处理一张图像，请只加载一张图片")
        
        if page_size is None:
            page_size = self.PAGE_SIZES['A4']
        
        img = self.images[0]
        adjusted_img = self._fit_image_to_page(img, page_size, margin, mode)
        
        pdf_writer = self._get_pdf_writer()
        pdf_page = self._create_pdf_page(adjusted_img, page_size, quality)
        pdf_writer.add_page(pdf_page)
        
        self._save_pdf(pdf_writer, output_path)
        adjusted_img.close()
        
        return output_path
    
    def _get_pdf_writer(self):
        """
        获取 PDF 写入器（支持多种库）
        
        Returns:
            PDF 写入器对象
        """
        try:
            # 尝试使用 pypdf（新版）
            from pypdf import PdfWriter
            return PdfWriter()
        except ImportError:
            pass
        
        try:
            # 尝试使用 PyPDF2（旧版）
            from PyPDF2 import PdfWriter
            return PdfWriter()
        except ImportError:
            pass
        
        raise ImportError(
            "请安装 pypdf 或 PyPDF2 库: pip install pypdf 或 pip install PyPDF2"
        )
    
    def _fit_image_to_page(
        self,
        img: Image.Image,
        page_size: Tuple[float, float],
        margin: float,
        mode: str
    ) -> Image.Image:
        """
        调整图像以适应页面
        
        Args:
            img: 原始图像
            page_size: 页面尺寸
            margin: 页边距
            mode: 适应模式
        
        Returns:
            调整后的图像
        """
        # 计算可用区域
        available_width = page_size[0] - 2 * margin
        available_height = page_size[1] - 2 * margin
        
        img_width, img_height = img.size
        
        if mode == 'stretch':
            # 拉伸模式：直接缩放到页面尺寸
            return img.resize(
                (int(available_width), int(available_height)),
                Image.Resampling.LANCZOS
            )
        
        elif mode == 'fill':
            # 填充模式：缩放到覆盖整个页面（可能溢出裁剪）
            ratio_w = available_width / img_width
            ratio_h = available_height / img_height
            ratio = max(ratio_w, ratio_h)
            
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 居中裁剪
            left = (new_width - available_width) // 2
            top = (new_height - available_height) // 2
            
            return resized.crop((
                left, top,
                left + available_width,
                top + available_height
            ))
        
        else:  # 'fit'
            # 自适应模式：完整显示在页面内
            ratio_w = available_width / img_width
            ratio_h = available_height / img_height
            ratio = min(ratio_w, ratio_h)
            
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _create_grid_image(
        self,
        images: List[Image.Image],
        rows: int,
        cols: int,
        cell_width: float,
        cell_height: float,
        spacing: float
    ) -> Image.Image:
        """
        创建网格布局图像
        
        Args:
            images: 图像列表
            rows: 行数
            cols: 列数
            cell_width: 单元格宽度
            cell_height: 单元格高度
            spacing: 间距
        
        Returns:
            网格图像
        """
        # 创建白色背景画布
        total_width = int(cols * cell_width + (cols - 1) * spacing)
        total_height = int(rows * cell_height + (rows - 1) * spacing)
        
        grid_img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
        
        for idx, img in enumerate(images):
            if idx >= rows * cols:
                break
            
            row = idx // cols
            col = idx % cols
            
            # 计算位置
            x = int(col * (cell_width + spacing))
            y = int(row * (cell_height + spacing))
            
            # 调整图像大小以适应单元格
            cell_img = img.copy()
            cell_img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)
            
            # 居中粘贴（添加白边）
            offset_x = int((cell_width - cell_img.width) / 2)
            offset_y = int((cell_height - cell_img.height) / 2)
            
            # 确保图像为 RGB 模式
            if cell_img.mode != 'RGB':
                cell_img = cell_img.convert('RGB')
            
            grid_img.paste(cell_img, (x + offset_x, y + offset_y))
            cell_img.close()
        
        return grid_img
    
    def _create_pdf_page(
        self,
        img: Image.Image,
        page_size: Tuple[float, float],
        quality: int
    ):
        """
        从图像创建 PDF 页面
        
        Args:
            img: 图像对象
            page_size: 页面尺寸
        
        Returns:
            PDF 页面对象
        """
        # 确保图像为 RGB 模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 创建临时文件保存图像
        import io
        
        # 保存为 JPEG 格式到内存
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=quality)
        img_bytes.seek(0)
        
        # 导入 PDF 相关库
        try:
            from pypdf import PdfReader
            from pypdf import PdfWriter
        except ImportError:
            from PyPDF2 import PdfReader
            from PyPDF2 import PdfWriter
        
        # 创建临时 PDF
        temp_pdf = io.BytesIO()
        img.save(temp_pdf, format='PDF')
        temp_pdf.seek(0)
        
        # 读取临时 PDF
        reader = PdfReader(temp_pdf)
        writer = PdfWriter()
        
        # 获取页面并设置尺寸
        page = reader.pages[0]
        page.mediabox.width = page_size[0]
        page.mediabox.height = page_size[1]
        writer.add_page(page)
        
        return writer
    
    def _save_pdf(self, pdf_writer, output_path: str):
        """
        保存 PDF 文件
        
        Args:
            pdf_writer: PDF 写入器
            output_path: 输出路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        # 保存 PDF
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    
    def clear(self) -> 'PDFConverter':
        """
        清空已加载的图像
        
        Returns:
            self（支持链式调用）
        """
        for img in self.images:
            try:
                img.close()
            except Exception:
                pass
        self.images = []
        self.image_paths = []
        return self
    
    def close(self):
        """关闭所有图像，释放资源"""
        self.clear()


def images_to_pdf(
    image_paths: List[str],
    output_path: str,
    page_size: Tuple[float, float] = None,
    mode: Literal['fit', 'fill', 'stretch'] = 'fit'
) -> str:
    """
    便捷函数：将多张图像转换为 PDF（每张一页）
    
    Args:
        image_paths: 图像文件路径列表
        output_path: 输出 PDF 文件路径
        page_size: 页面尺寸，默认 A4
        mode: 图像适应模式
    
    Returns:
        输出文件路径
    """
    converter = PDFConverter()
    try:
        converter.load_images(image_paths)
        return converter.images_to_pdf(output_path, page_size, mode=mode)
    finally:
        converter.close()


def single_image_to_pdf(
    image_path: str,
    output_path: str,
    page_size: Tuple[float, float] = None,
    mode: Literal['fit', 'fill', 'stretch'] = 'fit'
) -> str:
    """
    便捷函数：将单张图像转换为 PDF
    
    Args:
        image_path: 图像文件路径
        output_path: 输出 PDF 文件路径
        page_size: 页面尺寸，默认 A4
        mode: 图像适应模式
    
    Returns:
        输出文件路径
    """
    converter = PDFConverter()
    try:
        converter.load_images([image_path])
        return converter.single_image_to_pdf(output_path, page_size, mode=mode)
    finally:
        converter.close()


def images_to_grid_pdf(
    image_paths: List[str],
    output_path: str,
    grid: Tuple[int, int] = (2, 2),
    page_size: Tuple[float, float] = None
) -> str:
    """
    便捷函数：将多张图像转换为网格布局 PDF
    
    Args:
        image_paths: 图像文件路径列表
        output_path: 输出 PDF 文件路径
        grid: 网格布局 (行数, 列数)
        page_size: 页面尺寸，默认 A4
    
    Returns:
        输出文件路径
    """
    converter = PDFConverter()
    try:
        converter.load_images(image_paths)
        return converter.images_to_grid_pdf(output_path, grid, page_size)
    finally:
        converter.close()


def directory_to_pdf(
    image_dir: str,
    output_path: str,
    pattern: str = '*',
    recursive: bool = False,
    page_size: Tuple[float, float] = None,
    mode: Literal['fit', 'fill', 'stretch'] = 'fit'
) -> str:
    """
    便捷函数：将目录中的图像转换为 PDF
    
    Args:
        image_dir: 图像目录路径
        output_path: 输出 PDF 文件路径
        pattern: 文件匹配模式，默认 '*'
        recursive: 是否递归搜索子目录，默认 False
        page_size: 页面尺寸，默认 A4
        mode: 图像适应模式
    
    Returns:
        输出文件路径
    """
    import glob
    
    # 获取匹配的图像文件
    if recursive:
        search_pattern = os.path.join(image_dir, '**', pattern)
        image_paths = sorted(glob.glob(search_pattern, recursive=True))
    else:
        search_pattern = os.path.join(image_dir, pattern)
        image_paths = sorted(glob.glob(search_pattern))
    
    # 过滤图像文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    image_paths = [
        p for p in image_paths 
        if os.path.isfile(p) and os.path.splitext(p)[1].lower() in image_extensions
    ]
    
    if not image_paths:
        raise ValueError(f"在目录 {image_dir} 中找不到匹配的图像文件")
    
    return images_to_pdf(image_paths, output_path, page_size, mode)


def get_available_page_sizes() -> dict:
    """
    获取可用的页面尺寸
    
    Returns:
        页面尺寸字典
    """
    return PDFConverter.PAGE_SIZES.copy()
