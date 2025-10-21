# ---- Django REST Framework imports for API endpoints ----
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# ---- Imports for register (POST endpoint) ----
from .serializers import RegisterSerializer  # Serializer that handles user creation and validation
from .models import User            # Custom User model
from rest_framework import permissions, generics, status 

# ---- Imports for logout (blacklist) ----
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


# ---- Email verification ----
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as password_reset_token

from .tokens import email_verification_token
    


# ---------------------------------------------
#  REGISTER (public endpoint)
# ---------------------------------------------
class RegisterView(generics.CreateAPIView):
    # Uses DRF’s generic view for creating a new object (User)
    queryset = User.objects.all()              # Defines which model this view operates on
    serializer_class = RegisterSerializer      # Handles validation and hashing password
    permission_classes = [permissions.AllowAny]# Anyone can access (no auth required)
    # -> POST /api/v1/auth/register with email, password, name
    #    creates a new user row in the DB using serializer.create()




# ---------------------------------------------
#  ME (authenticated GET endpoint)
# ---------------------------------------------
class MeView(APIView):
    permission_classes = [IsAuthenticated]     # Only allow users with valid JWTs (Bearer token)

    def get(self, request):
        u = request.user                       # Django automatically fills this from JWT
        return Response({
            "id": str(u.id),
            "email": u.email,
            "name": getattr(u, "name", ""),     # use getattr in case name field doesn't exist
            "is_staff": u.is_staff,
            "is_active": u.is_active,
        })
    # -> GET /api/v1/auth/me returns current user info


# ---------------------------------------------
#  LOGOUT (blacklist tokens)
# ---------------------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]     # Only logged-in users can log out

    def post(self, request):
        # Fetch all unexpired (Outstanding) refresh tokens belonging to this user
        tokens = OutstandingToken.objects.filter(user=request.user)

        for t in tokens:
            try:
                # Mark each token as blacklisted (cannot be reused)
                BlacklistedToken.objects.get_or_create(token=t)
            except Exception:
                # In case a token was already blacklisted or error occurs, ignore
                pass

        # Return 204 (no content) — success, user logged out everywhere
        return Response(status=status.HTTP_204_NO_CONTENT)




# ---- Email verification ----
class RequestVerifyView(APIView):
    """
    POST /api/v1/auth/request-verify   (requires Bearer access)
    Why: sends a one-time verification link to the user (console in dev).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        u = request.user
        if getattr(u, "is_email_verified", False):
            return Response({"ok": True, "already_verified": True})
        uid = urlsafe_base64_encode(force_bytes(u.pk))
        tok = email_verification_token.make_token(u)
        verify_url = request.build_absolute_uri(
            reverse("verify") + f"?uid={uid}&tok={tok}"
        )
        send_mail(
            subject="Verify your Finsaction account",
            message=f"Click to verify your account: {verify_url}",
            from_email=None,
            recipient_list=[u.email],
        )
        return Response({"ok": True})


class VerifyView(APIView):
    """
    GET /api/v1/auth/verify?uid=...&tok=...
    Why: confirms the link, marks the user as verified.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        uidb64 = request.GET.get("uid")
        tok = request.GET.get("tok")
        if not uidb64 or not tok:
            return Response({"detail": "Missing uid or tok"}, status=400)

        U = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            u = U.objects.get(pk=uid)
        except Exception:
            return Response({"detail": "Invalid link"}, status=400)

        if email_verification_token.check_token(u, tok):
            u.is_email_verified = True
            u.email_verified_at = timezone.now()
            u.save(update_fields=["is_email_verified", "email_verified_at"])
            return Response({"ok": True})
        return Response({"detail": "Invalid or expired token"}, status=400)


# ---- Password reset ----
class ForgotPasswordView(APIView):
    """
    POST /api/v1/auth/forgot-password  (public)
    Why: sends a password reset link. Always returns ok to avoid leaking user existence.
    Body: { "email": "you@domain.com" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip()
        if not email:
            return Response({"detail": "email required"}, status=400)

        U = get_user_model()
        try:
            u = U.objects.get(email=email)
        except U.DoesNotExist:
            return Response({"ok": True})  # don't leak

        uid = urlsafe_base64_encode(force_bytes(u.pk))
        tok = password_reset_token.make_token(u)
        reset_url = request.build_absolute_uri(
            reverse("reset-password") + f"?uid={uid}&tok={tok}"
        )
        send_mail(
            subject="Reset your Finsaction password",
            message=f"Reset link: {reset_url}",
            from_email=None,
            recipient_list=[email],
        )
        return Response({"ok": True})


class ResetPasswordView(APIView):
    """
    POST /api/v1/auth/reset-password?uid=...&tok=...   (public)
    Why: validates token and sets a new password securely.
    Body: { "password": "NewStrongPassw0rd!" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.GET.get("uid")
        tok = request.GET.get("tok")
        new_pw = request.data.get("password")
        if not (uidb64 and tok and new_pw):
            return Response({"detail": "uid, tok (query) and password (body) required"}, status=400)

        U = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            u = U.objects.get(pk=uid)
        except Exception:
            return Response({"detail": "Invalid link"}, status=400)

        if not password_reset_token.check_token(u, tok):
            return Response({"detail": "Invalid or expired token"}, status=400)

        u.set_password(new_pw)      # hashes securely
        u.save(update_fields=["password"])
        return Response({"ok": True})