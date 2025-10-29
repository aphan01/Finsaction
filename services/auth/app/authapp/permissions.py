from rest_framework.permissions import BasePermission

class IsEmailVerified(BasePermission):
    """
    Blocks access unless user.is_email_verified == True
    """
    message = "Email not verified."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_email_verified", False)
        )