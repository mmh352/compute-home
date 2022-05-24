"""Websocket handler."""
import json
import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from tornado.websocket import WebSocketHandler
from typing import Callable

from ..session import SessionMixin
from ...models import get_sessionmaker, User
from ...utils import config


logger = logging.getLogger(__name__)


class ApiHandler(WebSocketHandler, SessionMixin):
    """Handle all API requests."""

    async def open(self: 'ApiHandler') -> None:
        """Handle opening the connection and initialising the user."""
        logger.debug('Accepting a new API connection')
        self._user = None

    async def on_message(self: 'ApiHandler', data: str) -> None:
        """Run the appropriate action upon receiving a Websocket message."""
        try:
            msg = json.loads(data)
            if 'type' in msg:
                if msg['type'] == 'request-config':
                    self.request_config()
                elif msg['type'] == 'request-user':
                    await self.request_user()
                elif self._user is not None:
                    if msg['type'] == 'request-containers':
                        self.request_containers()
            else:
                logger.debug(f'Invalid message {json.dumps(msg)}')
        except json.JSONDecodeError as e:
            logger.error(e)

    def send_message(self: 'ApiHandler', msg: str) -> None:
        """Send a message back to the client."""
        self.write_message(json.dumps(msg))

    def request_config(self: 'ApiHandler') -> None:
        """Handle the request for the current configuration."""
        self.send_message({
            'type': 'config',
            'config': {
                'title': config()['app']['title'],
                'vle': config()['app']['vle']
            }
        })

    async def request_user(self: 'ApiHandler') -> Callable[[], None]:
        """Handle the request for the logged in user.

        Fetch the user from the database if not done yet.
        """
        if 'user_id' in self.session:
            if self._user is None:
                async with get_sessionmaker()() as dbsession:
                    stmt = select(User).filter(User.id == self.session['user_id']).options(selectinload(User.groups))
                    result = await dbsession.execute(stmt)
                    try:
                        self._user = result.scalar_one()
                    except NoResultFound:
                        self.send_message({'type': 'unauthorised'})
                        self.close()
            self.send_message({
                'type': 'user',
                'user': {
                    'id': str(self._user.id),
                    'name': self._user.attributes['name'],
                }
            })
        else:
            self.send_message({'type': 'logged-out'})
            self.close()

    def request_containers(self: 'ApiHandler') -> None:
        """Request the currently configured containers."""
        containers = []
        group_ids = set(map(lambda g: g.external_id, self._user.groups))
        for container_config in config()['app']['containers']:
            if len(group_ids.intersection(container_config['groups'])) > 0:
                containers.append({
                    'name': container_config['name'],
                    'title': container_config['title'],
                    'description': container_config['description'],
                    'state': 'paused',
                })
        self.send_message({
            'type': 'containers',
            'containers': containers
        })
