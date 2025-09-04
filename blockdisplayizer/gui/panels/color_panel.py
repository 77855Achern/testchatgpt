"""Color assignment panel."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QDoubleSpinBox, QPushButton, QSlider


class ColorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.palette_combo = QComboBox()
        layout.addRow("Palette", self.palette_combo)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["DE76", "CIEDE2000"])
        layout.addRow("Method", self.method_combo)
        self.luma_slider = QSlider()
        self.luma_slider.setOrientation(1)  # horizontal
        self.luma_slider.setRange(0, 100)
        layout.addRow("Luma weight", self.luma_slider)
        self.apply_btn = QPushButton("Apply Colors")
        layout.addRow(self.apply_btn)
