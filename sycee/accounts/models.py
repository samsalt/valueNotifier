import secrets
import string
from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_invitation_code(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class InvitationCode(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='invitation_code'
    )
    used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            # Generate a unique code
            while True:
                new_code = generate_invitation_code()
                if not InvitationCode.objects.filter(code=new_code).exists():
                    self.code = new_code
                    break
            # Set expiration to 30 days from creation
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used_by and self.expires_at > timezone.now()

    def __str__(self):
        return self.code