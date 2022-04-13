from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.api.views import RegistrationView, LogoutView

urlpatterns = [
    path('', obtain_auth_token, name='login'),
    path('register/', RegistrationView, name='createUser'),
    path('logout/', LogoutView, name='logout'),
]
