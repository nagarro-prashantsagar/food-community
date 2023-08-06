from django.urls import path
from .views import *

urlpatterns = [
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),

    path('communities/<int:community_id>/join/', JoinCommunity.as_view(), name='join-community'),
    path('communities/<int:community_id>/leave/', LeaveCommunity.as_view(), name='leave-community'),

    path('communities/search/', SearchCommunity.as_view(), name='search-community'),
    path('communities/<int:community_id>/members/', CommunityMembers.as_view(), name='community-members'),
    path('communities/user/list/', UserCommunityList.as_view(), name='user_community_list'),

    path('communities/<int:community_id>/chat/', CommunityChat.as_view(), name='community-chat-list'),
    path('communities/<int:community_id>/start-chat/', StartChatWithCommunity.as_view(),
         name='start-chat-with-community'),
]
