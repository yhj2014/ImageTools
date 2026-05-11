# -*- coding: utf-8 -*-
"""
文件列表组件模块
提供文件列表展示、拖拽添加、右键菜单等功能的自定义列表组件
继承自 QListWidget，支持多选和文件过滤
"""

from PySide6.QtWidgets import (
    QListWidget, QListWidgetItem, QMenu, QMessageBox, 
    QFileDialog, QApplication
)
from PySide6.QtCore import Signal, Qt, QMimeData, QSize
from PySide6.QtGui import QIcon, QAction, QDragEnterEvent, QDropEvent
import os
from typing import List, Optional


class FileListWidget(QListWidget):
    """
    文件列表组件类
    
    功能特性：
    - 继承自 QListWidget，提供文件列表展示
    - 支持拖拽添加文件（从文件系统拖入）
    - 支持多选操作
    - 右键菜单（删除选中、清空列表）
    - 文件类型过滤（只显示图片文件）
    - 实时显示文件数量
    
    信号：
    - files_dropped: 当文件被拖入列表时发出，参数为文件路径列表
    - files_removed: 当文件从列表中移除时发出，参数为被移除的文件路径列表
    
    支持的图片格式：
    - JPEG: .jpg, .jpeg
    - PNG: .png
    - BMP: .bmp
    - GIF: .gif
    - TIFF: .tiff, .tif
    - WebP: .webp
    - ICO: .ico
    """
    
    # 类属性：支持的图片文件扩展名
    SUPPORTED_IMAGE_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.bmp', '.gif', 
        '.tiff', '.tif', '.webp', '.ico'
    }
    
    def __init__(self, parent=None):
        """
        初始化文件列表组件
        
        Args:
            parent: 父窗口部件，默认为 None
        """
        super().__init__(parent)
        
        # 启用拖拽功能
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        
        # 文件列表存储
        self._file_paths: List[str] = []
        
        # 初始化右键菜单
        self._setup_context_menu()
        
        # 初始化组件
        self._setup_ui()
        
        # 连接信号
        self.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _setup_ui(self):
        """
        设置用户界面属性
        """
        # 设置列表项图标大小
        self.setIconSize(QSize(24, 24))
        
        # 启用滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 设置视图模式
        self.setViewMode(QListWidget.ViewMode.ListMode)
    
    def _setup_context_menu(self):
        """
        设置右键上下文菜单
        """
        # 创建右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    def _show_context_menu(self, position):
        """
        显示右键上下文菜单
        
        Args:
            position: 菜单位置（相对于组件的坐标）
        """
        # 如果有选中的项目，显示完整菜单；否则显示清空菜单
        menu = QMenu(self)
        
        if self.selectedItems():
            # 添加删除选中项菜单
            delete_action = QAction("删除选中", self)
            delete_action.triggered.connect(self._delete_selected)
            menu.addAction(delete_action)
            
            # 添加分隔线
            menu.addSeparator()
        
        # 添加清空列表菜单
        clear_action = QAction("清空列表", self)
        clear_action.triggered.connect(self.clear_list)
        menu.addAction(clear_action)
        
        # 添加分隔线
        menu.addSeparator()
        
        # 添加添加文件菜单
        add_action = QAction("添加文件...", self)
        add_action.triggered.connect(self.add_files_dialog)
        menu.addAction(add_action)
        
        # 显示菜单
        menu.exec(self.mapToGlobal(position))
    
    def _delete_selected(self):
        """
        删除选中的文件项
        """
        # 获取选中的项目
        selected_items = self.selectedItems()
        
        if not selected_items:
            return
        
        # 获取被删除文件的路径
        removed_paths = []
        
        # 遍历所有选中的项目并删除
        for item in selected_items:
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and os.path.exists(file_path):
                removed_paths.append(file_path)
            
            # 从列表中移除项目
            row = self.row(item)
            self.takeItem(row)
            
            # 从文件路径列表中移除
            if file_path in self._file_paths:
                self._file_paths.remove(file_path)
        
        # 发出文件移除信号
        if removed_paths:
            self.files_removed.emit(removed_paths)
        
        # 更新文件数量显示
        self._update_count_label()
    
    def _on_selection_changed(self):
        """
        当选择改变时的处理函数
        """
        # 可以在这里添加选择改变时的处理逻辑
        pass
    
    def _update_count_label(self):
        """
        更新文件数量标签
        可以被子类重写以提供自定义的显示方式
        """
        count = len(self._file_paths)
        self.setWindowTitle(f"文件列表 ({count})")
    
    def _is_valid_image_file(self, file_path: str) -> bool:
        """
        检查文件是否为有效的图片文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            bool: 如果是有效的图片文件返回 True，否则返回 False
        """
        # 获取文件扩展名（转小写）
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # 检查扩展名是否在支持的列表中
        return ext in self.SUPPORTED_IMAGE_EXTENSIONS
    
    def _get_file_icon(self, file_path: str) -> QIcon:
        """
        根据文件类型获取图标
        
        Args:
            file_path: 文件路径
        
        Returns:
            QIcon: 对应文件类型的图标
        """
        # 获取文件扩展名
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # 根据扩展名返回不同的图标
        icon_map = {
            '.jpg': "🖼️",
            '.jpeg': "🖼️",
            '.png': "🖼️",
            '.gif': "🎞️",
            '.bmp': "🖼️",
            '.tiff': "🖼️",
            '.tif': "🖼️",
            '.webp': "🖼️",
            '.ico': "🎨"
        }
        
        # 返回图标或默认图标
        icon_text = icon_map.get(ext, "📄")
        return QIcon.fromTheme("image-x-generic")
    
    def add_files_dialog(self):
        """
        打开文件选择对话框添加文件
        """
        # 打开文件选择对话框
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("选择图片文件")
        file_dialog.setNameFilters([
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.ico)",
            "所有文件 (*.*)"
        ])
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            self.add_files(file_paths)
    
    def add_files(self, file_paths: List[str]) -> int:
        """
        添加文件到列表
        
        Args:
            file_paths: 文件路径列表
        
        Returns:
            int: 成功添加的文件数量
        """
        added_count = 0
        
        for file_path in file_paths:
            # 检查是否为有效图片文件
            if not self._is_valid_image_file(file_path):
                continue
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                continue
            
            # 检查是否已经添加过
            if file_path in self._file_paths:
                continue
            
            # 添加到文件路径列表
            self._file_paths.append(file_path)
            
            # 创建列表项
            item = QListWidgetItem(os.path.basename(file_path), self)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            item.setToolTip(file_path)  # 设置工具提示显示完整路径
            
            # 设置图标
            icon = self._get_file_icon(file_path)
            if not icon.isNull():
                item.setIcon(icon)
            
            added_count += 1
        
        # 更新文件数量显示
        self._update_count_label()
        
        # 如果成功添加了文件，发出信号
        if added_count > 0:
            self.files_dropped.emit(file_paths)
        
        return added_count
    
    def remove_files(self, file_paths: List[str]) -> int:
        """
        从列表中移除指定文件
        
        Args:
            file_paths: 要移除的文件路径列表
        
        Returns:
            int: 成功移除的文件数量
        """
        removed_count = 0
        
        for file_path in file_paths:
            if file_path in self._file_paths:
                self._file_paths.remove(file_path)
                removed_count += 1
        
        # 重新构建列表项
        self._rebuild_items()
        
        # 发出文件移除信号
        if removed_count > 0:
            self.files_removed.emit(file_paths)
        
        return removed_count
    
    def clear_list(self):
        """
        清空文件列表
        """
        if not self._file_paths:
            return
        
        # 保存当前文件列表用于信号
        removed_paths = self._file_paths.copy()
        
        # 清空列表
        self._file_paths.clear()
        QListWidget.clear(self)
        
        # 发出文件移除信号
        self.files_removed.emit(removed_paths)
        
        # 更新文件数量显示
        self._update_count_label()
    
    def _rebuild_items(self):
        """
        重新构建列表项
        用于在文件列表更新后刷新显示
        """
        # 保存当前选择
        selected_paths = [item.data(Qt.ItemDataRole.UserRole) 
                         for item in self.selectedItems()]
        
        # 清空列表
        QListWidget.clear(self)
        
        # 重新添加所有文件
        for file_path in self._file_paths:
            # 创建列表项
            item = QListWidgetItem(os.path.basename(file_path), self)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            item.setToolTip(file_path)
            
            # 设置图标
            icon = self._get_file_icon(file_path)
            if not icon.isNull():
                item.setIcon(icon)
        
        # 恢复选择状态
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.ItemDataRole.UserRole) in selected_paths:
                item.setSelected(True)
        
        # 更新文件数量显示
        self._update_count_label()
    
    def get_files(self) -> List[str]:
        """
        获取列表中的所有文件路径
        
        Returns:
            List[str]: 文件路径列表
        """
        return self._file_paths.copy()
    
    def get_selected_files(self) -> List[str]:
        """
        获取当前选中的文件路径
        
        Returns:
            List[str]: 选中的文件路径列表
        """
        return [
            item.data(Qt.ItemDataRole.UserRole) 
            for item in self.selectedItems()
            if item.data(Qt.ItemDataRole.UserRole)
        ]
    
    def get_file_count(self) -> int:
        """
        获取文件数量
        
        Returns:
            int: 文件数量
        """
        return len(self._file_paths)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        处理拖拽进入事件
        
        Args:
            event: 拖拽进入事件
        """
        # 检查是否有文件被拖入
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        """
        处理拖拽移动事件
        
        Args:
            event: 拖拽移动事件
        """
        # 接受拖拽移动
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """
        处理文件放下事件
        
        Args:
            event: 放下事件
        """
        # 检查是否有文件放下
        if event.mimeData().hasUrls():
            # 获取拖入的文件路径列表
            file_paths = []
            
            for url in event.mimeData().urls():
                # 将 URL 转换为本地文件路径
                file_path = url.toLocalFile()
                if file_path and os.path.isfile(file_path):
                    file_paths.append(file_path)
            
            # 添加文件到列表
            if file_paths:
                self.add_files(file_paths)
                self.files_dropped.emit(file_paths)
            
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    
    def set_files(self, file_paths: List[str]):
        """
        设置文件列表（替换现有列表）
        
        Args:
            file_paths: 新的文件路径列表
        """
        # 清空现有列表
        self._file_paths.clear()
        QListWidget.clear(self)
        
        # 添加新文件
        if file_paths:
            self.add_files(file_paths)


# 信号定义
FileListWidget.files_dropped = Signal(list)  # 文件被拖入时的信号
FileListWidget.files_removed = Signal(list)   # 文件被移除时的信号
