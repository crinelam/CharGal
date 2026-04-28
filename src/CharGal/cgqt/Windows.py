from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QUndoStack, QKeySequence, QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget, QApplication, QToolBar
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget
from cgqt.Widgets import Color, CharactersTree


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

        self.setWindowTitle("Character Gallery")
        # TODO: Set Window Icon
        # self.setWindowIcon(QIcon(""))
        self.showMaximized()

        self.initElements()

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
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        for color in ["red", "green", "blue", "yellow"]:
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)

    def initMenu(self):
        """Initialize menu."""
        menu = self.menuBar()
        mFile = menu.addMenu("&File")
        mEdit = menu.addMenu("&Edit")
        mHelp = menu.addMenu("&Help")

        aExit = QAction("E&xit", self)
        aExit.setShortcut("Alt+F4")
        aExit.triggered.connect(self.quit)
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
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        aNewChar = QAction(QIcon("assets/icons/blue-document--plus.png"),
                           "New Character", self)
        aNewChar.setStatusTip("Create a new character")
        aNewChar.triggered.connect(self.newChar)
        toolbar.addAction(aNewChar)

        self.addToolBar(toolbar)

    def initTree(self):
        """Initialize characters tree."""
        tree = CharactersTree()

        # TODO: Save Last Area it was docked in
        self.addDockWidget(Qt.LeftDockWidgetArea, tree)

    def showAbout(self):
        """Show about popup."""
        self.popup = AboutPopup(self)
        self.popup.setGeometry(QRect((self.width() - 400) / 2, (self.height() - 200) / 2,
                                     400, 200))
        self.popup.show()

    def newChar(self):
        """Open dialog to create a new character."""
        # TODO: New Character dialog and creation.
        print("newChar not implemented yet :C")

    def quit(self):
        """Close the app."""
        QApplication.closeAllWindows()
        QApplication.quit()
