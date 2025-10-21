from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationToken(PasswordResetTokenGenerator):
    """Uses Django’s built-in, time-safe token logic for email verification."""
    pass

email_verification_token = EmailVerificationToken()
