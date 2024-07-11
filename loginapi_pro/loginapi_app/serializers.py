from rest_framework import serializers
from .models import AyushUser
from django.forms import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = AyushUser
        fields = ['email','name','password','password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Both password does not match")
        return attrs
    
    def create(self,validate_data):
        return AyushUser.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = AyushUser
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyushUser
        fields = ['id','email','name']

class UseerChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length=200,style = {'input_type':'password'},write_only = True)
    class Meta:
        model = AyushUser
        fields = ['password','password2']

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Both password does not match")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = AyushUser
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email')
        if AyushUser.objects.filter(email=email).exists():
            user = AyushUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Link',link)
            body = 'Click Following Link to Reset Your Password' + link
            data = {
                'subject':'Reset your password',
                'body' : body,
                'to_email' : user.email
            }
            util.send_email(data)
            return attrs
        else:
            raise ValidationError('you are not registered user')
        

class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length=200,style = {'input_type':'password'},write_only = True)
    class Meta:
        model = AyushUser
        fields = ['password','password2']

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("Both password does not match")
        id = smart_str(urlsafe_base64_decode(uid))
        user = AyushUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise ValidationError('Token is not valid or expired')
        user.set_password(password)
        user.save()
        return attrs
        
