from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerationService(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active) + str(user.email)


account_activation_token = TokenGenerationService()
