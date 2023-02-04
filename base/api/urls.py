from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cities/', cities),
]