"""
批量重命名功能模块
提供多种批量重命名方式
支持模板变量：{name}, {date}, {index}, {time}
支持前缀/后缀添加和序号格式设置
"""

from typing import List, Tuple, Optional, Callable
import os
import re
from datetime import datetime
import glob


class BatchRenamer:
    """
    批量重命名类
    支持模板变量、前缀/后缀、序号格式等功能
    """
    
    # 可用的模板变量
    TEMPLATE_VARIABLES = {
        '{name}': '原始文件名（不含扩展名）',
        '{date}': '当前日期（YYYYMMDD）',
        '{time}': '当前时间（HHMMSS）',
        '{index}': '序号（可配置格式）',
        '{ext}': '文件扩展名',
        '{parent}': '父目录名',
        '{year}': '当前年份',
        '{month}': '当前月份',
        '{day}': '当前日期',
    }
    
    def __init__(self):
        """
        初始化批量重命名器
        """
        self.files: List[str] = []
        self.original_names: List[str] = []
    
    def load_files(self, file_paths: List[str]) -> 'BatchRenamer':
        """
        加载要重命名的文件列表
        
        Args:
            file_paths: 文件路径列表
        
        Returns:
            self（支持链式调用）
        """
        self.files = list(file_paths)
        self.original_names = [os.path.basename(f) for f in file_paths]
        return self
    
    def load_from_directory(
        self,
        directory: str,
        pattern: str = '*',
        recursive: bool = False
    ) -> 'BatchRenamer':
        """
        从目录加载文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式，默认 '*'
            recursive: 是否递归搜索子目录，默认 False
        
        Returns:
            self（支持链式调用）
        """
        if recursive:
            search_pattern = os.path.join(directory, '**', pattern)
            self.files = sorted(glob.glob(search_pattern, recursive=True))
        else:
            search_pattern = os.path.join(directory, pattern)
            self.files = sorted(glob.glob(search_pattern))
        
        # 过滤掉目录
        self.files = [f for f in self.files if os.path.isfile(f)]
        self.original_names = [os.path.basename(f) for f in self.files]
        
        return self
    
    def rename_by_template(
        self,
        template: str,
        start_index: int = 1,
        index_padding: int = 3,
        dry_run: bool = False
    ) -> List[Tuple[str, str]]:
        """
        根据模板批量重命名
        
        Args:
            template: 重命名模板
                     可用变量: {name}, {date}, {time}, {index}, {ext}, {parent}, {year}, {month}, {day}
            start_index: 起始序号，默认 1
            index_padding: 序号位数（填充），默认 3（如 001, 002）
            dry_run: 预览模式，不实际重命名，默认 False
        
        Returns:
            重命名结果列表 [(原路径, 新路径), ...]
        
        Raises:
            ValueError: 模板无效时抛出
        """
        if not self.files:
            raise ValueError("没有加载文件，请先调用 load_files 或 load_from_directory")
        
        results = []
        now = datetime.now()
        
        # 验证模板
        for var in self.TEMPLATE_VARIABLES.keys():
            if var not in template and '{' in template:
                # 检查是否有未识别的变量
                pass
        
        for i, file_path in enumerate(self.files):
            original_name = os.path.basename(file_path)
            name_without_ext, ext = os.path.splitext(original_name)
            parent_dir = os.path.basename(os.path.dirname(file_path))
            
            # 生成新文件名
            new_name = template
            new_name = new_name.replace('{name}', name_without_ext)
            new_name = new_name.replace('{date}', now.strftime('%Y%m%d'))
            new_name = new_name.replace('{time}', now.strftime('%H%M%S'))
            new_name = new_name.replace('{index}', str(i + start_index).zfill(index_padding))
            new_name = new_name.replace('{ext}', ext.lstrip('.'))
            new_name = new_name.replace('{parent}', parent_dir)
            new_name = new_name.replace('{year}', now.strftime('%Y'))
            new_name = new_name.replace('{month}', now.strftime('%m'))
            new_name = new_name.replace('{day}', now.strftime('%d'))
            
            # 确保新文件名有扩展名
            if '.' not in new_name and ext:
                new_name = new_name + ext
            
            # 生成完整路径
            directory = os.path.dirname(file_path)
            new_path = os.path.join(directory, new_name)
            
            # 如果是预览模式或文件名没有变化，直接添加结果
            if dry_run or original_name == new_name:
                results.append((file_path, new_path))
            else:
                try:
                    # 执行重命名
                    os.rename(file_path, new_path)
                    results.append((file_path, new_path))
                    # 更新文件列表中的路径
                    self.files[i] = new_path
                except OSError as e:
                    print(f"重命名失败 {original_name}: {e}")
                    results.append((file_path, file_path))
        
        return results
    
    def add_prefix(self, prefix: str, dry_run: bool = False) -> List[Tuple[str, str]]:
        """
        添加前缀
        
        Args:
            prefix: 前缀字符串
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        return self.rename_by_template(prefix + '{name}{ext}', dry_run=dry_run)
    
    def add_suffix(self, suffix: str, dry_run: bool = False) -> List[Tuple[str, str]]:
        """
        添加后缀
        
        Args:
            suffix: 后缀字符串
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        return self.rename_by_template('{name}' + suffix + '{ext}', dry_run=dry_run)
    
    def replace_text(
        self,
        old: str,
        new: str,
        case_sensitive: bool = True,
        dry_run: bool = False
    ) -> List[Tuple[str, str]]:
        """
        替换文件名中的文本
        
        Args:
            old: 要替换的文本
            new: 替换后的文本
            case_sensitive: 是否区分大小写，默认 True
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        template = '{name}'
        
        if not case_sensitive:
            # 使用正则表达式进行不区分大小写的替换
            def replace_func(match):
                return new
            template = f'{{re:{re.escape(old)}}}'
        
        return self.rename_by_custom(
            lambda name, ext, **kwargs: self._replace_in_name(
                name, old, new, case_sensitive
            ) + '.' + ext,
            dry_run=dry_run
        )
    
    def _replace_in_name(
        self,
        name: str,
        old: str,
        new: str,
        case_sensitive: bool
    ) -> str:
        """
        在文件名中执行文本替换
        
        Args:
            name: 原文件名
            old: 要替换的文本
            new: 替换后的文本
            case_sensitive: 是否区分大小写
        
        Returns:
            替换后的文件名
        """
        if case_sensitive:
            return name.replace(old, new)
        else:
            # 不区分大小写的替换
            pattern = re.compile(re.escape(old), re.IGNORECASE)
            return pattern.sub(new, name)
    
    def rename_by_regex(
        self,
        pattern: str,
        replacement: str,
        dry_run: bool = False
    ) -> List[Tuple[str, str]]:
        """
        使用正则表达式重命名
        
        Args:
            pattern: 正则表达式模式
            replacement: 替换字符串（支持分组引用如 \\1, \\2）
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        return self.rename_by_custom(
            lambda name, ext, **kwargs: 
                re.sub(pattern, replacement, name) + '.' + ext,
            dry_run=dry_run
        )
    
    def rename_by_custom(
        self,
        rename_func: Callable[[str, str, dict], str],
        dry_run: bool = False
    ) -> List[Tuple[str, str]]:
        """
        使用自定义函数重命名
        
        Args:
            rename_func: 自定义重命名函数，接收 (name, ext, info) 返回新文件名
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        if not self.files:
            raise ValueError("没有加载文件")
        
        results = []
        
        for i, file_path in enumerate(self.files):
            original_name = os.path.basename(file_path)
            name_without_ext, ext = os.path.splitext(original_name)
            ext = ext.lstrip('.')
            
            # 准备额外信息
            info = {
                'index': i + 1,
                'original_name': original_name,
                'directory': os.path.dirname(file_path),
            }
            
            # 调用自定义函数
            try:
                new_name = rename_func(name_without_ext, ext, info)
                # 确保扩展名正确
                if not new_name.endswith('.' + ext):
                    new_name = new_name + '.' + ext
            except Exception as e:
                print(f"自定义函数执行失败: {e}")
                new_name = original_name
            
            # 生成完整路径
            directory = os.path.dirname(file_path)
            new_path = os.path.join(directory, new_name)
            
            # 如果是预览模式或文件名没有变化
            if dry_run or original_name == new_name:
                results.append((file_path, new_path))
            else:
                try:
                    os.rename(file_path, new_path)
                    results.append((file_path, new_path))
                    self.files[i] = new_path
                except OSError as e:
                    print(f"重命名失败 {original_name}: {e}")
                    results.append((file_path, file_path))
        
        return results
    
    def sequential_numbering(
        self,
        prefix: str = '',
        suffix: str = '',
        start: int = 1,
        padding: int = 3,
        dry_run: bool = False
    ) -> List[Tuple[str, str]]:
        """
        顺序编号重命名
        
        Args:
            prefix: 文件名前缀
            suffix: 文件名后缀
            start: 起始编号，默认 1
            padding: 序号位数，默认 3（如 001）
            dry_run: 预览模式，默认 False
        
        Returns:
            重命名结果列表
        """
        template = f"{prefix}{{'index'}}{suffix}{{'ext'}}"
        return self.rename_by_template(
            template, 
            start_index=start, 
            index_padding=padding, 
            dry_run=dry_run
        )
    
    def get_preview(
        self,
        template: str,
        start_index: int = 1,
        index_padding: int = 3
    ) -> List[Tuple[str, str]]:
        """
        预览重命名结果（不实际执行）
        
        Args:
            template: 重命名模板
            start_index: 起始序号
            index_padding: 序号位数
        
        Returns:
            预览结果列表 [(原名, 新名), ...]
        """
        return self.rename_by_template(
            template, 
            start_index=start_index, 
            index_padding=index_padding, 
            dry_run=True
        )
    
    def get_file_count(self) -> int:
        """
        获取已加载的文件数量
        
        Returns:
            文件数量
        """
        return len(self.files)
    
    def clear(self) -> 'BatchRenamer':
        """
        清空文件列表
        
        Returns:
            self（支持链式调用）
        """
        self.files = []
        self.original_names = []
        return self


def batch_rename(
    file_paths: List[str],
    template: str,
    start_index: int = 1,
    index_padding: int = 3
) -> List[Tuple[str, str]]:
    """
    便捷函数：批量重命名
    
    Args:
        file_paths: 文件路径列表
        template: 重命名模板
        start_index: 起始序号
        index_padding: 序号位数
    
    Returns:
        重命名结果列表
    """
    renamer = BatchRenamer()
    renamer.load_files(file_paths)
    return renamer.rename_by_template(template, start_index, index_padding)


def add_prefix_to_files(
    file_paths: List[str],
    prefix: str
) -> List[Tuple[str, str]]:
    """
    便捷函数：为文件列表添加前缀
    
    Args:
        file_paths: 文件路径列表
        prefix: 前缀字符串
    
    Returns:
        重命名结果列表
    """
    renamer = BatchRenamer()
    renamer.load_files(file_paths)
    return renamer.add_prefix(prefix)


def add_suffix_to_files(
    file_paths: List[str],
    suffix: str
) -> List[Tuple[str, str]]:
    """
    便捷函数：为文件列表添加后缀
    
    Args:
        file_paths: 文件路径列表
        suffix: 后缀字符串
    
    Returns:
        重命名结果列表
    """
    renamer = BatchRenamer()
    renamer.load_files(file_paths)
    return renamer.add_suffix(suffix)


def sequential_rename(
    file_paths: List[str],
    prefix: str = '',
    suffix: str = '',
    start: int = 1,
    padding: int = 3
) -> List[Tuple[str, str]]:
    """
    便捷函数：顺序编号重命名
    
    Args:
        file_paths: 文件路径列表
        prefix: 文件名前缀
        suffix: 文件名后缀
        start: 起始编号
        padding: 序号位数
    
    Returns:
        重命名结果列表
    """
    renamer = BatchRenamer()
    renamer.load_files(file_paths)
    return renamer.sequential_numbering(prefix, suffix, start, padding)


def rename_with_date(
    file_paths: List[str],
    prefix: str = '',
    suffix: str = '',
    date_format: str = '%Y%m%d'
) -> List[Tuple[str, str]]:
    """
    便捷函数：添加日期前缀/后缀
    
    Args:
        file_paths: 文件路径列表
        prefix: 文件名前缀
        suffix: 文件名后缀
        date_format: 日期格式，默认 '%Y%m%d'
    
    Returns:
        重命名结果列表
    """
    renamer = BatchRenamer()
    renamer.load_files(file_paths)
    
    date_str = datetime.now().strftime(date_format)
    prefix_str = f"{date_str}_{prefix}" if prefix else date_str
    suffix_str = f"_{date_str}" if suffix else ''
    
    template = f"{prefix_str}{{'name'}}{suffix_str}{{'ext'}}"
    return renamer.rename_by_template(template)
