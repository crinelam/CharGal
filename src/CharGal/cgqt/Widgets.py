from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QIcon
from PySide6.QtWidgets import QWidget, QDockWidget, QTreeWidget, QTreeWidgetItem
from alchemy.db import DB
from Config import DirectoryManager


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
        """Initialize Widget."""
        super().__init__()

        self.db = DB()
        self.dirMan = DirectoryManager()

        self.setWindowTitle("Characters Folders")

        self.setFeatures(self.DockWidgetFeature.DockWidgetMovable)  # | self.DockWidgetFeature.DockWidgetVerticalTitleBar)
        self.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels(["Name", "Type", "ID"])
        self.tree.setColumnCount(3)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setSortingEnabled(True)

        self.folderIcon = QIcon("assets/icons/folder.png")
        self.characterIcon = QIcon("assets/icons/stickman-smiley.png")
        # Load data TODO: Load from DB.
        # TODO: Separate into it's own function.
        self.loadData()
        self.setWidget(self.tree)

    def loadData(self):
        """Load data."""
        rootFolders = self.db.getRootFolders()
        rootCharacters = self.db.getRootCharacters()

        for character in rootCharacters:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, character["name"])
            if character["image"] is not None:
                path = self.dirMan.getImagePath(character["image"])
                print(path)
                item.setIcon(0, QIcon(str(path)))
            else:
                item.setIcon(0, self.characterIcon)
            item.setText(1, character["type"])
            item.setText(2, str(character["id"]))
            self.tree.insertTopLevelItem(0, item)

        for root in rootFolders:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, root["name"])
            item.setIcon(0, self.folderIcon)
            item.setText(1, root["type"])
            item.setText(2, str(root["id"]))
            self.tree.insertTopLevelItem(0, item)
            self.loadCharacters(root["id"], item)
            self.loadChilds(root["id"], item)

    def loadChilds(self, id, parent):
        """Check if folder has childs and iterate."""
        childs = self.db.getFoldersByParentId(id)
        if not bool(childs):
            return
        else:
            for child in childs:
                item = QTreeWidgetItem(parent)
                item.setText(0, child["name"])
                item.setIcon(0, self.folderIcon)
                item.setText(1, child["type"])
                item.setText(2, str(child["id"]))
                parent.addChild(item)
                self.loadCharacters(child["id"], item)
                self.loadChilds(child["id"], item)

    def loadCharacters(self, id, parent):
        """Check if folder has characters."""
        characters = self.db.getCharactersByFolderId(id)
        if not bool(characters):
            return
        else:
            for character in characters:
                item = QTreeWidgetItem(parent)
                item.setText(0, character["name"])
                if character["image"] is not None:
                    path = self.dirMan.getImagePath(character["image"])
                    item.setIcon(0, QIcon(str(path)))
                else:
                    item.setIcon(0, self.characterIcon)
                item.setText(1, character["type"])
                item.setText(2, str(character["id"]))
                parent.addChild(item)
