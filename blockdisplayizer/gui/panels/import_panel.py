"""Import panel UI."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QFormLayout, QDoubleSpinBox, QLabel


class ImportPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.path_edit = QLineEdit()
        layout.addRow("GLB/GLTF Path", self.path_edit)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setValue(1.0)
        layout.addRow("Scale", self.scale_spin)
        self.load_btn = QPushButton("Load Model")
        layout.addRow(self.load_btn)
