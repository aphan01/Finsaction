"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse

class HealthView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        db_ok = True
        try:
            from django.db import connection
            with connection.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        except Exception:
            db_ok = False
        return Response({
            "ok": True, 
            "service": "auth", 
            "status": "healthy",
            "db": "ok" if db_ok else "down"
            })
def root(_request): 
    return JsonResponse({"ok": True, "service": "Finsaction Auth", "v": 1})
urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", HealthView.as_view(), name= "health"),
    path("api/v1/auth/", include ("authapp.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("", root),
]
