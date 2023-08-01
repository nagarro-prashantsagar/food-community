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

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'