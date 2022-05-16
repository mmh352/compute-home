"""The ComputeHome Server application."""
import logging

from tornado.web import Application, RedirectHandler
from tornado.ioloop import IOLoop

from .handlers import (FrontendHandler,)

from ..utils import config


logger = logging.getLogger(__name__)


def run_application_server() -> None:
    """Run the ComputeHome server.

    :param config: The configuration to use
    :type config: dict
    """
    logger.debug('Application server starting up...')
    routes = [
        ('/', RedirectHandler, {'permanent': False, 'url': '/app'}),
        ('/app(.*)', FrontendHandler),
    ]
    app = Application(
        routes,
        debug=config()['debug'],
        xsrf_cookies=True,
        cookie_secret='ohqu6aegezie9uuChidf9shuisahsiegiej4Quo9aiK3Ohhe8aisoimig4Bee9Eb')
    logger.debug(f'Application listening on {config()["server"]["host"]} port {config()["server"]["port"]}')
    app.listen(config()['server']['port'], config()['server']['host'])
    IOLoop.current().start()
