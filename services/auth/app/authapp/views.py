#GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#POST
from .serializers import RegisterSerializer  #
from .models import User
from rest_framework import permissions, generics, status #
#Logout
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": str(u.id),
            "email": u.email,
            "name": getattr(u, "name", ""),
            "is_staff": u.is_staff,
            "is_active": u.is_active,
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Blacklist all outstanding tokens for this user (server-side logout everywhere)
        tokens = OutstandingToken.objects.filter(user=request.user)
        for t in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=t)
            except Exception:
                pass
        return Response(status=status.HTTP_204_NO_CONTENT)