from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import AdminLoginForm
from .serializers import *
from .backends import CustomUserAuthenticationBackend


class CustomUserLogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})


# @csrf_exempt
class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Use the custom authentication backend to authenticate custom users
        user_backend = CustomUserAuthenticationBackend()
        user = user_backend.authenticate(request, username=email, password=password)

        if user is not None:
            # Use the default authenticate() function with the custom backend
            authenticated_user = authenticate(request, username=email, password=password,
                                              backend='your_app_name.backends.CustomUserAuthenticationBackend')
            if authenticated_user is not None:
                login(request, authenticated_user)
                return Response('Login successful!', status=status.HTTP_200_OK)

        return Response('Invalid credentials', status=status.HTTP_401_UNAUTHORIZED)
    # def post(self, request):
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     tempuser = get_object_or_404(CustomUser, email=email)
    #     if (tempuser.email == email and tempuser.password == password):
    #         login(request, tempuser)
    #         # print(tempuser)
    #         return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
    # @csrf_exempt
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
