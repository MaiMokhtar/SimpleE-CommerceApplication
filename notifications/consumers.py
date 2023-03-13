import json

from channels.generic.websocket import AsyncWebsocketConsumer

from notifications import constants


class NotificationConsumer(AsyncWebsocketConsumer):
    """Class representing a WebSocket consumer for notifications."""
    async def connect(self):
        """Method called when a client connects to the WebSocket."""
        if self.scope["user"].is_anonymous:
            self.close()
            return

        self.group_name = constants.NOTIFICATIONS_GROUP_NAME_PREFIX + self.scope["user"].username

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Method called when a client disconnects from the WebSocket.

        Args:
            close_code: A code indicating the reason for the WebSocket connection closing.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        """Method to receive and send notifications to the WebSocket.

        Args:
            event: A dictionary containing the message to be sent to the WebSocket.
        """
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
