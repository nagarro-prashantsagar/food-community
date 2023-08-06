from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from rest_framework import status, generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChefSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    # def post(self, request):
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     print(email,password)
    #
    #     chef = authenticate(request, username=email, password=password)
    #     print(chef)
    #     if chef is not None:
    #         token, _ = Token.objects.get_or_create(user=chef)
    #         return Response({'token': token.key}, status=status.HTTP_200_OK)
    #
    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        chef = get_object_or_404(Chef, email=email)
        print(email,password)
        # chef = authenticate(request, email=email, password=password)
        if chef.email == email and chef.password == password:
            print(email,password)
        if chef is not None:
            login(request, chef)
            print(chef)
            # login(request, chef)
            token, _ = Token.objects.get_or_create(chef=chef)
            chef.is_online = True
            chef.save()
            return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)
        return Response('Invalid credentials', status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        chef = request.user
        # Set the is_online status to False when the chef logs out
        chef.is_online = False
        chef.save()
        logout(request)
        return Response('Logged out successfully!', status=HTTP_200_OK)


class ChefDetailView(DetailView):
    model = Chef
    # template_name = 'chef/chef_detail.html'  # Replace with the path to your template if needed

    def render_to_response(self, context, **response_kwargs):
        # Convert the cuisine_specialty object to a dictionary
        chef = context['object']
        cuisine_specialty_dict = {
            'id': chef.cuisine_specialty.id,
            'name': chef.cuisine_specialty.name,
            # Add other fields you want to include in the response
        }

        # Convert the Chef object to a dictionary
        chef_details = {
            'id': chef.id,
            'username': chef.username,
            'cuisine_specialty': cuisine_specialty_dict,
            'restaurant_name': chef.restaurant_name,
            'experience_years': chef.experience_years,
            'short_info': chef.short_info,
            # Add other fields you want to include in the response
        }

        return JsonResponse(chef_details)


class ChefUpdateView(APIView):
    def put(self, request, pk):
        try:
            chef = Chef.objects.get(pk=pk)
        except Chef.DoesNotExist:
            return Response({'error': 'Chef not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChefSerializer(chef, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OnlineChefListView(ListAPIView):
    queryset = Chef.objects.filter(is_online=True)
    serializer_class = ChefSerializer

class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chef_id = self.kwargs.get('chef_id')
        chef = get_object_or_404(User, id=chef_id)

        serializer.save(user=self.request.user, chef=chef)

        # Create a welcome message from the CustomUser to the Chef
        ChatMessage.objects.create(chat=serializer.instance, sender=self.request.user, content="Hello Chef!")

        # Create a welcome message from the Chef to the CustomUser
        ChatMessage.objects.create(chat=serializer.instance, sender=chef, content="Hello! How can I assist you?")


class RecentChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chef_id = self.kwargs.get('chef_id')
        return Chat.objects.filter(chef__id=chef_id).order_by('-timestamp')[:10]