from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('chef/<int:pk>/', views.ChefDetailView.as_view(), name='chef_detail'),
    path('chef/<int:pk>/update/', views.ChefUpdateView.as_view(), name='chef_update'),

    path('chef/online/', views.OnlineChefListView.as_view(), name='online_chef_list'),
    path('chats/create/<int:chef_id>/', views.ChatCreateView.as_view(), name='chat-create'),

    path('chats/recent/<int:chef_id>/', views.RecentChatList.as_view(), name='recent-chat-list'),
]