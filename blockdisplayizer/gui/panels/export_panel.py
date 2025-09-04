"""Export panel."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFormLayout, QCheckBox, QPushButton, QLineEdit


class ExportPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.mcfunc_check = QCheckBox("Export mcfunction")
        self.mcfunc_path = QLineEdit("build.mcfunction")
        layout.addRow(self.mcfunc_check, self.mcfunc_path)
        self.bd_check = QCheckBox("Export BDEngine JSON")
        self.bd_path = QLineEdit("project.json")
        layout.addRow(self.bd_check, self.bd_path)
        self.export_btn = QPushButton("Export")
        layout.addRow(self.export_btn)
