

# # Create your views here.
# from django.shortcuts import render
# # Create your views here.
# from rest_framework import viewsets, filters
# from django_filters import rest_framework as filters
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from django.contrib.auth import authenticate, login, logout
# from rest_framework.exceptions import AuthenticationFailed
# from django.http import HttpResponse
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token
# from .serializer import *
# from foodapp.permission import isDonorReadOnly


# class RegistrationAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.set_password(serializer.validated_data['password']) 
#             user.save()
#             return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class LoginAPIView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         if not username or not password:
#             raise AuthenticationFailed('Both username and password are required')
        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
#         if user:
           
#             if not user.is_active:
#                 raise AuthenticationFailed('User account is inactive')
            
    
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key, 'username': user.username, 'role': user.role})
        
#         raise AuthenticationFailed('Invalid username or password')


# class LogoutAPIView(APIView):
#    permission_classes = [IsAuthenticated]
#    def post(self, request):
#       username = request.data.get('username')
#       password = request.data.get('password')
#       if not(username and password):
#          return Response({'detail':'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
#       user = authenticate(username=username, password=password)
#       if user is not None:
#          logout(request)
#          try:
#             token = Token.objects.get(user=user)
#             token.delete()
#             return Response({'detail': 'Successfully logged out.'})
#          except Token.DoesNotExist:
#             return Response({'detail': 'Token does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#       else:
#          return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render
# from .models import *
# from .serializer import *
# from rest_framework import viewsets,status
# from django.core.mail import send_mail
# import random
# from rest_framework.response import Response
# from django.conf import settings
# from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
   
# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# # Create your views here.
# # class UserViewset(viewsets.ModelViewSet):
# #    queryset = User.objects.all().order_by('email')
# #    serializer_class = UserSerializer

# class OTPVerificationViewset(viewsets.ModelViewSet):
#    queryset = OTPVerification.objects.all().order_by('email')
#    serializer_class = OTPVerificationSerializer
   
#    @action(detail = False, methods = ['post'], url_path = 'send-otp')
#    def send_otp(self,request):
#       email = request.data.get('email')
      
#       if email:
#          otp = random.randint(100000, 999999)
#          otp_record,created = OTPVerification.objects.update_or_create(
#             email = email,
#             defaults = {'otp':str(otp),'otp_created_at':timezone.now()}
#          )
         
#          send_mail(
#             'Your OTP code',
#             f'YOur OTP code is {otp}',
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=False
#          )
#          return Response({"message":"OTP send successfully","otp":otp},status = status.HTTP_200_OK)
#       return Response({"error":"Email is required"},status = status.HTTP_400_BAD_REQUEST)
   
#    @action(detail=False, methods=['post'],url_path='verify-otp')
#    def verify_otp(self,request):
#       email = request.data.get('email')
#       otp = request.data.get('otp')
      
#       if email and otp:
#          try:
#             otp_record = OTPVerification.objects.get(email = email,otp=otp)
            
#             if otp_record.is_expired():
#                otp_record.delete()
#                return Response({"error":"OTP is expired"},status = status.HTTP_400_BAD_REQUEST)
            
#             otp_record.delete()
#             return Response({"message":"OTP verified successfully"},status = status.HTTP_200_OK)
         
#          except OTPVerification.DoesNotExist:
#             return Response({"error":"Invalid OTP"},status = status.HTTP_400_BAD_REQUEST)
      
#       return Response ({"error":"Email and OTP are required"},status = status.HTTP_400_BAD_REQUEST)
   


# User = get_user_model()
# @csrf_exempt

# def register_view(request):
#     if request.method=='GET':
#       return render(request, 'signup.html')
#     elif  request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')  # Get confirm password
#         name = request.POST.get('name')
#         phone_number = request.POST.get('phone_number')
#         address = request.POST.get('address')
#         img = request.FILES.get('img')  # Handle optional image upload

#         if password != confirm_password:  # Password matching validation
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'signup.html')

#         try:
#             user = User.objects.create_user(
#                 email=email,
#                 password=password,
#                 Name=name,
#                 Phone_Number=phone_number,
#                 Address=address,
#                 Img=img
#             )
#             messages.success(request, "Registration successful!")
#             return redirect('login')  # Redirect to login or any other page
#         except Exception as e:
#             messages.error(request, f"Registration failed: {e}")

#     return render(request, 'signup.html')
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser
from rest_framework import generics 
import json
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.response import Response,SimpleTemplateResponse
from .serializer import *
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseForbidden
from django.contrib.auth import logout as django_logout
   
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializer import DonorSignupSerializer, RecipientSignupSerializer


class DonorSignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        serializer = DonorSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonorLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f'Username: {username}, Password: {password}')
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                return Response({'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)

            if not user.is_Donor:
                return Response({'error': 'User is not registered as a Donor'}, status=status.HTTP_403_FORBIDDEN)

            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RecipientSignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'usersignup.html')

    def post(self, request):
        serializer = RecipientSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipientLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'recipientlogin.html')
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                return Response({'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)

            if not user.is_Recipient:
                return Response({'error': 'User is not registered as a Recipient'}, status=status.HTTP_403_FORBIDDEN)

            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, request):
        user = request.user

        if not user:
            return HttpResponseForbidden("Access Denied: You are not a user.")

        context = {
            'username': user.username,
            'phone': user.phone,
            'is_donor': user.is_Donor,
            'is_recipient': user.is_Recipient,
        }
        return render(request, 'dashboard.html', context)

        return render(request, 'dashboard.html', context)
    
class logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve token from request
            token = request.auth  # Valid if DRF's TokenAuthentication is used
            print(f'Token received: {token}')  # Debugging log to confirm receipt of token

            # Delete the token to log out
            if token:
                token.delete()  # This deletes the token instance from the database
                django_logout(request)  # Ends the session
                return Response({'message': 'Logout successful.'}, status=200)
            else:
                return Response({'message': 'Token not found or invalid.'}, status=400)

        except Exception as e:
            return Response({'message': 'Logout failed. Please try again.', 'error': str(e)}, status=400)