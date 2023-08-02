from rest_framework import serializers
from .models import *

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitieschat
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitieschat
        fields = '__all__'

class communitieschatSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitieschat
        fields = ['id', 'topic', 'sender', 'message', 'timestamp']