from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import RegisterUser

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
