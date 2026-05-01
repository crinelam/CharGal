from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QUndoStack, QKeySequence, QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget, QApplication, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget
from cgqt.Widgets import Color, CharactersTree
from Config import DirectoryManager
from alchemy.db import *
import json


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
        link = QLabel("<a href=\"http://creativecommons.org/licenses/by/3.0/\">http://creativecommons.org/licenses/by/3.0/</a>")
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

        for color in ["red", "green", "blue", "yellow"]:
            self.tabs.addTab(Color(color), color)

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

        aNewFolder = QAction(QIcon("assets/icons/blue-folder--plus.png"),
                             "New Folder", self)
        aNewFolder.setStatusTip("Create a new folder")
        aNewFolder.triggered.connect(self.newFolder)
        self.toolbar.addAction(aNewFolder)

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

    def newFolder(self):
        """Open dialog to create a new folder."""
        # TODO: New Folder dialog and creation.
        print("newFolder not implemented yet :C")
        self.db.saveFolder(Folder(name="Test"))

    def closeTabHandler(self, index):
        """Handle tab closure."""
        # TODO: Ask to save changes and allow to cancel the closure.
        self.tabs.removeTab(index)

    def changedDocked(self):
        location = self.tree.dockLocation()
        if location == Qt.LeftDockWidgetArea:
            self.config["treeDockedArea"] = "Left"
        else:
            self.config["treeDockedArea"] = "Right"
        self.dirMan.saveConfig(self.config)
        
    def closeEvent(self, event):
        """Close event."""
        # TODO: Detect unsaved character changes.
        print("Closing")
        self.dirMan.saveConfig(self.config)
        event.accept()
