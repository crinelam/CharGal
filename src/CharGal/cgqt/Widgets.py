from PySide6.QtCore import Qt
from PySide6.QtGui import (QColor, QPalette, QIcon, QPixmap)
from PySide6.QtWidgets import (QWidget, QDockWidget, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QHBoxLayout,
                               QLabel, QFormLayout, QLineEdit, QPushButton,
                               QTextEdit, QCheckBox, QStackedWidget,
                               QScrollArea, QSizePolicy, QListWidget)
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

        self.scrollArea = QScrollArea()

        self.scrollArea.setWidget(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.db = DB()

        self.info = self.db.getCharacterById(characterId)

        self.layout.addWidget(CharacterInfoHeader(self.info))

        self.layout.addWidget(CharacterDescription(self.info["description"]))

        self.layout.addWidget(CharacterGallery(self.info["id"]))


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
        self.formLayout1.addRow(QLabel("age"), self.ageEdit)
        self.formLayout1.addRow(QLabel("birthday"), self.birthdayEdit)
        self.formLayout1.addRow(QLabel("job"), self.jobEdit)

        self.info2 = QWidget()
        self.formLayout2 = QFormLayout()
        self.info2.setLayout(self.formLayout2)
        self.formLayout2.addRow(QLabel("eyes"), self.eyesEdit)
        self.formLayout2.addRow(QLabel("hair"), self.hairEdit)
        self.formLayout2.addRow(QLabel("height"), self.heightEdit)
        self.formLayout2.addRow(QLabel("weight"), self.weightEdit)
        self.formLayout2.addRow(QLabel("species"), self.speciesEdit)

        self.layout.addWidget(self.info1)
        self.layout.addWidget(self.info2)

        self.layout.addWidget(CharacterTags(info["id"]))
        self.layout.addWidget(CharacterFiles(info["id"]))

        self.setFixedHeight(210)


class CharacterTags(QWidget):
    """Character tags."""

    def __init__(self, characterId):
        """Initialize widget."""
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bEdit = QPushButton("Edit tags.")
        self.layout.addWidget(self.bEdit)

        self.tagsWidget = QWidget()
        self.layout.addWidget(self.tagsWidget)
        self.tagsWidget.setStyleSheet("border: 1px solid gray;")
        self.setFixedWidth(200)
        self.setFixedHeight(200)


class CharacterFiles(QWidget):
    """Character files."""

    def __init__(self, characterId):
        """Initialize widget."""
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bAddFile = QPushButton("Add file.")
        self.layout.addWidget(self.bAddFile)

        self.filesWidget = QListWidget()
        self.layout.addWidget(self.filesWidget)
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        placeholderData = ["File1.txt", "File2.pdf", "File3"]
        self.filesWidget.addItems(placeholderData)


class CharacterImage(QLabel):
    """Character image."""

    def __init__(self, imageName):
        """Initialize widget."""
        super().__init__()

        self.setStyleSheet("border: 1px solid gray;")
        self.setFixedWidth(200)
        self.setFixedHeight(200)

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


class CharacterDescription(QWidget):
    """Character description widget."""

    def __init__(self, description):
        """Initialize Widget."""
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text = description

        self.cEdit = QCheckBox("Edit Description")
        self.layout.addWidget(self.cEdit)
        self.cEdit.checkStateChanged.connect(self.changeEditMode)

        self.stacked = QStackedWidget()

        self.markdownViewer = QTextEdit(readOnly=True)
        self.markdownViewer.setMarkdown(self.text)

        self.markdownEditor = QTextEdit()
        self.markdownEditor.setText(self.text)

        self.stacked.addWidget(self.markdownViewer)
        self.stacked.addWidget(self.markdownEditor)

        self.layout.addWidget(self.stacked)

    def changeEditMode(self):
        """Checkbox changed."""
        if self.cEdit.isChecked():
            self.stacked.setCurrentWidget(self.markdownEditor)
        else:
            self.stacked.setCurrentWidget(self.markdownViewer)
        self.markdownViewer.setMarkdown(self.markdownEditor.toPlainText())


class CharacterGallery(QWidget):
    """Character gallery widget."""

    def __init__(self, characterId):
        """Initialize widget."""
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.addImage = QPushButton("Add image")
        self.addImage.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.layout.addWidget(self.addImage)

        self.scrollArea = QScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Minimum)
        self.scrollArea.setFixedHeight(230)
        self.scrollArea.setWidget(ImageGallery(characterId))
        self.layout.addWidget(self.scrollArea)


class ImageGallery(QWidget):
    """Images gallery widget."""

    def __init__(self, characterId):
        """Initialize widget."""
        super().__init__()

        self.setStyleSheet("border: 1px solid gray;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.setFixedHeight(210)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.db = DB()

        images = self.db.getImagesByCharacterId(characterId)
        for image in images:
            imageWidget = CharacterImage(image)
            imageWidget.setContentsMargins(5, 5, 5, 5)
            self.layout.addWidget(imageWidget)


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
