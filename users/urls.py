from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CreateSkillView, DeleteSkillView, RegisterUserView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("skill/", CreateSkillView.as_view(), name="skill"),
    path("skill/<int:pk>/", DeleteSkillView.as_view(), name="skill_delete"),
]
