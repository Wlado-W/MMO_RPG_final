#urls.py
from django.urls import path, include
from .views import AccountProfile, UpdateProfile, auth_code


urlpatterns = [
  path('profile/', AccountProfile.as_view(), name='profile_accounts'),
  path('edit/', UpdateProfile.as_view(), name='edit_accounts'),
  path('auth_code', auth_code, name='auth_code'),
  path('', include('allauth.urls')),
]
