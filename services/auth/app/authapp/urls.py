from .views import RegisterView, MeView, LogoutView, RequestVerifyView, VerifyView, ForgotPasswordView, ResetPasswordView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register", RegisterView.as_view(),    name="register"),
    path("login",    TokenObtainPairView.as_view(),  name="token_obtain_pair"),
    path("refresh",  TokenRefreshView.as_view(),     name="token_refresh"),
    path("me",       MeView.as_view(),          name="me"),
    path("logout",   LogoutView.as_view(),      name="logout"),
    path("request-verify", RequestVerifyView.as_view(), name="request-verify"),
    path("verify", VerifyView.as_view(), name="verify"),
    path("forgot-password", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password", ResetPasswordView.as_view(), name="reset-password"),
]

