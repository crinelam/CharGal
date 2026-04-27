from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget
from cgqt.Widgets import Color, CharactersTree


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self):
        """Initialize window."""
        super().__init__()

        self.setWindowTitle("Character Gallery")
        self.showMaximized()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        for color in ["red", "green", "blue", "yellow"]:
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)

        tree = CharactersTree()

        # TODO: Save Last Area it was docked in
        self.addDockWidget(Qt.LeftDockWidgetArea, tree)
