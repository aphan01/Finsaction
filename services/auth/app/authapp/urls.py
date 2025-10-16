from .views import PingView
from django.urls import path

urlpatterns = [
    path("ping/", PingView.as_view()),
]