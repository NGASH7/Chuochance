from django.urls import path
from .views import home, profile

urlpatterns = [
    path('', home, name='home'),
    path('users/profile/', profile, name='profile'),
]
