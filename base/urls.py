from django.urls import path
from .views import *

urlpatterns = [
    path('', get_rides_plan, name="plan"),
    path('form/', find_bus, name='find'),
    path('route/<str:pk>/', get_single_bus, name='bus'),

    path('login/', loginUser, name='loginUser'),
    path('logout/', logoutUser, name='logoutUser'),
    path('register/', registerUser, name='registerUser'),

    path('profile/<str:pk>/', userProfile, name='profile')
]