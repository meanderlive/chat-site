

# consumers.py
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Message, UserProfile
import json
from django.db.models import Q

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.receiver_username = self.scope['url_route']['kwargs']['username']

        # Create a unique room name for the two users
        users = sorted([self.user.username, self.receiver_username])
        self.room_name = f'chat_{users[0]}_{users[1]}'

        try:
            self.receiver = User.objects.get(username=self.receiver_username)
            self.receiver_profile = UserProfile.objects.get(user=self.receiver)
        except User.DoesNotExist:
            self.close()
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

        # Fetch previous messages and send them to WebSocket
        previous_messages = Message.objects.filter(
            (Q(sender=self.user) & Q(receiver=self.receiver)) |
            (Q(receiver=self.user) & Q(sender=self.user))
        ).order_by('timestamp')

        for message in previous_messages:
            self.send(text_data=json.dumps({
                'message': message.content,
                'sender': message.sender.username,
                'sender_name': message.sender.userprofile.name,
                'sender_image': message.sender.userprofile.image.url,
                'timestamp': str(message.timestamp)
            }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to database
        message_instance = Message.objects.create(sender=self.user, receiver=self.receiver, content=message)

        # Get sender's profile image URL
        sender_profile_image_url = self.user.userprofile.image.url

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'sender_name': self.user.userprofile.name,
                'sender_image': sender_profile_image_url,
                'timestamp': str(message_instance.timestamp)
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_name = event['sender_name']
        sender_image = event['sender_image']
        timestamp = event['timestamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_name': sender_name,
            'sender_image': sender_image,
            'timestamp': timestamp
        }))









