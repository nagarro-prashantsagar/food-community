from django.urls import path
from .views import *

urlpatterns = [
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),
    path('communitieshat/', ChatRoomList.as_view(), name='chatroom-list'),
    path('communitieshat/<int:room_id>/messages/', MessageList.as_view(), name='message-list'),
    path('communities/<int:community_id>/join/', JoinCommunity.as_view(), name='join-community'),
]
