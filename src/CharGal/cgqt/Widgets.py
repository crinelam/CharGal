from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget, QDockWidget, QTreeWidget, QTreeWidgetItem


class Color(QWidget):
    """Simple color widget for placeholder purposes."""

    def __init__(self, color):
        """Initialize widget."""
        super().__init__()

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



class CharactersTree(QDockWidget):
    """Tree widget for character organization."""

    def __init__(self):
        super().__init__()

        data = {"Folder A": ["Character 1", "Character 2", "Character 3"],
                "Folder B": ["Character 1", "Character 2"],
                "Folder C": []}

        self.setWindowTitle("Characters Folders")

        self.setFeatures(self.DockWidgetFeature.DockWidgetMovable | self.DockWidgetFeature.DockWidgetVerticalTitleBar)
        self.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        
        tree = QTreeWidget()

        tree.setHeaderLabels([""])

        # Load data TODO: Load from DB.
        # TODO: Separate into it's own function.
        items = []
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                child = QTreeWidgetItem([value])
                item.addChild(child)
            items.append(item)
        tree.insertTopLevelItems(0, items)

        self.setWidget(tree)
