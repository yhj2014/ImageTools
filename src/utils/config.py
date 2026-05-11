"""
配置管理模块 - 提供应用程序配置文件的读写和验证功能

功能特性:
- JSON 格式配置文件读写
- 默认配置管理
- 配置验证机制
- 自动保存/加载功能
- 使用 QStandardPaths 管理用户配置目录

使用方法:
    from utils.config import Config, get_config
    
    # 获取配置实例
    config = get_config()
    
    # 获取配置值
    theme = config.get('appearance.theme', 'dark')
    
    # 设置配置值
    config.set('appearance.theme', 'light')
    
    # 保存配置
    config.save()
    
    # 重置为默认配置
    config.reset()
"""

import json
import copy
from pathlib import Path
from typing import Any, Dict, Optional, List, Type, Union
from datetime import datetime

try:
    from PySide6.QtCore import QObject, Signal
    HAS_PYSIDE6 = True
except ImportError:
    HAS_PYSIDE6 = False


class ConfigValidator:
    """
    配置验证器基类
    
    用于定义配置项的验证规则
    """
    
    @staticmethod
    def validate_int(value: Any, min_value: Optional[int] = None, max_value: Optional[int] = None) -> bool:
        """
        验证整数类型的配置值
        
        Args:
            value: 要验证的值
            min_value: 最小值(可选)
            max_value: 最大值(可选)
            
        Returns:
            bool: 验证是否通过
        """
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
    
    @staticmethod
    def validate_float(value: Any, min_value: Optional[float] = None, max_value: Optional[float] = None) -> bool:
        """
        验证浮点数类型的配置值
        
        Args:
            value: 要验证的值
            min_value: 最小值(可选)
            max_value: 最大值(可选)
            
        Returns:
            bool: 验证是否通过
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
    
    @staticmethod
    def validate_string(value: Any, allowed_values: Optional[List[str]] = None) -> bool:
        """
        验证字符串类型的配置值
        
        Args:
            value: 要验证的值
            allowed_values: 允许的值列表(可选)
            
        Returns:
            bool: 验证是否通过
        """
        if not isinstance(value, str):
            return False
        if allowed_values is not None and value not in allowed_values:
            return False
        return True
    
    @staticmethod
    def validate_bool(value: Any) -> bool:
        """
        验证布尔类型的配置值
        
        Args:
            value: 要验证的值
            
        Returns:
            bool: 验证是否通过
        """
        return isinstance(value, bool)
    
    @staticmethod
    def validate_list(value: Any, item_type: Optional[Type] = None) -> bool:
        """
        验证列表类型的配置值
        
        Args:
            value: 要验证的值
            item_type: 列表项的类型(可选)
            
        Returns:
            bool: 验证是否通过
        """
        if not isinstance(value, list):
            return False
        if item_type is not None:
            return all(isinstance(item, item_type) for item in value)
        return True
    
    @staticmethod
    def validate_path(value: Any, must_exist: bool = False, must_be_dir: bool = False) -> bool:
        """
        验证路径类型的配置值
        
        Args:
            value: 要验证的值
            must_exist: 是否必须存在
            must_be_dir: 是否必须为目录
            
        Returns:
            bool: 验证是否通过
        """
        if not isinstance(value, (str, Path)):
            return False
        path = Path(value)
        if must_exist and not path.exists():
            return False
        if must_be_dir and path.exists() and not path.is_dir():
            return False
        return True


class Config:
    """
    配置管理系统 - 提供应用程序配置的集中管理
    
    特性:
    - 单例模式,全局共享配置
    - JSON 格式存储
    - 配置验证机制
    - 自动保存/加载
    - PySide6 Signal 信号支持
    """
    
    _instance: Optional['Config'] = None  # 单例实例
    _initialized: bool = False  # 初始化标志
    
    # 默认配置定义 - 定义了所有可用的配置项及其默认值和验证规则
    DEFAULT_CONFIG = {
        # 外观设置
        'appearance': {
            'theme': 'dark',  # 主题: 'dark' 或 'light'
            'language': 'zh_CN',  # 语言: 'zh_CN', 'en_US'
            'font_size': 12,  # 字体大小: 8-24
            'window_width': 1200,  # 窗口宽度
            'window_height': 800,  # 窗口高度
            'window_maximized': False,  # 窗口是否最大化
        },
        # 处理设置
        'processing': {
            'output_format': 'png',  # 输出格式: 'png', 'jpg', 'webp', 'bmp', 'tiff'
            'quality': 95,  # 图片质量: 1-100
            'preserve_metadata': True,  # 是否保留元数据
            'preserve_exif': True,  # 是否保留 EXIF 信息
            'backup_original': False,  # 是否备份原文件
            'output_directory': '',  # 输出目录(空字符串表示使用原文件目录)
        },
        # 性能设置
        'performance': {
            'max_workers': 4,  # 最大并发工作线程数
            'preview_size': 150,  # 预览图大小
            'cache_enabled': True,  # 是否启用缓存
            'cache_size': 500,  # 缓存大小(MB)
            'memory_limit': 2048,  # 内存限制(MB)
        },
        # 图像处理默认值
        'image': {
            'resize_width': 1920,  # 默认缩放宽度
            'resize_height': 1080,  # 默认缩放高度
            'resize_mode': 'fit',  # 缩放模式: 'fit', 'fill', 'stretch'
            'rotate_quality': 'high',  # 旋转质量: 'low', 'medium', 'high'
            'compression_level': 6,  # PNG 压缩级别: 0-9
            'watermark_opacity': 0.5,  # 水印不透明度: 0.0-1.0
        },
        # 预览设置
        'preview': {
            'show_grid': False,  # 是否显示网格
            'grid_size': 50,  # 网格大小
            'zoom_level': 100,  # 缩放级别
            'fit_to_window': True,  # 是否适应窗口
        },
        # 文件过滤设置
        'file_filter': {
            'supported_formats': ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif', 'tiff', 'tif'],
            'show_hidden_files': False,  # 是否显示隐藏文件
            'sort_by': 'name',  # 排序方式: 'name', 'date', 'size', 'type'
            'sort_order': 'asc',  # 排序顺序: 'asc', 'desc'
        },
        # 历史记录
        'history': {
            'enabled': True,  # 是否启用历史记录
            'max_entries': 100,  # 最大历史记录数
            'recent_directories': [],  # 最近使用的目录
        },
        # 日志设置
        'logging': {
            'enabled': True,  # 是否启用日志
            'level': 'INFO',  # 日志级别: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            'max_file_size': 10,  # 日志文件最大大小(MB)
            'backup_count': 5,  # 日志备份数量
        }
    }
    
    # 配置验证规则 - 定义每个配置项的验证方法
    VALIDATION_RULES = {
        'appearance.theme': {
            'type': 'string',
            'allowed': ['dark', 'light']
        },
        'appearance.language': {
            'type': 'string',
            'allowed': ['zh_CN', 'en_US']
        },
        'appearance.font_size': {
            'type': 'int',
            'min': 8,
            'max': 24
        },
        'appearance.window_width': {
            'type': 'int',
            'min': 800,
            'max': 3840
        },
        'appearance.window_height': {
            'type': 'int',
            'min': 600,
            'max': 2160
        },
        'processing.output_format': {
            'type': 'string',
            'allowed': ['png', 'jpg', 'webp', 'bmp', 'tiff']
        },
        'processing.quality': {
            'type': 'int',
            'min': 1,
            'max': 100
        },
        'performance.max_workers': {
            'type': 'int',
            'min': 1,
            'max': 16
        },
        'performance.preview_size': {
            'type': 'int',
            'min': 50,
            'max': 500
        },
        'image.resize_mode': {
            'type': 'string',
            'allowed': ['fit', 'fill', 'stretch']
        },
        'image.rotate_quality': {
            'type': 'string',
            'allowed': ['low', 'medium', 'high']
        },
        'image.compression_level': {
            'type': 'int',
            'min': 0,
            'max': 9
        },
        'image.watermark_opacity': {
            'type': 'float',
            'min': 0.0,
            'max': 1.0
        },
    }
    
    def __init__(
        self,
        config_file: Optional[str] = None,
        auto_save: bool = True,
        config_dir: Optional[str] = None
    ):
        """
        初始化配置系统
        
        Args:
            config_file: 配置文件名,默认为 'config.json'
            auto_save: 是否在设置值时自动保存,默认 True
            config_dir: 配置目录,默认为用户配置目录
        """
        self.auto_save = auto_save
        
        # 设置配置文件路径
        if config_dir is None:
            self.config_dir = self._get_default_config_dir()
        else:
            self.config_dir = Path(config_dir)
        
        # 创建配置目录(如果不存在)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置文件路径
        if config_file is None:
            self.config_file = self.config_dir / 'config.json'
        else:
            self.config_file = self.config_dir / config_file
        
        # 配置数据
        self._config: Dict[str, Any] = {}
        
        # 原始配置(用于检测变更)
        self._original_config: Dict[str, Any] = {}
        
        # 加载配置
        self._load()
        
        # 信号发射器 - 用于通知配置变更
        if HAS_PYSIDE6:
            self.config_changed = Signal(str, object)
    
    def _get_default_config_dir(self) -> Path:
        """
        获取默认的配置目录
        
        优先使用 QStandardPaths,否则使用当前目录下的 config 文件夹
        
        Returns:
            Path: 配置目录路径
        """
        if HAS_PYSIDE6:
            try:
                from PySide6.QtCore import QStandardPaths
                config_dir = QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.AppConfigLocation
                )
                return Path(config_dir)
            except ImportError:
                pass
        
        # 回退到当前目录
        return Path.cwd() / 'config'
    
    def _load(self) -> bool:
        """
        从文件加载配置
        
        如果配置文件不存在或加载失败,使用默认配置
        
        Returns:
            bool: 是否成功加载
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # 合并配置,保留默认值
                self._config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
                self._original_config = copy.deepcopy(self._config)
                return True
            except (json.JSONDecodeError, IOError) as e:
                print(f"加载配置文件失败: {e}")
                self._config = copy.deepcopy(self.DEFAULT_CONFIG)
                self._original_config = copy.deepcopy(self.DEFAULT_CONFIG)
                return False
        else:
            # 使用默认配置
            self._config = copy.deepcopy(self.DEFAULT_CONFIG)
            self._original_config = copy.deepcopy(self.DEFAULT_CONFIG)
            return True
    
    def _merge_config(
        self,
        default: Dict[str, Any],
        loaded: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        合并默认配置和加载的配置
        
        保留默认配置中的所有键,使用加载的值覆盖
        
        Args:
            default: 默认配置
            loaded: 加载的配置
            
        Returns:
            Dict: 合并后的配置
        """
        result = copy.deepcopy(default)
        
        for key, value in loaded.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_config(result[key], value)
                else:
                    result[key] = value
            else:
                # 保留加载配置中的新键
                result[key] = value
        
        return result
    
    def save(self, config_file: Optional[str] = None) -> bool:
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径(可选)
            
        Returns:
            bool: 是否成功保存
        """
        target_file = self.config_dir / config_file if config_file else self.config_file
        
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(
                    self._config,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    sort_keys=True
                )
            self._original_config = copy.deepcopy(self._config)
            return True
        except IOError as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def _get_nested_value(self, config: Dict[str, Any], key_path: str) -> Any:
        """
        获取嵌套配置值
        
        Args:
            config: 配置字典
            key_path: 键路径,使用点号分隔,例如 'appearance.theme'
            
        Returns:
            配置值,如果键不存在返回 None
        """
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def _set_nested_value(self, config: Dict[str, Any], key_path: str, value: Any) -> bool:
        """
        设置嵌套配置值
        
        Args:
            config: 配置字典
            key_path: 键路径,使用点号分隔
            value: 要设置的值
            
        Returns:
            bool: 是否成功设置
        """
        keys = key_path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return True
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key_path: 键路径,例如 'appearance.theme'
            default: 默认值,如果键不存在返回此值
            
        Returns:
            配置值或默认值
        """
        value = self._get_nested_value(self._config, key_path)
        return value if value is not None else default
    
    def set(self, key_path: str, value: Any, validate: bool = True) -> bool:
        """
        设置配置值
        
        Args:
            key_path: 键路径
            value: 要设置的值
            validate: 是否进行验证,默认 True
            
        Returns:
            bool: 是否成功设置
        """
        # 验证配置值
        if validate and key_path in self.VALIDATION_RULES:
            if not self._validate_value(key_path, value):
                print(f"配置值验证失败: {key_path} = {value}")
                return False
        
        # 设置值
        self._set_nested_value(self._config, key_path, value)
        
        # 发射配置变更信号
        if HAS_PYSIDE6 and hasattr(self, 'config_changed'):
            self.config_changed.emit(key_path, value)
        
        # 自动保存
        if self.auto_save:
            self.save()
        
        return True
    
    def _validate_value(self, key_path: str, value: Any) -> bool:
        """
        验证配置值是否符合规则
        
        Args:
            key_path: 键路径
            value: 要验证的值
            
        Returns:
            bool: 验证是否通过
        """
        rule = self.VALIDATION_RULES.get(key_path)
        if not rule:
            return True  # 没有验证规则,通过验证
        
        rule_type = rule.get('type')
        
        if rule_type == 'string':
            allowed = rule.get('allowed')
            return ConfigValidator.validate_string(value, allowed)
        elif rule_type == 'int':
            return ConfigValidator.validate_int(
                value,
                rule.get('min'),
                rule.get('max')
            )
        elif rule_type == 'float':
            return ConfigValidator.validate_float(
                value,
                rule.get('min'),
                rule.get('max')
            )
        elif rule_type == 'bool':
            return ConfigValidator.validate_bool(value)
        elif rule_type == 'list':
            return ConfigValidator.validate_list(value)
        
        return True
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            Dict: 完整配置字典的副本
        """
        return copy.deepcopy(self._config)
    
    def update(self, config_dict: Dict[str, Any], validate: bool = True) -> bool:
        """
        批量更新配置
        
        Args:
            config_dict: 要更新的配置字典
            validate: 是否进行验证
            
        Returns:
            bool: 是否全部更新成功
        """
        success = True
        
        for key_path, value in self._flatten_dict(config_dict).items():
            if not self.set(key_path, value, validate=validate):
                success = False
        
        return success
    
    def _flatten_dict(
        self,
        d: Dict[str, Any],
        parent_key: str = '',
        sep: str = '.'
    ) -> Dict[str, Any]:
        """
        将嵌套字典展平为单层字典
        
        Args:
            d: 要展平的字典
            parent_key: 父键前缀
            sep: 键分隔符
            
        Returns:
            Dict: 展平后的字典
        """
        items = []
        
        for key, value in d.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key, sep).items())
            else:
                items.append((new_key, value))
        
        return dict(items)
    
    def reset(self, key_path: Optional[str] = None):
        """
        重置配置为默认值
        
        Args:
            key_path: 要重置的键路径,如果为 None 则重置所有配置
        """
        if key_path is None:
            # 重置所有配置
            self._config = copy.deepcopy(self.DEFAULT_CONFIG)
            self._original_config = copy.deepcopy(self.DEFAULT_CONFIG)
        else:
            # 重置特定配置项
            default_value = self._get_nested_value(self.DEFAULT_CONFIG, key_path)
            if default_value is not None:
                self._set_nested_value(self._config, key_path, copy.deepcopy(default_value))
        
        # 保存重置后的配置
        self.save()
    
    def has_changed(self) -> bool:
        """
        检查配置是否已修改
        
        Returns:
            bool: 配置是否与保存时不同
        """
        return self._config != self._original_config
    
    @classmethod
    def get_instance(
        cls,
        config_file: Optional[str] = None,
        auto_save: bool = True,
        config_dir: Optional[str] = None
    ) -> 'Config':
        """
        获取配置系统单例实例
        
        Args:
            config_file: 配置文件名
            auto_save: 是否自动保存
            config_dir: 配置目录
            
        Returns:
            Config: 配置系统实例
        """
        if cls._instance is None:
            cls._instance = cls(
                config_file=config_file,
                auto_save=auto_save,
                config_dir=config_dir
            )
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """
        重置单例实例
        
        用于测试或重新初始化配置系统
        """
        if cls._instance is not None:
            # 保存当前配置
            cls._instance.save()
            cls._instance = None
    
    def export_config(self, file_path: str) -> bool:
        """
        导出配置到指定文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            bool: 是否成功导出
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    self._config,
                    f,
                    indent=4,
                    ensure_ascii=False,
                    sort_keys=True
                )
            return True
        except IOError as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config(self, file_path: str, merge: bool = True) -> bool:
        """
        从指定文件导入配置
        
        Args:
            file_path: 导入文件路径
            merge: 是否与现有配置合并,False 则替换
            
        Returns:
            bool: 是否成功导入
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            if merge:
                self._config = self._merge_config(self._config, imported_config)
            else:
                self._config = self._merge_config(self.DEFAULT_CONFIG, imported_config)
            
            self.save()
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"导入配置失败: {e}")
            return False


# 便捷函数
def get_config(**kwargs) -> Config:
    """
    获取配置系统实例的便捷函数
    
    Args:
        **kwargs: 传递给 Config.get_instance 的参数
        
    Returns:
        Config: 配置系统实例
    """
    return Config.get_instance(**kwargs)


if __name__ == '__main__':
    # 测试配置系统
    print("测试配置系统...")
    
    # 获取配置实例
    config = Config.get_instance(config_file='test_config.json')
    
    # 测试获取配置
    print(f"当前主题: {config.get('appearance.theme')}")
    print(f"输出格式: {config.get('processing.output_format')}")
    
    # 测试设置配置
    config.set('appearance.theme', 'light', validate=True)
    print(f"修改后主题: {config.get('appearance.theme')}")
    
    # 测试批量获取
    print(f"所有外观设置: {config.get('appearance')}")
    
    # 测试配置验证
    print("\n测试配置验证:")
    print(f"设置有效的字体大小(14): {config.set('appearance.font_size', 14)}")
    print(f"设置无效的字体大小(50): {config.set('appearance.font_size', 50)}")
    
    # 测试配置变更检测
    print(f"\n配置已修改: {config.has_changed()}")
    
    # 保存配置
    config.save()
    
    # 重置配置
    print("\n重置为默认配置...")
    config.reset()
    print(f"重置后主题: {config.get('appearance.theme')}")
    
    print(f"\n配置文件位置: {config.config_file}")
    print("配置系统测试完成!")
