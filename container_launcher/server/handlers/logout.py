"""Handler for the logging out."""
import logging

from tornado.web import RequestHandler

from ..session import SessionMixin
from ...utils import config


logger = logging.getLogger(__name__)


class LogoutHandler(RequestHandler, SessionMixin):
    """Handle logout requests, ensuring all containers are shut down."""

    def get(self: 'LogoutHandler') -> None:
        """Perform the logout and shut down all user containers."""
        if 'user_id' in self.session:
            del self.session['user_id']
        if config()['app']['vle']['url']:
            self.redirect(config()['app']['vle']['url'])
        else:
            self.redirect('/app')
