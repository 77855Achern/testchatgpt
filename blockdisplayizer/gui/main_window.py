"""Main application window."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QTabWidget,
    QLabel,
)

from .gl_view import GLViewWidget
from .panels.import_panel import ImportPanel
from .panels.voxel_panel import VoxelPanel
from .panels.orient_panel import OrientPanel
from .panels.color_panel import ColorPanel
from .panels.export_panel import ExportPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlockDisplayizer")
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.view = GLViewWidget()
        layout.addWidget(self.view, 1)
        # panels
        self.import_panel = ImportPanel()
        self.voxel_panel = VoxelPanel()
        self.orient_panel = OrientPanel()
        self.color_panel = ColorPanel()
        self.export_panel = ExportPanel()
        self.tabs.addTab(self.import_panel, "Import")
        self.tabs.addTab(self.voxel_panel, "Voxel")
        self.tabs.addTab(self.orient_panel, "Orient")
        self.tabs.addTab(self.color_panel, "Color")
        self.tabs.addTab(self.export_panel, "Export")
        self.statusBar().showMessage("Ready")
