"""The User database model."""
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson

from .meta import Base
from .users_groups import users_groups


class User(Base):
    """Model representing a single user in the database.

    Attributes:
    * id - The unique database id
    * external_id - The external id provided by the LTI authentication
    * attributes - JSON dictionary containing the user's attributes

    Relationships:
    * groups - The groups this user belongs to
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    external_id = Column(Unicode(255))
    attributes = Column(NestedMutableJson)

    groups = relationship('Group', secondary=users_groups, back_populates='users')
