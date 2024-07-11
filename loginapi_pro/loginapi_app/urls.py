from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('update_password/',UserChangePasswordView.as_view(),name='chage_password'),
    path('reset-password-email/',SendPasswordResetEmailView.as_view(),name='reset'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset_password')
]
