from django.urls import path

from authapp.views import UserLoginView, UserRegisterView, profile, logout

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>/', UserRegisterView.verify, name='verify'),
]