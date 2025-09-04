"""Voxelisation panel."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFormLayout, QDoubleSpinBox, QPushButton, QCheckBox


class VoxelPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.size_spin = QDoubleSpinBox()
        self.size_spin.setValue(0.25)
        layout.addRow("Voxel size", self.size_spin)
        self.surface_only = QCheckBox("Surface only")
        self.surface_only.setChecked(True)
        layout.addRow(self.surface_only)
        self.voxel_btn = QPushButton("Voxelize")
        layout.addRow(self.voxel_btn)
