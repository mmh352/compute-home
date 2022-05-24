"""Tornado Session Mixin."""
import json
from tornado.web import RequestHandler
from typing import Iterator

from ..utils import config


class Session(object):
    """The Session object implements a cookie-baked session."""

    def __init__(self: 'Session', handler: RequestHandler) -> 'Session':
        """Initialise the session.

        :param handler: The handler to use for accessing cookies.
        :type handler: RequestHandler
        """
        self._handler = handler
        self._dict = {}
        try:
            cookie = self._handler.get_secure_cookie(config()['server']['session']['name'],
                                                     max_age_days=config()['server']['session']['validity_days'])
            if cookie:
                self._dict = json.loads(cookie)
        except Exception:
            pass

    def update_cookie(self: 'Session') -> None:
        """Update the cookie with the session data."""
        self._handler.set_secure_cookie(config()['server']['session']['name'],
                                        json.dumps(self._dict),
                                        expires_days=config()['server']['session']['validity_days'])

    def __setitem__(self: 'Session', key: str, value: str) -> None:
        """Set a session value.

        :param key: The name of the value to store.
        :type key: str
        :param value: The value to store.
        :type value: str
        """
        self._dict[key] = value
        self.update_cookie()

    def __getitem__(self: 'Session', key: str) -> str:
        """Get a session value.

        :param key: The name of the value to get.
        :type key: str
        :return: The value associated with the name.
        :return_type: str
        """
        return self._dict[key]

    def __contains__(self: 'Session', key: str) -> bool:
        """Check if the session contains the given key.

        :param key: The name of the value to check for.
        :type key: str
        :return: Whether the key exists.
        :return_type: bool
        """
        return key in self._dict

    def __iter__(self: 'Session') -> Iterator:
        """Return an iterator over the session values."""
        return iter(self._dict)

    def __delitem__(self: 'Session', key: str) -> None:
        """Delete the session entry with the given key.

        :param key: The name of the value to delete.
        :type key: str
        """
        del self._dict[key]
        self.update_cookie()

    def get(self: 'Session', key: str, default: str = None) -> str:
        """Get a session value with a default.

        :param key: The name of the value to get.
        :type key: str
        :param default: The default to use if the key does not exist.
        :type default: str or None
        :return: The value or the default value.
        :return_type: str
        """
        if key in self._dict:
            return self._dict[key]
        else:
            return default

    def clear(self: 'Session') -> None:
        """Clear the session."""
        self._dict = {}
        self.update_cookie()


class SessionMixin(object):
    """The SessionMixin provides a dynamically constructed session.

    Can be used with :class:`~tornado.web.RequestHandler` subclasses.
    """

    _session = None

    @property
    def session(self: RequestHandler) -> Session:
        """Return the :class:`~compute_home.server.session.Session`."""
        if self._session is None:
            self._session = Session(self)
        return self._session
