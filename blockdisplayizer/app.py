import sys
from PySide6.QtWidgets import QApplication

from .gui.main_window import MainWindow


def main() -> None:
    """Entry point for the BlockDisplayizer application."""
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
