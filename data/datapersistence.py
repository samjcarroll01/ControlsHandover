import abc
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base


class IDataPersistence(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'find') and
                callable(subclass.find) and
                hasattr(subclass, 'all') and
                callable(subclass.all) and
                hasattr(subclass, 'edit') and
                callable(subclass.edit) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete))


class SqlitePersistence(IDataPersistence):
    """
    Handles read/write operations of a sqlite database.

    Constructor requires a path to the database.
    """
    engine = None
    session = None


    def __init__(self, dbpath):
        """
        Creates a database engine and session connecting to the requested
        database.

        :param dbpath: string representation of the path to the database.
        """
        connectionString = "sqlite:///%s" % str(dbpath)
        self.engine = create_engine(connectionString)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save(self, entity):
        """
        Saves an entity to the database.

        :param entity: object to be saved to the database
        :return: True if success; Error message if failure
        """
        try:
            self.session.add(entity)
            self.session.commit()
            return True
        except:
            return "Unexpected Error:'%s'" % sys.exc_info()[0]

    # Pass in the class and the id of element you wish to find.
    def find(self, type, id):
        """
        Find an entity in the database based on its id (integer).

        :param type: the class if the entity you are searching for
        :param id: the id of the entity
        :return: returns the results of the query in the form of an
                 object that of the type requested.
        """
        return self.session.query(type).filter_by(id=id).first()

    def edit(self, type, id, data):
        """

        :param type: the class if the entity you are searching for
        :param id: the id of the entity
        :param data: a dictionary containing the data you wish to
                     change on the existing entity
        :return: returns the updated object.
        """
        element = self.session.query(type).filter_by(id=id).first()
        for key, value in data:
            element.setattr = value

        self.session.commit()
        return element


