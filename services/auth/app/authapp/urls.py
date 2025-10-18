from .views import RegisterView, MeView, LogoutView
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class PingView(APIView):
    def get(self, request):
        return Response({"ok": True, "data": {"pong": True}})
urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
    path("auth/register", RegisterView.as_view(),    name="register"),
    path("auth/login",    TokenObtainPairView.as_view(),  name="token_obtain_pair"),
    path("auth/refresh",  TokenRefreshView.as_view(),     name="token_refresh"),
    path("auth/me",       MeView.as_view(),          name="me"),
    path("auth/logout",   LogoutView.as_view(),      name="logout"),
]

