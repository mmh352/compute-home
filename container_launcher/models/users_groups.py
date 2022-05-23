"""Link table from :class:`~compute_home.models.user.User` to :class:`~compute_home.models.group.Group`."""
from sqlalchemy import Table, Column, ForeignKey

from .meta import Base

users_groups = Table(
    'users_groups',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True))
