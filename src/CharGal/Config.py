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

from platformdirs import PlatformDirs
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from pathlib import Path
import tempfile
import json
import os
import shutil


class DirectoryManager():
    """Configuration and data Manager."""

    def __init__(self):
        """Initialice."""
        if os.geteuid() == 0:
            # Use /usr/local/share instead of /root when running as root
            self.dirs = PlatformDirs("CharGal", appauthor=False,
                                     use_site_for_root=True)
        else:
            self.dirs = PlatformDirs("CharGal", appauthor=False)

    def getFilenameFromPath(self, path):
        """Get the filename from the path."""
        return os.path.basename(path)

    def getNameFromFilename(self, filename):
        """Get the name from the filename."""
        name, _ = os.path.splitext(filename)
        return name

    def getExtensionFromFilename(self, filename):
        """Get the extension from the filename."""
        _, extension = os.path.splitext(filename)
        return extension

    def getConfigPath(self):
        """Get the config dir from the system."""
        return self.dirs.user_config_path

    def getDataPath(self):
        """Get the data dir from the system."""
        return self.dirs.user_data_path

    def getDocumentsDir(self):
        """Get the images path from the system."""
        return self.dirs.user_documents_dir

    def getImagePath(self, name, characterId, characterName):
        """Get the image path for a given image name."""
        dir = self.getDataPath()
        folder = str(characterId) + " - " + characterName
        file = dir / "images" / folder / name
        file.parent.mkdir(parents=True, exist_ok=True)
        return file

    def getFilePath(self, name, characterId, characterName):
        """Get the file path for a given file name."""
        dir = self.getDataPath()
        folder = str(characterId) + " - " + characterName
        file = dir / "documents" / folder / name
        file.parent.mkdir(parents=True, exist_ok=True)
        return file

    def getDBEngine(self):
        """Get a sqlalchemy engine."""
        dir = self.getDataPath()
        file = dir / "data.db"
        file.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine("sqlite:///" + str(file), poolclass=NullPool) # , pool_size=20,
                               # max_overflow=0)
        # print("Connected to database:", engine)
        return engine

    def copyImage(self, sourcePath, characterId, characterName):
        """Copy an image."""
        originalName = self.getFilenameFromPath(sourcePath)
        destPath = self.getImagePath(originalName, characterId, characterName)

        originalName = self.getNameFromFilename(originalName)

        fileExistCounter = 1
        while destPath.exists():
            fileName, fileExtension = os.path.splitext(destPath)
            destPath = self.getImagePath(originalName + str(fileExistCounter) +
                                         fileExtension, characterId,
                                         characterName)
            fileExistCounter += 1
        try:
            shutil.copy2(sourcePath, str(destPath))
        except FileNotFoundError:
            print(f"The file {sourcePath} does not exist.")
            return "error"
        except PermissionError:
            print(f"Permission denied while copying {sourcePath}.")
            return "error"

        return destPath

    def copyFile(self, sourcePath, characterId, characterName):
        """Copy an image."""
        originalName = self.getFilenameFromPath(sourcePath)
        destPath = self.getFilePath(originalName, characterId, characterName)

        originalName = self.getNameFromFilename(originalName)

        fileExistCounter = 1
        while destPath.exists():
            fileName, fileExtension = os.path.splitext(destPath)
            destPath = self.getFilePath(originalName + str(fileExistCounter) +
                                         fileExtension, characterId,
                                         characterName)
            fileExistCounter += 1
        try:
            shutil.copy2(sourcePath, str(destPath))
        except FileNotFoundError:
            print(f"The file {sourcePath} does not exist.")
            return "error"
        except PermissionError:
            print(f"Permission denied while copying {sourcePath}.")
            return "error"

        return destPath

    def deleteImage(self, imageName, characterId, characterName):
        """Delete an image."""
        imagePath = self.getImagePath(imageName, characterId, characterName)
        os.remove(imagePath)

    def deleteFile(self, fileName, characterId, characterName):
        """Delete an image."""
        filePath = self.getFilePath(fileName, characterId, characterName)
        os.remove(filePath)

    def saveConfig(self, config):
        """Save the configuration file."""
        dir = self.getConfigPath()
        file = dir / "config.json"

        configData = json.dumps(config, indent=4)

        try:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(configData)
            print("written config on " + file.as_uri())
        except (OSError, PermissionError) as e:
            tempDir = Path(tempfile.gettempdir()) / "CharGal"
            tempDir.mkdir(parents=True, exist_ok=True)
            file = tempDir / "config.json"
            file.write_text(configData)
            # TODO: Show error message in a dialog
            print(e)

    def loadConfig(self):
        """Load configuration file."""
        config = {}

        for configDir in self.dirs.iter_config_paths():
            file = configDir / "config.json"
            if file.exists():
                config.update(json.loads(file.read_text()))

        return config
