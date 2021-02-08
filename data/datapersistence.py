import sys
import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.item import Item


class SqlitePersistence:
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
            # Add timestamps and user information
            entity.created_at = datetime.datetime.now()
            entity.updated_at = entity.created_at
            entity.created_by = os.getlogin()
            entity.updated_by = entity.created_by

            # add entity to the session and save it to the database.
            self.session.add(entity)
            self.session.commit()
            return True
        except:
            return "Unexpected Error:'%s'" % sys.exc_info()[0]

    def find(self, entitytype, id):
        """
        Find an entity in the database based on its id (integer).

        :param entitytype: the class if the entity you are searching for
        :param id: the id of the entity
        :return: returns the results of the query in the form of an
                 object that of the type requested.
        """
        return self.session.query(entitytype).filter_by(id=id).first()

    def get_incomplete_items(self):
        """
        :return: return list of items that are incomplete
        """
        return self.session.query(Item).filter(Item.completed_at.is_(None))

    def edit(self, entitytype, id, data):
        """

        :param entitytype: the class if the entity you are searching for
        :param id: the id of the entity
        :param data: a dictionary containing the data you wish to
                     change on the existing entity
        :return: returns the updated object.
        """

        try:
            # Get the entity that needs to be updated.
            element = self.session.query(entitytype).filter_by(id=id).first()

            # Go through the dictionary of data to be changed and set the values on
            # that entity to the values in the dictionary
            for key in data.keys():
                print(key)
                setattr(element, key, data[key])

            # Update the timestamp and user info for updated_at and updated_by
            element.updated_at = datetime.datetime.now()
            element.updated_by = os.getlogin()

            # Save the updated information to the database
            self.session.commit()
            return element
        except:
            return "Unexpected Error:'%s'" % sys.exc_info()[0]

    def complete(self, entitytype, id):
        """
        Marks an entity as complete by adding a timestamp for completed_at

        :param entitytype: the class if the entity you are searching for
        :param id: the id of the entity
        :return: returns the completed entity
        """
        try:
            element = self.find(entitytype, id)

            # Set the completed_at, updated_at, and updated_by fields
            element.completed_at = datetime.datetime.now()
            element.updated_at = element.completed_at
            element.updated_by = os.getlogin()

            # Save the element to the database
            self.session.commit()
            return element
        except:
            return "Unexpected Error:'%s'" % sys.exc_info()[0]

    def incomplete(self, entitytype, id):
        """
        Marks an entity as complete by adding a timestamp for completed_at

        :param entitytype: the class if the entity you are searching for
        :param id: the id of the entity
        :return: returns the completed entity
        """
        try:
            element = self.find(entitytype, id)

            # Set the completed_at to None, Set the updated_at, and updated_by fields
            element.completed_at = None
            element.updated_at = datetime.datetime.now()
            element.updated_by = os.getlogin()

            # Save the element to the database
            self.session.commit()
            return element
        except:
            return "Unexpected Error:'%s'" % sys.exc_info()[0]
