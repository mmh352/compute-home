"""The Group database model."""
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson

from .meta import Base
from .users_groups import users_groups


class Group(Base):
    """Model representing a single group in the database.

    * id - The unique database id
    * external_id - The external id provided by the LTI authentication
    * attributes - JSON dictionary containing the user's attributes
    """

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    external_id = Column(Unicode(255))
    attributes = Column(NestedMutableJson)

    users = relationship('User', secondary=users_groups, back_populates='groups')
