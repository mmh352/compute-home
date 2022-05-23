"""The ComputeHome Server application."""
import logging

from tornado.web import Application, RedirectHandler
from tornado.ioloop import IOLoop

from .handlers import (FrontendHandler, LtiLoginStartHandler, LtiLaunchHandler, ApiHandler)

from ..utils import config


logger = logging.getLogger(__name__)


def run_application_server() -> None:
    """Run the ComputeHome server."""
    logger.debug('Application server starting up...')
    routes = [
        ('/', RedirectHandler, {'permanent': False, 'url': '/app'}),
        ('/app(.*)', FrontendHandler),
        ('/api', ApiHandler),
        ('/lti', LtiLaunchHandler),
        ('/lti/login', LtiLoginStartHandler),
    ]
    app = Application(
        routes,
        debug=config()['debug'],
        xsrf_cookies=True,
        cookie_secret=config()['server']['cookie_secret'])
    logger.debug(f'Application listening on {config()["server"]["host"]} port {config()["server"]["port"]}')
    app.listen(config()['server']['port'], config()['server']['host'])
    IOLoop.current().start()
