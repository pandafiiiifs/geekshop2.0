from django.urls import path, include

from authapp.views import LoginListView, RegisterListView, ProfileFormView, logout

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>/',  RegisterListView.verify, name='verify'),
    path('logout/', logout, name='logout'),
]