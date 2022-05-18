"""Handler for the LTI login."""
import logging

from pylti1p3.cookie import CookieService as LTICookieService
from pylti1p3.message_launch import MessageLaunch as LTIMessageLaunch
from pylti1p3.oidc_login import OIDCLogin as LTILogin
from pylti1p3.request import Request as LTIRequest
from pylti1p3.session import SessionService as LTISessionService
from pylti1p3.tool_config import ToolConfDict
from sqlalchemy.future import select
from tornado.web import RequestHandler, HTTPError

from ..session import SessionMixin, Session
from ...models import get_sessionmaker, User
from ...utils import config

logger = logging.getLogger(__name__)


def generate_config() -> dict:
    """Generate the configuration dictionary for the configured LTI platforms.

    :return: The configuration dictionary for the LTI library.
    :rtype: dict
    """
    return dict([(entry['iss'], entry) for entry in config()['lti']])


class TornadoLTIRequest(LTIRequest):
    """Request wrapper for the LTI authentication processes."""

    def __init__(self: 'TornadoLTIRequest', handler: RequestHandler) -> None:
        """Create a new :class:`~compute_home.server.handlers.lti.TornadoLTIRequest`.

        :param handler: The request handler for parameter and session access.
        :type handler: :class:`~tornado.web.RequestHandler`
        """
        self._handler = handler

    def get_param(self: 'TornadoLTIRequest', key: str) -> str:
        """Get the request parameter for the ``key``.

        :param key: The key of the request parameter
        :type key: str
        :return: The value for the request parameter
        :rtype: str
        """
        return self._handler.get_argument(key)

    def is_secure(self: 'TornadoLTIRequest') -> bool:
        """Determine whether the request is secure.

        Currently defaults to ``True``.
        """
        return True

    @property
    def session(self: 'TornadoLTIRequest') -> Session:
        """Get the session for the request.

        :return: The current session.
        :rtype: :class:`~compute_home_server.session.Session`
        """
        return self._handler.session


class TornadoLTICookieService(LTICookieService):
    """Cookie wrapper for the LTI authentication process."""

    def __init__(self: 'TornadoLTICookieService', handler: RequestHandler) -> None:
        """Create a new :class:`~compute_home.server.handlers.lti.TornadoLTICookieService`.

        :param handler: The handler to use for setting / getting cookies.
        :type handler: :class:`~tornado.web.RequestHandler`
        """
        super().__init__()
        self._handler = handler

    def set_cookie(self: 'TornadoLTICookieService', name: str, value: str, expires: int) -> None:
        """Set a cookie value.

        :param name: The name of the cookie to set.
        :type name: str
        :param value: The value of the cookie to set.
        :type value: str
        :param expires: The number of seconds until the cookie expires.
        :type expires: int
        """
        self._handler.set_secure_cookie(name, value.encode('utf-8'), max_age=expires)

    def get_cookie(self: 'TornadoLTICookieService', name: str) -> str:
        """Get a cookie value.

        :param name: The name of the cookie to get.
        :type name: str
        :return: The value of the cookie
        :rtype: str
        """
        return self._handler.get_secure_cookie(name).decode('utf-8')


class TornadoLTIRedirect(object):
    """Redirection object required for the LTI authentication process."""

    def __init__(self: 'TornadoLTIRedirect', handler: RequestHandler, url: str) -> None:
        """Create a new :class:`~compute_home.server.handlers.lti.TornadoLTIRedirect`.

        :param handler: The handler to use for sending the redirect.
        :type handler: :class:`~tornado.web.RequestHandler`
        :param url: The to redirect to.
        :type url: str
        """
        self._handler = handler
        self._url = url

    def do_redirect(self: 'TornadoLTIRedirect') -> None:
        """Perform the actual redirect."""
        self._handler.redirect(self._url)


class TornadoLTILogin(LTILogin):
    """LTI authentication process step 2: authentication."""

    def __init__(self: 'TornadoLTILogin', request: TornadoLTIRequest, tool_config: ToolConfDict, cookie_service: TornadoLTICookieService) -> None:  # noqa: E501
        """Create a new :class:`~compute_home.server.handlers.lti.TornadoLTILogin`.

        :param request: The request containing the login initiation data.
        :type request: :class:`~compute_home.server.handlers.lti.TornadoLTIRequest`
        :param tool_config: The LTI tool configuration.
        :type tool_config: :class:`~pylti1p3.tool_config.ToolConfigDict`
        :param cookie_service: The cookie wrapper.
        :type cookie_service: :class:`~compute_home.server.handlers.lti.TornadoLTICookieService`
        """
        super().__init__(request, tool_config, LTISessionService(request), cookie_service)

    def get_redirect(self: 'TornadoLTILogin', url: str) -> TornadoLTIRedirect:
        """Get the authentication redirect.

        :param url: The URL to redirect to.
        :type url: str
        :return: The redirection proxy.
        :rtype: :class:`~compute_home.server.handlers.lti.TornadoLTIRedirect`
        """
        return TornadoLTIRedirect(self._request._handler, url)


class TornadoLTIMessageLaunch(LTIMessageLaunch):
    """LTI authentication process step 2: launch."""

    def __init__(self: 'TornadoLTIMessageLaunch', request: TornadoLTIRequest, tool_config: ToolConfDict, cookie_service: TornadoLTICookieService) -> None:  # noqa: E501
        """Create a new :class:`~compute_home.server.handlers.lti.TornadoLTIMessageLaunch`.

        :param request: The request containing the launch data.
        :type request: :class:`~compute_home.server.handlers.lti.TornadoLTIRequest`
        :param tool_config: The LTI tool configuration.
        :type tool_config: :class:`~pylti1p3.tool_config.ToolConfigDict`
        :param cookie_service: The cookie wrapper.
        :type cookie_service: :class:`~compute_home.server.handlers.lti.TornadoLTICookieService`
        """
        super().__init__(request, tool_config, LTISessionService(request), cookie_service)

    def _get_request_param(self: 'TornadoLTIMessageLaunch', key: str) -> str:
        """Get a request parameter value.

        :param key: The key of the request parameter to fetch.
        :type key: str
        :return: The request parameter value.
        :rtype: str
        """
        return self._request.get_param(key)


class LtiLoginStartHandler(RequestHandler, SessionMixin):
    """Request handler for handling the initial login process start request."""

    def post(self: 'LtiLoginStartHandler') -> None:
        """Handle the POST request that starts the login process."""
        logger.debug('Starting the LTI login process')
        self.session.clear()
        oidc_request = TornadoLTIRequest(self)
        oidc_login = TornadoLTILogin(
            request=oidc_request,
            tool_config=ToolConfDict(generate_config()),
            cookie_service=TornadoLTICookieService(self),
        )
        oidc_login.pass_params_to_launch({'xsrf': self.xsrf_token.decode('utf-8')})
        self.session['xsrf'] = self.xsrf_token.decode('utf-8')
        logger.debug('Redirecting to the LTI platform')
        return oidc_login.redirect(self.get_argument('target_link_uri'))

    def check_xsrf_cookie(self: 'LtiLoginStartHandler') -> None:
        """No XSRF check needed, as this will always come from external."""
        pass


class LtiLaunchHandler(RequestHandler, SessionMixin):
    """Request handler for handling the launch request after authentication is successful."""

    async def post(self: 'LtiLaunchHandler') -> None:
        """Handle the POST request that completes the login proces."""
        logger.debug('Starting the LTI launch process')
        tool_config = ToolConfDict(generate_config())
        oidc_request = TornadoLTIRequest(self)
        message_launch = TornadoLTIMessageLaunch(
            request=oidc_request,
            tool_config=tool_config,
            cookie_service=TornadoLTICookieService(self),
        )
        logger.debug('LTI launch validated - logging in')
        message_launch.get_launch_data()
        data = message_launch.get_launch_data()
        logger.debug(data)
        logger.debug('Logging in user')
        async with get_sessionmaker()() as session:
            stmt = select(User).filter(User.external_id == str(data['sub']))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user is None:
                logger.debug('Creating a new user')
                user = User(external_id=str(data['sub']), attributes={})
                session.add(user)
                await session.commit()
            user.attributes['name'] = str(data['name'])
            session.add(user)
            await session.commit()
        self.session.clear()
        self.session['user_id'] = user.id
        self.redirect('/app')

    def check_xsrf_cookie(self: 'LtiLaunchHandler') -> None:
        """Check the XSRF state parameter."""
        tool_config = ToolConfDict(generate_config())
        oidc_request = TornadoLTIRequest(self)
        message_launch = TornadoLTIMessageLaunch(
            request=oidc_request,
            tool_config=tool_config,
            cookie_service=TornadoLTICookieService(self),
        )
        params = message_launch.get_params_from_login()
        if params is None or 'xsrf' not in params or params['xsrf'] != self.session['xsrf']:
            raise HTTPError(status_code=403, log_message='XSRF validation failed')
