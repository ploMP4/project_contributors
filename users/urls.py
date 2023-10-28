from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CreateSkillView,
    DeleteSkillView,
    RegisterUserView,
    RequestPasswordResetUserView,
    ResetPasswordUserView,
    RetrieveUserWithStatsView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path(
        "password-reset/",
        RequestPasswordResetUserView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset/<int:pk>/<str:token>/",
        ResetPasswordUserView.as_view(),
        name="password_reset_confirm",
    ),
    path("<int:pk>/stats/", RetrieveUserWithStatsView.as_view(), name="user_stats"),
    path("skill/", CreateSkillView.as_view(), name="skill"),
    path("skill/<int:pk>/", DeleteSkillView.as_view(), name="skill_delete"),
]
