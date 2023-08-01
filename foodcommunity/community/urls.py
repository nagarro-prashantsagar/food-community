from django.urls import path
from .views import *

urlpatterns = [
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),

    path('communitieschat/', ChatRoomList.as_view(), name='chatroom-list'),
    path('communitieschat/<int:room_id>/', MessageList.as_view(), name='message-list'),

    path('communities/<int:community_id>/join/', JoinCommunity.as_view(), name='join-community'),
    path('communities/search/', SearchCommunity.as_view(), name='search-community'),
    path('communities/<int:community_id>/members/', CommunityMembers.as_view(), name='community-members'),
]
