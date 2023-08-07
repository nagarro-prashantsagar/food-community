from rest_framework import serializers
from .models import *


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitiesChat
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitiesChat
        fields = '__all__'


class communitieschatSerializer(serializers.ModelSerializer):
    class Meta:
        model = communitiesChat
        fields = ['id', 'topic', 'sender', 'message', 'timestamp']


class CommunityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['name', 'description']
