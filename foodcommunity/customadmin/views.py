from .forms import CustomUserLoginForm
import json
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from .forms import AdminLoginForm
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authtoken.models import Token
from .authentication import CustomUserEmailBackend


class CustomUserLogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})

class CustomUserLoginView(APIView):
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # print(email,password)

            # Authenticate the user with the custom authentication backend
            user = CustomUserEmailBackend.authenticate(self, request=request, email=email, password=password)
            # user = EmailAuthBackend.get_user(self,email)
            print(user)
            if user is not None:
                print(user)
                # The user is authenticated, return the token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_200_OK)
            else:
                # The user could not be authenticated, return an error response
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserSignupView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Save the user with a hashed password
                user = serializer.save()
                return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class AdminLoginView(View):
    def post(self, request):
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid login credentials'}, status=401)
        else:
            return JsonResponse({'errors': form.errors}, status=400)


class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
