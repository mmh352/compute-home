"""The User database model."""
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class User(Base):
    """Model representing a single user in the database.

    * id - The unique database id
    * external_id - The external id provided by the LTI authentication
    * attributes - JSON dictionary containing the user's attributes
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    external_id = Column(Unicode(255))
    attributes = Column(NestedMutableJson)
