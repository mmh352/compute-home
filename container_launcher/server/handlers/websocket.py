"""Websocket handler."""
from tornado.websocket import WebSocketHandler


class ApiHandler(WebSocketHandler):
    """Handle all API requests."""

    async def on_message(self: 'ApiHandler', msg: str) -> None:
        """Run the appropriate action upon receiving a Websocket message."""
        # print(msg)
