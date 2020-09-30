from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import logging
from group.models import group,message
from personal.models import UserProfile
import datetime
# logging module with django logging
logger = logging.getLogger('django')
logger.debug('msg')
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("connecting")
        # get name from ws url args
        self.group_id = self.scope['url_route']['kwargs']['group_id'] 
        # self.name = self.scope['url_route']['kwargs']['name']
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_id,
            self.channel_name
        )

        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.accept()
            

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        user=UserProfile.objects.get(user=self.scope['user'])
        now_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        user_name = user.name
        g_unit = group.objects.get(id=self.group_id)
        message.objects.create( message=msg, group=g_unit, owner=user)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_id,
            {
                'type': 'chat_message',
                'message': msg,
                'user': str(user),
                'user_name':user_name,
                'now_time': now_time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        msg = event['message']
        now_time = event['now_time']
        user = event['user']
        user_name = event['user_name']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': msg,
            'user': user,
            'user_name':user_name,
            'now_time': now_time,
        }))