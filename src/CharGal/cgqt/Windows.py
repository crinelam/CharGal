#        CharGal, a Character Gallery.
#        Copyright (C) 2026 crinelam
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QUndoStack, QKeySequence, QIcon
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QToolBar,
                               QVBoxLayout, QLabel, QWidget, QMessageBox,
                               QDialog, QDialogButtonBox, QFormLayout,
                               QLineEdit, QTreeWidget, QTreeWidgetItem)
from cgqt.Widgets import CharacterInfo, CharactersTree
from Config import DirectoryManager
from alchemy.db import DB
import alchemy.db


class AboutPopup(QWidget):
    """About Popup."""

    def __init__(self, parent):
        """Initialize popup."""
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)  # Qt.FramelessWindowHint)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("CharGal v0.1.0 Copyright (C) 2026 crinelam"), 0, Qt.AlignCenter)
        layout.addWidget(QLabel("This program comes with ABSOLUTELY NO WARRANTY; for details visit <a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">https://www.gnu.org/licenses/gpl-3.0.html</a>"), 0, Qt.AlignCenter)
        layout.addWidget(QLabel("This is free software, and you are welcome to redistribute it"), 0, Qt.AlignCenter)
        layout.addWidget(QLabel("under certain conditions; visit <a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">https://www.gnu.org/licenses/gpl-3.0.html</a> for details"), 0, Qt.AlignCenter)
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


class NewCharacterDialog(QDialog):
    """New character dialog."""

    def __init__(self, parent):
        """Initialize dialog."""
        super().__init__(parent)

        self.db = DB()

        self.setWindowTitle("New Character")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QFormLayout()

        self.nameEdit = QLineEdit()
        self.layout.addRow(QLabel("Name"), self.nameEdit)

        self.folderSelect = QTreeWidget()
        self.folderSelect.setHeaderLabels(["Name", "ID"])
        self.folderSelect.setColumnCount(2)
        self.folderSelect.setColumnHidden(1, True)
        self.folderSelect.setSortingEnabled(True)

        self.folderIcon = QIcon("assets/icons/folder.png")
        self.initFolders()

        self.layout.addRow(QLabel("Folder"), self.folderSelect)

        self.layout.addRow(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        """Accept event."""
        folderItem = self.folderSelect.currentItem()
        if folderItem:
            character = alchemy.db.Character(name=self.nameEdit.text(),
                                             folder=folderItem.data(1, 0))
        else:
            character = alchemy.db.Character(name=self.nameEdit.text())
        id = self.db.saveCharacter(character)
        self.parent().openNewCharacter(id)
        self.close()

    def initFolders(self):
        """Initialize folders."""
        rootFolders = self.db.getRootFolders()

        for root in rootFolders:
            item = QTreeWidgetItem(self.folderSelect)
            item.setText(0, root["name"])
            item.setIcon(0, self.folderIcon)
            item.setText(1, str(root["id"]))
            self.folderSelect.insertTopLevelItem(0, item)
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
                item.setText(1, str(child["id"]))
                parent.addChild(item)
                self.loadChilds(child["id"], item)


class NewFolderDialog(QDialog):
    """New character dialog."""

    def __init__(self, parent):
        """Initialize dialog."""
        super().__init__(parent)

        self.db = DB()

        self.setWindowTitle("New Folder")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QFormLayout()

        self.nameEdit = QLineEdit("New Folder")
        self.layout.addRow(QLabel("Name"), self.nameEdit)

        self.folderSelect = QTreeWidget()
        self.folderSelect.setHeaderLabels(["Name", "ID"])
        self.folderSelect.setColumnCount(2)
        self.folderSelect.setColumnHidden(1, True)
        self.folderSelect.setSortingEnabled(True)

        self.folderIcon = QIcon("assets/icons/folder.png")
        self.initFolders()

        self.layout.addRow(QLabel("Folder"), self.folderSelect)

        self.layout.addRow(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        """Accept event."""
        folderItem = self.folderSelect.currentItem()
        if folderItem:
            folder = alchemy.db.Folder(name=self.nameEdit.text(),
                                       parentId=folderItem.data(1, 0))
        else:
            folder = alchemy.db.Folder(name=self.nameEdit.text())
        folderId = self.db.saveFolder(folder)
        newFolder = self.db.getFolderById(folderId)
        self.parent().addFolderToTree(newFolder)
        self.close()

    def initFolders(self):
        """Initialize folders."""
        rootFolders = self.db.getRootFolders()

        for root in rootFolders:
            item = QTreeWidgetItem(self.folderSelect)
            item.setText(0, root["name"])
            item.setIcon(0, self.folderIcon)
            item.setText(1, str(root["id"]))
            self.folderSelect.insertTopLevelItem(0, item)
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
                item.setText(1, str(child["id"]))
                parent.addChild(item)
                self.loadChilds(child["id"], item)


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
        self.tree = CharactersTree(self)

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
        dialog = NewCharacterDialog(self)
        dialog.exec()

    def openNewCharacter(self, id):
        """Open newly created character."""
        character = self.db.getCharacterById(id)
        if character["folder"] is None:
            self.tree.addRootCharacter(character)
        else:
            self.tree.addChildCharacter(character)
        self.openCharacter(self.tree.tree.indexFromItem(self.tree.tree.selectedItems()[0]))

    def updateCharacterFolder(self, characterId, folderId):
        """Update character folder."""
        self.tabs.currentWidget().info["folder"] = folderId
        character = self.db.getCharacterById(characterId)

        self.tree.removeCharacterFromList(characterId)

        if character["folder"] is None:
            self.tree.addRootCharacter(character, False)
        else:
            self.tree.addChildCharacter(character, False)

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
            oldCharacter = self.db.getCharacterById(characterWidget.info["id"])
            nameChanged = oldCharacter["name"] != characterWidget.info["name"]
            self.db.updateCharacter(characterWidget.info)

            if nameChanged:
                self.dirMan.moveFolder(oldCharacter["id"],
                                       oldCharacter["name"],
                                       characterWidget.info["name"])
                self.refreshCharacterName(characterWidget.info["id"])

        dialog = QMessageBox.information(self, "Character Saved",
                                         "Character " + characterWidget.info["name"] + " was saved.",
                                         buttons=QMessageBox.Ok,
                                         defaultButton=QMessageBox.Ok)
        dialog.exec()

    def newFolder(self):
        """Open dialog to create a new folder."""
        dialog = NewFolderDialog(self)
        dialog.exec()

    def addFolderToTree(self, folder):
        """Add folder to tree."""
        if folder["parentId"] is None:
            self.tree.addRootFolder(folder)
        else:
            self.tree.addChildFolder(folder)

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

        items = self.tree.tree.findItems(str(characterId),
                                         Qt.MatchExactly | Qt.MatchRecursive, 2)
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

    def refreshCharacterName(self, characterId):
        """Refresh character name."""
        character = self.db.getCharacterById(characterId)

        items = self.tree.tree.findItems(str(characterId),
                                         Qt.MatchExactly | Qt.MatchRecursive, 2)
        characterItem = None
        for item in items:
            type = item.data(1, 0)
            if type == "Character":
                characterItem = item
                break
        if characterItem:
            characterItem.setText(0, character["name"])

        characterTabIndex = self.tabs.indexOf(self.tabs.currentWidget())
        self.tabs.setTabText(characterTabIndex, character["name"])

    def changedDocked(self):
        """Trigger when the docked widget position is changed."""
        location = self.tree.dockLocation()
        self.config = self.dirMan.loadConfig()
        if location == Qt.LeftDockWidgetArea:
            self.config["treeDockedArea"] = "Left"
        else:
            self.config["treeDockedArea"] = "Right"
        self.dirMan.saveConfig(self.config)

    def closeEvent(self, event):
        """Close event."""
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
