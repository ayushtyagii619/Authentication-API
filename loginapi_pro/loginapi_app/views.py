from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UseerChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

#This project done by Ayush Tyagi.
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Successfully registration'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = UseerChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def post(self,request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send to email. Please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserPasswordResetView(APIView):
    def post(self,request,uid,token):
        serializer = UserPasswordResetSerializer(data=request.data,context = {'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)