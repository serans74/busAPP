from django.urls import path, include
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),
    path('auth/', views.obtain_auth_token)
]
