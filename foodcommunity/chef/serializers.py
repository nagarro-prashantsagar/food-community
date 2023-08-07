from rest_framework import serializers
from .models import *


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('email','first_name','last_name','restaurant_name','short_info', 'password', 'cuisine_specialty', 'experience_years')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        chef = Chef(**validated_data)
        chef.set_password(password)
        chef.save()
        return chef



# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = ['id', 'sender', 'content', 'timestamp']
#
# class ChatSerializer(serializers.ModelSerializer):
#     messages = ChatMessageSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Chat
#         fields = ['id', 'user', 'chef', 'timestamp', 'messages']
