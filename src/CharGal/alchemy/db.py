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
        """Return a session"""
        return Session(bind=self.engine)

    def getFolders(self):
        """Return folder list."""
        #data = {"Folder A": ["Character 1", "Character 2", "Character 3"],
        #        "Folder B": ["Character 1", "Character 2"],
        #        "Folder C": []}
        data = {}
        
        session = self.getSession()
        
        folders = session.query(Folder).all()
        folderParents = session.query(FolderParents).all()
        
        for folder in folders:
            #if folder.id in folderParents.child_id:
            #    print(folder)
            print(folder.name)
            folderParents = session.query(FolderParents).filter_by(childId=folder.id).all()
            childs = []
            for child in folderParents:
                childs.append(child.name)
            data[folder.name] = childs
        return data

    def saveFolder(self, folder):
        session = self.getSession()
        session.add(folder)
        session.commit()

        
class Base(DeclarativeBase):
    """Base."""
    
    
class Folder(Base):
    """Folder table."""
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class FolderParents(Base):
    """Folder Parents table."""
    __tablename__ = "folder_parents"

    parentId = Column(Integer, ForeignKey("folders.id"), primary_key=True, nullable=False)
    childId = Column(Integer, ForeignKey("folders.id"), primary_key=True, nullable=False)


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

    tagId = Column(Integer, ForeignKey("tags.id"), primary_key=True, nullable=False)
    characterId = Column(Integer, ForeignKey("characters.id"), primary_key=True, nullable=False)

    
class CharacterImage(Base):
    """Character images table-"""
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character = Column(Integer, ForeignKey("characters.id"), nullable=False)
    image = Column(String, nullable=False)

class CharacterDocument(Base):
    """Character documents table-"""
    __tablename__ = "character_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character = Column(Integer, ForeignKey("characters.id"), nullable=False)
    document = Column(String, nullable=False)
