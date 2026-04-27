from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget


class Color(QWidget):
    """Simple color widget for placeholder purposes."""

    def __init__(self, color):
        """Initialize widget."""
        super().__init__()

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
