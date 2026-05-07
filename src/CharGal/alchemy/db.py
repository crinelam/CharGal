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

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from Config import DirectoryManager


class DB():
    """DB Manager."""

    def __init__(self):
        """Initialize db."""
        self.dirMan = DirectoryManager()
        self.engine = self.dirMan.getDBEngine()

        # Create missing folders
        Base.metadata.create_all(self.engine)

    def getSession(self):
        """Return a session."""
        return Session(bind=self.engine)

    def getRootFolders(self):
        """Return root folders list."""
        session = self.getSession()

        folders = session.query(Folder).filter_by(parentId=None)
        session.close()
        data = []

        for folder in folders:

            data.append({"type": "Folder", "name": folder.name,
                         "id": folder.id})
        return data

    def getRootCharacters(self):
        """Return characters by folder id."""
        session = self.getSession()

        characters = session.query(Character).filter_by(folder=None)
        session.close()
        data = []

        for character in characters:
            data.append({"type": "Character", "name": character.name,
                         "id": character.id, "image": character.image})
        return data

    def getChildFolders(self):
        """Return folders with parents."""
        session = self.getSession()

        folders = session.query(Folder).filter(Folder.parentId is not None)
        session.close()
        data = []

        for folder in folders:
            data.append({"type": "Folder", "name": folder.name,
                         "id": folder.id, "parentId": folder.parentId})
        return data

    def getFoldersByParentId(self, searchId):
        """Return folders by parent id."""
        session = self.getSession()

        folders = session.query(Folder).filter_by(parentId=searchId)
        session.close()
        data = []

        for folder in folders:
            data.append({"type": "Folder", "name": folder.name,
                         "id": folder.id, "parentId": folder.parentId})
        return data

    def getCharactersByFolderId(self, searchId):
        """Return characters by folder id."""
        session = self.getSession()

        characters = session.query(Character).filter_by(folder=searchId)
        session.close()
        data = []

        for character in characters:
            data.append({"type": "Character", "name": character.name,
                         "id": character.id, "image": character.image})
        return data

    def getCharacterById(self, searchId):
        """Return character by id."""
        session = self.getSession()

        character = session.query(Character).filter_by(id=searchId).first()
        data = {"id": character.id, "image": character.image,
                "name": character.name,
                "description": character.description,
                "pronouns": character.pronouns,
                "orientation": character.orientation,
                "age": character.age, "birthday": character.birthday,
                "height": character.height,
                "weight": character.weight, "eyes": character.eyes,
                "hair": character.hair, "job": character.job,
                "species": character.species,
                "folder": character.folder}
        session.close()
        return data

    def getFolderById(self, searchId):
        """Return folder by id."""
        session = self.getSession()

        folder = session.query(Folder).filter_by(id=searchId).first()
        data = {"id": folder.id,
                "name": folder.name,
                "parentId": folder.parentId}
        session.close()
        return data

    def deleteFolder(self, folderId):
         """Delete folder."""
         session = self.getSession()
         folder = session.query(Folder).filter_by(id=folderId).first()
         if folder:
             session.delete(folder)
             session.commit()
         session.close()

    def getCharacterNameById(self, searchId):
        """Return character name by id."""
        session = self.getSession()

        character = session.query(Character).filter_by(id=searchId).first()
        session.close()

        name = character.name
        return name

    def getImagesByCharacterId(self, searchId):
        """Return images by character id."""
        session = self.getSession()

        images = session.query(CharacterImage).filter_by(character=searchId)
        session.close()
        data = []

        for image in images:
            data.append({"id": image.id, "image": image.image,
                         "characterId": image.character})
        return data

    def saveFolder(self, folder):
        """Save folder to db."""
        session = self.getSession()
        session.add(folder)
        session.commit()
        id = folder.id
        session.close()
        return id

    def saveCharacter(self, character):
        """Save character to db."""
        session = self.getSession()
        session.add(character)
        session.commit()
        id = character.id
        session.close()
        return id

    def updateCharacter(self, characterInfo):
        """Update character to db."""
        session = self.getSession()
        character = session.query(Character).filter_by(
            id=characterInfo["id"]).first()
        if character:
            character.image = characterInfo["image"]
            character.name = characterInfo["name"]
            character.description = characterInfo["description"]
            character.pronouns = characterInfo["pronouns"]
            character.orientation = characterInfo["orientation"]
            character.age = characterInfo["age"]
            character.birthday = characterInfo["birthday"]
            character.height = characterInfo["height"]
            character.weight = characterInfo["weight"]
            character.eyes = characterInfo["eyes"]
            character.hair = characterInfo["hair"]
            character.job = characterInfo["job"]
            character.species = characterInfo["species"]
            character.folder = characterInfo["folder"]
            session.commit()
        session.close()

    def updateCharacterImage(self, characterId, imageName):
        """Update image of character."""
        session = self.getSession()
        character = session.query(Character).filter_by(
            id=characterId).first()
        if character:
            character.image = imageName
            session.commit()
        session.close()

    def updateCharacterFolder(self, characterId, folderId):
        """Update folder of character."""
        session = self.getSession()
        character = session.query(Character).filter_by(
            id=characterId).first()
        if character:
            character.folder = folderId
            session.commit()
        session.close()

    def saveCharacterImage(self, characterImage):
        """Save character image to db."""
        session = self.getSession()
        session.add(characterImage)
        session.commit()
        session.close()

    def deleteCharacterImage(self, imageId):
        """Delete character image."""
        session = self.getSession()
        image = session.query(CharacterImage).filter_by(id=imageId).first()
        if image:
            session.delete(image)
            session.commit()
        session.close()

    def getCharacterFiles(self, characterId):
        """Get character files."""
        session = self.getSession()
        files = session.query(CharacterDocument).filter_by(character=characterId)
        session.close()

        data = []
        for file in files:
            data.append({"id": file.id,
                         "characterId": file.character,
                         "fileName": file.document})
        return data

    def saveCharacterFile(self, characterFile):
        """Save character file to db."""
        session = self.getSession()
        session.add(characterFile)
        session.commit()
        session.close()

    def deleteCharacterFile(self, fileId):
        """Delete character file."""
        session = self.getSession()
        file = session.query(CharacterDocument).filter_by(id=fileId).first()
        if file:
            session.delete(file)
            session.commit()
        session.close()


class Base(DeclarativeBase):
    """Base."""


class Folder(Base):
    """Folder table."""

    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parentId = Column(Integer, ForeignKey("folders.id"))


class Character(Base):
    """Characters table."""

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String)
    name = Column(String)
    description = Column(String)
    pronouns = Column(String)
    orientation = Column(String)
    age = Column(String)
    birthday = Column(String)
    height = Column(String)
    weight = Column(String)
    eyes = Column(String)
    hair = Column(String)
    job = Column(String)
    species = Column(String)
    folder = Column(Integer, ForeignKey("folders.id"))


class Tag(Base):
    """Tags table."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    isCategory = Column(Boolean, nullable=False)
    isDefault = Column(Boolean, nullable=False)


class TagParent(Base):
    """Tag parents table."""

    __tablename__ = "tag_parents"

    tagId = Column(Integer, ForeignKey("tags.id"), primary_key=True,
                   nullable=False)
    characterId = Column(Integer, ForeignKey("characters.id"),
                         primary_key=True, nullable=False)


class CharacterImage(Base):
    """Character images table."""

    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character = Column(Integer, ForeignKey("characters.id"), nullable=False)
    image = Column(String, nullable=False)


class CharacterDocument(Base):
    """Character documents table."""

    __tablename__ = "character_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character = Column(Integer, ForeignKey("characters.id"), nullable=False)
    document = Column(String, nullable=False)
