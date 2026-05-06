from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QUndoStack, QKeySequence, QIcon
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QToolBar,
                               QVBoxLayout, QLabel, QWidget, QMessageBox)
from cgqt.Widgets import CharacterInfo, CharactersTree
from Config import DirectoryManager
from alchemy.db import DB
# import json


class AboutPopup(QWidget):
    """About Popup."""

    def __init__(self, parent):
        """Initialize popup."""
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)  # Qt.FramelessWindowHint)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Character Gallery"), 0, Qt.AlignCenter)
        layout.addWidget(QLabel("Created by crinelam"), 0, Qt.AlignCenter)
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(
            "Icons (C) 2013 Yusuke Kamiyamane. All rights reserved."),
                         0, Qt.AlignCenter)
        layout.addWidget(QLabel(
            "Licensed under a Creative Commons Attribution 3.0 License."),
                         0, Qt.AlignCenter)
        link = QLabel("<a href=\"http://creativecommons.org/licenses/by/3.0/\"_>http://creativecommons.org/licenses/by/3.0/</a>")
        link.setOpenExternalLinks(True)
        layout.addWidget(link, 0, Qt.AlignCenter)


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self):
        """Initialize window."""
        super().__init__()

        self.config = {}
        self.loadConfig()

        self.db = DB()

        self.setWindowTitle("Character Gallery")
        # TODO: Set Window Icon
        # self.setWindowIcon(QIcon(""))
        self.showMaximized()

        self.initElements()

    def loadConfig(self):
        """Load configuration."""
        self.dirMan = DirectoryManager()
        self.config = self.dirMan.loadConfig()
        # print(self.config)

    def initElements(self):
        """Initialize the gui elements."""
        self.initUndo()
        # Create main area.
        self.initMain()
        # Create menu.
        self.initMenu()
        # Create Toolbar.
        self.initToolbar()
        # Create charactes tree.
        self.initTree()

    def initUndo(self):
        """Initialize undo stack."""
        # TODO: Implement Undo Stack
        self.undoStack = QUndoStack()

    def initMain(self):
        """Initialize main area."""
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTabHandler)

        self.setCentralWidget(self.tabs)

    def initMenu(self):
        """Initialize menu."""
        self.menu = self.menuBar()
        mFile = self.menu.addMenu("&File")
        mEdit = self.menu.addMenu("&Edit")
        mHelp = self.menu.addMenu("&Help")

        aExit = QAction("E&xit", self)
        # aExit.setShortcut("Alt+F4")
        aExit.triggered.connect(self.close)
        mFile.addAction(aExit)

        aUndo = QAction("&Undo", self)
        aUndo.setShortcut(QKeySequence.Undo)
        aUndo.triggered.connect(self.undoStack.undo)
        mEdit.addAction(aUndo)

        aRedo = QAction("&Redo", self)
        aRedo.setShortcut(QKeySequence.Redo)
        aRedo.triggered.connect(self.undoStack.redo)
        mEdit.addAction(aRedo)

        aSave = QAction("&Save", self)
        aSave.setShortcut(QKeySequence.Save)
        aSave.triggered.connect(self.saveCharacter)
        mEdit.addAction(aSave)

        aAbout = QAction("About", self)
        aAbout.triggered.connect(self.showAbout)
        mHelp.addAction(aAbout)
        self.popup = None

    def initToolbar(self):
        """Initialize toolbar."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)

        aNewChar = QAction(QIcon("assets/icons/blue-document--plus.png"),
                           "New Character", self)
        aNewChar.setStatusTip("Create a new character")
        aNewChar.triggered.connect(self.newChar)
        self.toolbar.addAction(aNewChar)

        aNewFolder = QAction(QIcon("assets/icons/folder--plus.png"),
                             "New Folder", self)
        aNewFolder.setStatusTip("Create a new folder")
        aNewFolder.triggered.connect(self.newFolder)
        self.toolbar.addAction(aNewFolder)

        aSaveCharacter = QAction(QIcon("assets/icons/disk.png"),
                                 "Save Character", self)
        aSaveCharacter.setStatusTip("Save the current character")
        aSaveCharacter.triggered.connect(self.saveCharacter)
        self.toolbar.addAction(aSaveCharacter)

        self.addToolBar(self.toolbar)

    def initTree(self):
        """Initialize characters tree."""
        self.tree = CharactersTree()

        # TODO: Save Last Area it was docked in
        if "treeDockedArea" in self.config:
            area = self.config["treeDockedArea"]
            if area == "Left":
                self.addDockWidget(Qt.LeftDockWidgetArea, self.tree)
            else:
                self.addDockWidget(Qt.RightDockWidgetArea, self.tree)
        else:
            # Default value
            self.config["treeDockedArea"] = "Left"
            self.addDockWidget(Qt.LeftDockWidgetArea, self.tree)

        self.tree.dockLocationChanged.connect(self.changedDocked)
        self.tree.tree.doubleClicked.connect(self.openCharacter)

    def showAbout(self):
        """Show about popup."""
        self.popup = AboutPopup(self)
        self.popup.setGeometry(QRect((self.width() - 400) / 2,
                                     (self.height() - 200) / 2,
                                     400, 200))
        self.popup.show()

    def newChar(self):
        """Open dialog to create a new character."""
        # TODO: New Character dialog and creation.
        print("newChar not implemented yet :C")

    def openCharacter(self, index):
        """Open clicked character."""
        item = self.tree.tree.itemFromIndex(index)
        type = item.data(1, 0)
        if type == "Character":
            id = item.data(2, 0)
            icon = item.icon(0)
            index = self.tabs.addTab(CharacterInfo(id), icon,
                                     self.db.getCharacterNameById(id))
            self.tabs.setCurrentIndex(index)

    def saveCharacter(self):
        """Save Character."""
        characterWidget = self.tabs.currentWidget()
        if characterWidget is not None:
            self.db.updateCharacter(characterWidget.info)

    def newFolder(self):
        """Open dialog to create a new folder."""
        # TODO: New Folder dialog and creation.
        print("newFolder not implemented yet :C")

    def closeTabHandler(self, index):
        """Handle tab closure."""
        # TODO: Ask to save changes and allow to cancel the closure.
        item = self.tabs.widget(index)
        dbInfo = self.db.getCharacterById(item.info["id"])
        if dbInfo != item.info:
            confirmDialog = QMessageBox.warning(self, "Save changes?",
                                                "The character is not saved, do you want to save changes?",
                                                buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                                defaultButton=QMessageBox.Cancel)
            if confirmDialog == QMessageBox.Save:
                self.saveCharacter()
                self.tabs.removeTab(index)
            elif confirmDialog == QMessageBox.Discard:
                self.tabs.removeTab(index)
        else:
            self.tabs.removeTab(index)

    def refreshCharacterImage(self, characterId):
        """Refresh character image."""
        character = self.db.getCharacterById(characterId)
        imagePath = self.dirMan.getImagePath(character["image"],
                                             character["id"],
                                             character["name"])

        items = self.tree.tree.findItems(str(characterId), Qt.MatchExactly, 2)
        characterItem = None
        for item in items:
            type = item.data(1, 0)
            if type == "Character":
                characterItem = item
                break
        if characterItem:
            characterItem.setIcon(0, QIcon(str(imagePath)))

        characterTabIndex = self.tabs.indexOf(self.tabs.currentWidget())
        self.tabs.setTabIcon(characterTabIndex, QIcon(str(imagePath)))

    def changedDocked(self):
        """Trigger when the docked widget position is changed."""
        location = self.tree.dockLocation()
        if location == Qt.LeftDockWidgetArea:
            self.config["treeDockedArea"] = "Left"
        else:
            self.config["treeDockedArea"] = "Right"
        self.dirMan.saveConfig(self.config)

    def closeEvent(self, event):
        """Close event."""
        self.dirMan.saveConfig(self.config)
        tabCount = self.tabs.count()
        hasChanges = False
        if tabCount > 0:
            for i in range(tabCount):
                item = self.tabs.widget(i)
                dbInfo = self.db.getCharacterById(item.info["id"])
                if dbInfo != item.info:
                    hasChanges = True
                    break
        if hasChanges:
            confirmDialog = QMessageBox.warning(self, "Save changes?",
                                                "You have open characters with unsaved changes, do you want to save all changes before closing?",
                                                buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                                defaultButton=QMessageBox.Cancel)
            if confirmDialog == QMessageBox.Save:
                for i in range(tabCount):
                    self.tabs.setCurrentIndex(i)
                    self.saveCharacter()
                event.accept()
            elif confirmDialog == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
