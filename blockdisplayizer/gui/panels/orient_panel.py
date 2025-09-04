"""Orientation quantisation panel."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QDoubleSpinBox, QSpinBox, QPushButton


class OrientPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["6", "18", "26", "snap_0_45_90"])
        layout.addRow("Mode", self.mode_combo)
        self.tol_spin = QDoubleSpinBox()
        self.tol_spin.setValue(10.0)
        layout.addRow("Tolerance", self.tol_spin)
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setValue(1)
        layout.addRow("Min chart size", self.min_size_spin)
        self.mesh_btn = QPushButton("Greedy Meshing")
        layout.addRow(self.mesh_btn)
