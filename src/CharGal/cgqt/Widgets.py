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

from PySide6.QtCore import Qt
from PySide6.QtGui import (QColor, QPalette, QIcon, QPixmap, QAction,
                           QImageReader)
from PySide6.QtWidgets import (QWidget, QDockWidget, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QHBoxLayout,
                               QLabel, QFormLayout, QLineEdit, QPushButton,
                               QTextEdit, QCheckBox, QStackedWidget,
                               QScrollArea, QSizePolicy, QMessageBox,
                               QMenu, QFileDialog, QFrame, QDialog,
                               QDialogButtonBox)

import alchemy.db
from alchemy.db import DB
from Config import DirectoryManager

import subprocess
import os
import platform


class ChangeCharacterFolderDialog(QDialog):
    """New character dialog."""

    def __init__(self, parent, characterId):
        """Initialize dialog."""
        super().__init__(parent)

        self.db = DB()

        self.characterId = characterId

        self.setWindowTitle("Change Character Folder")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QFormLayout()

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
        folderItem = self.folderSelect.selectedItems()
        selectedFolder = None
        if folderItem:
            selectedFolder = int(folderItem[0].data(1, 0))
        else:
            selectedFolder = None
        self.db.updateCharacterFolder(self.characterId, selectedFolder)
        self.parent().updateCharacterFolder(self.characterId, selectedFolder)
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

        self.layout.addWidget(CharacterGallery(self.info["id"],
                                               self.info["name"]))


class CharacterInfoHeader(QWidget):
    """Character info header."""

    def __init__(self, info):
        """Initialize widget."""
        super().__init__()

        self.db = DB()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(MainCharacterImage(info["image"], info["id"],
                                                 info["name"]),
                              alignment=Qt.AlignTop)

        self.nameEdit = QLineEdit(info["name"])
        self.nameEdit.textChanged.connect(self.nameEdited)
        self.pronounsEdit = QLineEdit(info["pronouns"])
        self.pronounsEdit.textChanged.connect(self.pronounsEdited)
        self.orientationEdit = QLineEdit(info["orientation"])
        self.orientationEdit.textChanged.connect(self.orientationEdited)

        self.ageEdit = QLineEdit(info["age"])
        self.ageEdit.textChanged.connect(self.ageEdited)
        self.birthdayEdit = QLineEdit(info["birthday"])
        self.birthdayEdit.textChanged.connect(self.birthdayEdited)
        self.eyesEdit = QLineEdit(info["eyes"])
        self.eyesEdit.textChanged.connect(self.eyesEdited)

        self.heightEdit = QLineEdit(info["height"])
        self.heightEdit.textChanged.connect(self.heightEdited)
        self.weightEdit = QLineEdit(info["weight"])
        self.weightEdit.textChanged.connect(self.weightEdited)
        self.hairEdit = QLineEdit(info["hair"])
        self.hairEdit.textChanged.connect(self.hairEdited)

        self.jobEdit = QLineEdit(info["job"])
        self.jobEdit.textChanged.connect(self.jobEdited)
        self.speciesEdit = QLineEdit(info["species"])
        self.speciesEdit.textChanged.connect(self.speciesEdited)

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

        self.panel = QFrame()
        self.panel.setContentsMargins(0, 0, 0, 0)
        self.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.panelLayout = QHBoxLayout()
        self.panelLayout.setContentsMargins(0, 0, 0, 0)
        self.bDeleteChar = QPushButton("Delete")
        self.bDeleteChar.clicked.connect(self.deleteCharacter)
        self.bChangeFolder = QPushButton("Change Folder")
        self.bChangeFolder.clicked.connect(self.changeFolder)

        self.panel.setLayout(self.panelLayout)
        self.panelLayout.addWidget(self.bDeleteChar)
        self.panelLayout.addWidget(self.bChangeFolder)

        self.formLayout2.addRow(self.panel)

        self.layout.addWidget(self.info1)
        self.layout.addWidget(self.info2)

        self.layout.addWidget(CharacterTags(info["id"]))
        self.layout.addWidget(CharacterFiles(info["id"], info["name"]))

        self.setFixedHeight(210)

    def nameEdited(self, text):
        """Name edited event."""
        self.parent().info["name"] = text

    def pronounsEdited(self, text):
        """Pronouns edited event."""
        self.parent().info["pronouns"] = text

    def orientationEdited(self, text):
        """Orientation edited event."""
        self.parent().info["orientation"] = text

    def ageEdited(self, text):
        """Age edited event."""
        self.parent().info["age"] = text

    def birthdayEdited(self, text):
        """Birthday edited event."""
        self.parent().info["birthday"] = text

    def eyesEdited(self, text):
        """Eyes edited event."""
        self.parent().info["eyes"] = text

    def heightEdited(self, text):
        """Height edited event."""
        self.parent().info["height"] = text

    def weightEdited(self, text):
        """Weight edited event."""
        self.parent().info["weight"] = text

    def hairEdited(self, text):
        """Hair edited event."""
        self.parent().info["hair"] = text

    def jobEdited(self, text):
        """Job edited event."""
        self.parent().info["job"] = text

    def speciesEdited(self, text):
        """Species edited event."""
        self.parent().info["species"] = text

    def changeFolder(self):
        """Change folder event."""
        parentWindow = self.parent().parent().parent().parent()
        dialog = ChangeCharacterFolderDialog(parentWindow,
                                             self.parent().info["id"])
        dialog.exec()

    def deleteCharacter(self):
        """Delete character event."""
        self.dirMan = DirectoryManager()

        dialog = QMessageBox.warning(self, "Delete character?",
                                     "Are you sure you want to delete the character?\nWarning: This will delete all data from the character and can't be undone.",
                                     buttons=QMessageBox.Yes | QMessageBox.Cancel,
                                     defaultButton=QMessageBox.Cancel)
        if dialog == QMessageBox.Yes:
            characterId = self.parent().info["id"]
            characterName = self.parent().info["name"]
            self.parent().parent().parent().parent().tree.removeCharacterFromList(characterId)
            currentTabWidget = self.parent().parent().parent().parent().tabs.currentWidget()
            characterTabIndex = self.parent().parent().parent().parent().tabs.indexOf(currentTabWidget)
            self.parent().parent().parent().parent().tabs.removeTab(characterTabIndex)

            images = self.db.getImagesByCharacterId(characterId)
            for image in images:
                self.dirMan.deleteImage(image["image"],
                                        characterId, characterName)
                self.db.deleteCharacterImage(image["id"])
            self.dirMan.deleteImage(self.parent().info["image"],
                                    characterId, characterName)

            files = self.db.getCharacterFiles(characterId)
            for file in files:
                self.dirMan.deleteFile(file["fileName"],
                                       characterId, characterName)
                self.db.deleteCharacterFile(file["id"])

            self.dirMan.deleteFolders(characterId, characterName)
            self.db.deleteCharacter(characterId)


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

    def __init__(self, characterId, characterName):
        """Initialize widget."""
        super().__init__()

        self.characterId = characterId
        self.characterName = characterName

        self.icons = {"image": QIcon("assets/icons/blue-document-image.png"),
                      "word": QIcon("assets/icons/blue-document-word.png"),
                      "excel": QIcon("assets/icons/blue-document-excel.table.png"),
                      "audio": QIcon("assets/icons/blue-document-music.png"),
                      "powerpoint": QIcon("assets/icons/blue-document-powerpoint.png"),
                      "pdf": QIcon("assets/icons/blue-document-pdf-text.png"),
                      "video": QIcon("assets/icons/blue-document-film.png"),
                      "text": QIcon("assets/icons/blue-document-text.png"),
                      "compress": QIcon("assets/icons/blue-document-zipper.png"),
                      "other": QIcon("assets/icons/blue-document.png")}

        self.audioExtensions = [".wav", ".mp3", ".ogg", ".flac", "-opus"]
        self.videoExtensions = [".mkv", ".webm", ".mp4", ".avi", ".mov"]
        self.imageExtensions = [".png", ".webp", ".jpg"]
        self.textExtensions = [".txt", ".xml", ".html", ".css", ".md", ".json"]

        self.wordExtensions = [".doc", ".docx", ".odt", ".ott", ".rtf"]
        self.excelExtensions = [".ods", ".xls", ".xlsx", ".xltx", ".ots",
                                ".xlsb"]
        self.powerpointExtensions = [".ppt", ".pptx", ".ppsx", ".odp", ".potx",
                                     ".otp"]
        self.compressExtensions = [".zip", ".rar", ".7z", ".gz", ".lz",
                                   ".br"]

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.panel = QWidget()
        self.panelLayout = QHBoxLayout()
        self.panel.setLayout(self.panelLayout)

        self.bAddFile = QPushButton("Add file")
        self.bAddFile.clicked.connect(self.addFile)
        self.panelLayout.addWidget(self.bAddFile)

        self.bOpenFile = QPushButton("Open")
        self.bOpenFile.clicked.connect(self.openFile)
        self.panelLayout.addWidget(self.bOpenFile)
        self.bOpenFile.setEnabled(False)

        self.bDeleteFile = QPushButton("Delete")
        self.bDeleteFile.clicked.connect(self.deleteFile)
        self.panelLayout.addWidget(self.bDeleteFile)
        self.bDeleteFile.setEnabled(False)

        self.layout.addWidget(self.panel)

        self.filesWidget = QTreeWidget()
        self.filesWidget.setHeaderLabels(["Name", "ID"])
        self.filesWidget.setColumnCount(2)
        self.filesWidget.setColumnHidden(1, True)
        self.filesWidget.setSortingEnabled(True)

        self.filesWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.filesWidget.itemDoubleClicked.connect(self.openFile)

        self.layout.addWidget(self.filesWidget)
        self.setFixedWidth(400)
        self.setFixedHeight(200)

        self.db = DB()

        self.files = []
        self.refreshFiles()

    def selectionChanged(self):
        """Check selection changed."""
        selected = self.filesWidget.selectedItems()
        if selected:
            self.bDeleteFile.setEnabled(True)
            self.bOpenFile.setEnabled(True)
        else:
            self.bDeleteFile.setEnabled(False)
            self.bOpenFile.setEnabled(False)

    def openFile(self):
        """Open file."""
        self.dirMan = DirectoryManager()
        selectedFile = self.filesWidget.selectedItems()[0].data(0, 0)
        filepath = self.dirMan.getFilePath(selectedFile, self.characterId,
                                           self.characterName)

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else: # linux
            subprocess.call(('xdg-open', filepath))

    def deleteFile(self):
        """Delete file."""
        selectedItem = self.filesWidget.selectedItems()[0]
        selectedFile =selectedItem.data(0, 0)
        dialog = QMessageBox.warning(self, "Delete file?",
                                     "Are you sure you want to delete the file '" + selectedFile + "'?",
                                     buttons=QMessageBox.Yes | QMessageBox.No,
                                     defaultButton=QMessageBox.No)
        if dialog == QMessageBox.Yes:
            print("deleting")
            self.db.deleteCharacterFile(selectedItem.data(1, 0))
            print(selectedItem.data(1, 0))
            self.dirMan.deleteFile(selectedFile, self.characterId,
                                   self.characterName)
            self.refreshFiles()

    def addFile(self):
        """Add file."""
        self.dirMan = DirectoryManager()

        dialog = QFileDialog()
        # dialog.setNameFilter("Images ( *.png *.jpg)")
        dialog.setDirectory(self.dirMan.getDocumentsDir())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if dialog.exec():
            fileNames = dialog.selectedFiles()
            for fileNam in fileNames:
                newFilePath = self.dirMan.copyFile(fileNam, self.characterId,
                                                   self.characterName)
                if newFilePath != "error":
                    fileName = self.dirMan.getFilenameFromPath(newFilePath)
                    file = alchemy.db.CharacterDocument(character=self.characterId,
                                                        document=fileName)
                    self.db.saveCharacterFile(file)
            self.refreshFiles()

    def refreshFiles(self):
        """Refresh files."""
        while self.filesWidget.takeTopLevelItem(0) is not None:
            pass

        self.dirMan = DirectoryManager()
        self.files = self.db.getCharacterFiles(self.characterId)

        for file in self.files:
            fileExtension = self.dirMan.getExtensionFromFilename(file["fileName"])
            item = QTreeWidgetItem(self.filesWidget)
            item.setText(0, file["fileName"])
            if fileExtension == ".pdf":
                item.setIcon(0, self.icons["pdf"])
            elif fileExtension in self.audioExtensions:
                item.setIcon(0, self.icons["audio"])
            elif fileExtension in self.videoExtensions:
                item.setIcon(0, self.icons["video"])
            elif fileExtension in self.imageExtensions:
                item.setIcon(0, self.icons["image"])
            elif fileExtension in self.textExtensions:
                item.setIcon(0, self.icons["text"])
            elif fileExtension in self.wordExtensions:
                item.setIcon(0, self.icons["word"])
            elif fileExtension in self.excelExtensions:
                item.setIcon(0, self.icons["excel"])
            elif fileExtension in self.powerpointExtensions:
                item.setIcon(0, self.icons["powerpoint"])
            elif fileExtension in self.compressExtensions:
                item.setIcon(0, self.icons["compress"])
            else:
                item.setIcon(0, self.icons["other"])
            item.setText(1, str(file["id"]))
            self.filesWidget.insertTopLevelItem(0, item)


class CharacterImage(QLabel):
    """Character image."""

    def __init__(self, imageInfo, characterId, characterName):
        """Initialize widget."""
        super().__init__()

        self.imageInfo = imageInfo
        self.imageName = self.imageInfo["image"]

        QImageReader.setAllocationLimit(0)

        self.characterId = characterId
        self.characterName = characterName

        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        self.defaultImage = QPixmap("assets/images/blankCharacter.png").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        self.dirMan = DirectoryManager()

        if self.imageName is not None:
            imagePath = self.dirMan.getImagePath(self.imageName,
                                                 self.characterId,
                                                 self.characterName)
            self.image = QPixmap(str(imagePath)).scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.image = self.defaultImage

        self.setPixmap(self.image)

        self.db = DB()

        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    def contextMenuEvent(self, event):
        """Context menu event."""
        menu = QMenu(self)

        aEdit = QAction("Delete image", self)
        aEdit.triggered.connect(self.deleteImage)
        menu.addAction(aEdit)

        menu.exec(event.globalPos())

        event.accept()

    def mouseDoubleClickEvent(self, event):
        """Mouse double click event."""
        self.openImage()

    def openImage(self):
        """Open image."""
        self.dirMan = DirectoryManager()
        imagepath = self.dirMan.getImagePath(self.imageName, self.characterId,
                                             self.characterName)

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', imagepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(imagepath)
        else:  # linux
            subprocess.call(('xdg-open', imagepath))

    def deleteImage(self, event):
        """Delete Image Trigger."""
        dialog = QMessageBox.warning(self, "Delete file?",
                                     "Are you sure you want to delete the image '" + self.imageName + "'?",
                                     buttons=QMessageBox.Yes | QMessageBox.No,
                                     defaultButton=QMessageBox.No)
        if dialog == QMessageBox.Yes:
            self.db.deleteCharacterImage(self.imageInfo["id"])
            self.dirMan.deleteImage(self.imageName, self.characterId, self.characterName)
            self.destroy()
            self.parent().parent().parent().parent().refreshImageGallery(self.imageInfo["characterId"])


class MainCharacterImage(QLabel):
    """Character image."""

    def __init__(self, imageName, characterId, characterName):
        """Initialize widget."""
        super().__init__()

        self.imageName = imageName
        self.characterId = characterId
        self.characterName = characterName

        QImageReader.setAllocationLimit(0)

        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        self.defaultImage = QPixmap("assets/images/blankCharacter.png").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        self.dirMan = DirectoryManager()

        if self.imageName is not None:
            imagePath = self.dirMan.getImagePath(self.imageName,
                                                 self.characterId,
                                                 self.characterName)
            self.image = QPixmap(str(imagePath)).scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.image = self.defaultImage

        self.setPixmap(self.image)

        self.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.db = DB()

    def mouseDoubleClickEvent(self, event):
        """Mouse double click event."""
        self.openImage()

    def openImage(self):
        """Open image."""
        self.dirMan = DirectoryManager()
        imagepath = self.dirMan.getImagePath(self.imageName, self.characterId,
                                             self.characterName)

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', imagepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(imagepath)
        else:  # linux
            subprocess.call(('xdg-open', imagepath))

    def contextMenuEvent(self, event):
        """Context menu event."""
        menu = QMenu(self)

        aEdit = QAction("Change image", self)
        aEdit.triggered.connect(self.editImage)
        menu.addAction(aEdit)

        menu.exec(event.globalPos())

        event.accept()

    def editImage(self):
        """Edit image."""
        currentImage = self.imageName
        self.dirMan = DirectoryManager()

        dialog = QFileDialog()
        dialog.setNameFilter("Images ( *.png *.jpg *.jpeg *.webp *.gif)")
        dialog.setDirectory(self.dirMan.getLastFileDialogDir())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if dialog.exec():
            fileNames = dialog.selectedFiles()
            self.dirMan.saveLastFileDialogDir(self.dirMan.getFolderFromPath(fileNames[0]))
            newImagePath = self.dirMan.copyImage(fileNames[0], self.characterId, self.characterName)
            if newImagePath != "error":
                self.image = QPixmap(str(newImagePath)).scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.setPixmap(self.image)

                newImageName = os.path.basename(newImagePath)
                self.parent().parent().info["image"] = newImageName

                if currentImage is not None:
                    self.dirMan.deleteImage(currentImage, self.characterId, self.characterName)

                self.imageName = newImageName

                self.db.updateCharacterImage(self.parent().parent().info["id"],
                                           newImageName)
                self.parent().parent().parent().parent().parent().refreshCharacterImage(self.parent().parent().info["id"])


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
        self.markdownEditor.textChanged.connect(self.descriptionEdited)

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

    def descriptionEdited(self):
        """Edit description event."""
        self.parent().info["description"] = self.markdownEditor.toPlainText()


class CharacterGallery(QWidget):
    """Character gallery widget."""

    def __init__(self, characterId, characterName):
        """Initialize widget."""
        super().__init__()

        self.characterId = characterId
        self.characterName = characterName

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bAddImage = QPushButton("Add image")
        self.bAddImage.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.bAddImage.clicked.connect(self.addImage)

        self.layout.addWidget(self.bAddImage)

        self.scrollArea = QScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Minimum)
        self.scrollArea.setFixedHeight(230)
        self.imageGallery = ImageGallery(self.characterId, self.characterName)
        self.scrollArea.setWidget(self.imageGallery)
        self.layout.addWidget(self.scrollArea)

        self.db = DB()

    def refreshImageGallery(self, characterId):
        """Refresh images."""
        self.imageGallery.destroy()
        self.imageGallery = ImageGallery(self.characterId, self.characterName)
        self.scrollArea.setWidget(self.imageGallery)

    def addImage(self):
        """Add image."""
        self.dirMan = DirectoryManager()
        dialog = QFileDialog()
        dialog.setNameFilter("Images ( *.png *.jpg *.jpeg *.webp *.gif )")
        dialog.setDirectory(self.dirMan.getLastFileDialogDir())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if dialog.exec():
            fileNames = dialog.selectedFiles()
            self.dirMan.saveLastFileDialogDir(self.dirMan.getFolderFromPath(fileNames[0]))
            for fileName in fileNames:
                imagePath = self.dirMan.copyImage(fileName, self.characterId,
                                                  self.characterName)
                if imagePath != "error":
                    imageName = os.path.basename(imagePath)
                    characterImage = alchemy.db.CharacterImage(image=imageName,
                                                               character=int(self.characterId))
                    self.db.saveCharacterImage(characterImage)
                    self.refreshImageGallery(self.characterId)


class ImageGallery(QWidget):
    """Images gallery widget."""

    def __init__(self, characterId, characterName):
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
            imageWidget = CharacterImage(image, characterId, characterName)
            imageWidget.setContentsMargins(5, 5, 5, 5)
            self.layout.addWidget(imageWidget)


class CharactersTree(QDockWidget):
    """Tree widget for character organization."""

    def __init__(self, parent):
        """Initialize Widget."""
        super().__init__(parent)

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

        self.loadData()
        self.setWidget(self.tree)

        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.createContextMenu)
        self.lastContextMenuItem = None

    def createContextMenu(self, pos):
        """Create context menu."""
        self.lastContextMenuItem = self.tree.itemAt(pos)
        itemType = self.lastContextMenuItem.data(1, 0)
        if itemType == "Folder":
            menu = QMenu(self)
            aDeleteFolder = QAction("Delete Folder", self)
            aDeleteFolder.triggered.connect(self.deleteFolder)
            menu.addAction(aDeleteFolder)
            menu.exec(self.tree.mapToGlobal(pos))

    def deleteFolder(self):
        """Delete folder."""
        dialog = QMessageBox.warning(self, "Delete folder?",
                                     "Are you sure you want to delete the folder?\nWarning: This will delete all subfolders.\nCharacters will be moved to the root folder and all open characters will be saved afterwards.",
                                     buttons=QMessageBox.Yes | QMessageBox.Cancel,
                                     defaultButton=QMessageBox.Cancel)
        if dialog == QMessageBox.Yes:
            parentId = self.lastContextMenuItem.data(2, 0)
            folders = self.db.getFoldersByParentId(parentId)
            for folder in folders:
                characters = self.db.getCharactersByFolderId(folder["id"])
                for character in characters:
                    self.db.updateCharacterFolder(character["id"], None)
                    self.removeCharacterFromList(character["id"])
                    character["folder"] = None
                    self.addRootCharacter(character, False)

            characters = self.db.getCharactersByFolderId(parentId)
            for character in characters:
                self.db.updateCharacterFolder(character["id"], None)
                self.removeCharacterFromList(character["id"])
                character["folder"] = None
                self.addRootCharacter(character, False)

            for folder in folders:
                self.db.deleteFolder(folder["id"])
                self.removeFolderFromList(folder["id"])
            self.db.deleteFolder(parentId)
            self.removeFolderFromList(parentId)

            tabCount = self.parent().tabs.count()
            for i in range(tabCount):
                self.parent().tabs.setCurrentIndex(i)
                self.parent().saveCharacter()

    def loadData(self):
        """Load data."""
        rootFolders = self.db.getRootFolders()
        rootCharacters = self.db.getRootCharacters()

        for character in rootCharacters:
            self.addRootCharacter(character)

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
        if not characters:
            return
        else:
            for character in characters:
                item = QTreeWidgetItem(parent)
                item.setText(0, character["name"])
                if character["image"] is not None:
                    path = self.dirMan.getImagePath(character["image"],
                                                    character["id"],
                                                    character["name"])
                    item.setIcon(0, QIcon(str(path)))
                else:
                    item.setIcon(0, self.characterIcon)
                item.setText(1, character["type"])
                item.setText(2, str(character["id"]))
                parent.addChild(item)

    def addRootCharacter(self, character, select=True):
        """Add root character."""
        item = QTreeWidgetItem(self.tree)
        item.setText(0, character["name"])
        if character["image"] is not None:
            path = self.dirMan.getImagePath(character["image"],
                                            character["id"],
                                            character["name"])
            item.setIcon(0, QIcon(str(path)))
        else:
            item.setIcon(0, self.characterIcon)
        item.setText(1, "Character")
        item.setText(2, str(character["id"]))
        self.tree.insertTopLevelItem(0, item)
        if select:
            self.tree.setCurrentItem(item)

    def addChildCharacter(self, character, select=True):
        """Add child character."""
        parentFolder = None
        folders = self.tree.findItems(str(character["folder"]),
                                      Qt.MatchFlag.MatchExactly | Qt.MatchRecursive, 2)
        for folder in folders:
            if folder.data(1, 0) == "Folder":
                parentFolder = folder

        item = QTreeWidgetItem(parentFolder)
        item.setText(0, character["name"])
        if character["image"] is not None:
            path = self.dirMan.getImagePath(character["image"],
                                            character["id"],
                                            character["name"])
            item.setIcon(0, QIcon(str(path)))
        else:
            item.setIcon(0, self.characterIcon)
        item.setText(1, "Character")
        item.setText(2, str(character["id"]))
        parentFolder.addChild(item)
        if select:
            self.tree.setCurrentItem(item)

    def addRootFolder(self, folder):
        """Add root folder."""
        item = QTreeWidgetItem(self.tree)
        item.setText(0, folder["name"])
        item.setIcon(0, self.folderIcon)
        item.setText(1, "Folder")
        item.setText(2, str(folder["id"]))
        self.tree.insertTopLevelItem(0, item)

    def addChildFolder(self, folder):
        """Add child folder."""
        parentFolder = None
        folders = self.tree.findItems(str(folder["parentId"]),
                                      Qt.MatchFlag.MatchExactly | Qt.MatchRecursive, 2)
        for f in folders:
            if f.data(1, 0) == "Folder":
                parentFolder = f

        item = QTreeWidgetItem(parentFolder)
        item.setText(0, folder["name"])
        item.setIcon(0, self.folderIcon)
        item.setText(1, "Folder")
        item.setText(2, str(folder["id"]))
        self.tree.insertTopLevelItem(0, item)

    def removeCharacterFromList(self, characterId):
        """Remove a character fom the list."""
        characters = self.tree.findItems(str(characterId),
                                         Qt.MatchFlag.MatchExactly | Qt.MatchRecursive, 2)
        for character in characters:
            if character.data(1, 0) == "Character":
                # TODO: Figure out a way to delete this instead.
                character.setHidden(True)

    def removeFolderFromList(self, folderId):
        """Remove a character fom the list."""
        folders = self.tree.findItems(str(folderId),
                                         Qt.MatchFlag.MatchExactly | Qt.MatchRecursive, 2)
        for folder in folders:
            if folder.data(1, 0) == "Folder":
                # TODO: Figure out a way to delete this instead.
                folder.setHidden(True)
