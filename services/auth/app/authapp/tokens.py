from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationToken(PasswordResetTokenGenerator):
    """
    Re-uses Django’s built-in time-safe token generator logic.
    Each token includes the user’s primary key, last login timestamp,
    and a timestamp counter to prevent reuse after password change.
    """
    pass


# instantiate one reusable generator
email_verification_token = EmailVerificationToken()