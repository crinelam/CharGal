from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QIcon, QPixmap
from PySide6.QtWidgets import (QWidget, QDockWidget, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QHBoxLayout,
                               QLabel, QFormLayout, QLineEdit)
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


class CharacterInfo(QWidget):
    """Character info widget."""

    def __init__(self, characterId):
        """Initialize widget."""
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.db = DB()

        self.info = self.db.getCharacterById(characterId)

        self.layout.addWidget(CharacterInfoHeader(self.info))


class CharacterInfoHeader(QWidget):
    """Character info header."""

    def __init__(self, info):
        """Initialize widget."""
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(CharacterImage(info["image"]),
                              alignment=Qt.AlignTop)

        self.nameEdit = QLineEdit(info["name"])
        self.pronounsEdit = QLineEdit(info["pronouns"])
        self.orientationEdit = QLineEdit(info["orientation"])

        self.ageEdit = QLineEdit(info["age"])
        self.birthdayEdit = QLineEdit(info["birthday"])
        self.eyesEdit = QLineEdit(info["eyes"])

        self.heightEdit = QLineEdit(info["height"])
        self.weightEdit = QLineEdit(info["weight"])
        self.hairEdit = QLineEdit(info["hair"])

        self.jobEdit = QLineEdit(info["job"])
        self.speciesEdit = QLineEdit(info["species"])

        self.info1 = QWidget()
        self.formLayout1 = QFormLayout()
        self.info1.setLayout(self.formLayout1)
        self.formLayout1.addRow(QLabel("name"), self.nameEdit)
        self.formLayout1.addRow(QLabel("pronouns"), self.pronounsEdit)
        self.formLayout1.addRow(QLabel("orientation"), self.orientationEdit)

        self.info2 = QWidget()
        self.formLayout2 = QFormLayout()
        self.info2.setLayout(self.formLayout2)
        self.formLayout2.addRow(QLabel("age"), self.ageEdit)
        self.formLayout2.addRow(QLabel("birthday"), self.birthdayEdit)
        self.formLayout2.addRow(QLabel("eyes"), self.eyesEdit)

        self.info3 = QWidget()
        self.formLayout3 = QFormLayout()
        self.info3.setLayout(self.formLayout3)
        self.formLayout3.addRow(QLabel("height"), self.heightEdit)
        self.formLayout3.addRow(QLabel("weight"), self.weightEdit)
        self.formLayout3.addRow(QLabel("hair"), self.hairEdit)

        self.info4 = QWidget()
        self.formLayout4 = QFormLayout()
        self.info4.setLayout(self.formLayout4)
        self.formLayout4.addRow(QLabel("job"), self.jobEdit)
        self.formLayout4.addRow(QLabel("species"), self.speciesEdit)

        self.layout.addWidget(self.info1)
        self.layout.addWidget(self.info2)
        self.layout.addWidget(self.info3)
        self.layout.addWidget(self.info4)


class CharacterImage(QLabel):
    """Character image."""

    def __init__(self, imageName):
        """Initialize widget."""
        super().__init__()

        self.defaultImage = QPixmap("assets/images/blankCharacter.png").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        self.dirMan = DirectoryManager()

        if imageName is not None:
            imagePath = self.dirMan.getImagePath(imageName)
            self.image = QPixmap(str(imagePath)).scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.image = self.defaultImage

        self.setPixmap(self.image)


class CharactersTree(QDockWidget):
    """Tree widget for character organization."""

    def __init__(self):
        """Initialize Widget."""
        super().__init__()

        self.db = DB()
        self.dirMan = DirectoryManager()

        self.setWindowTitle("Characters Folders")

        self.setFeatures(self.DockWidgetFeature.DockWidgetMovable)
        # | self.DockWidgetFeature.DockWidgetVerticalTitleBar)
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
