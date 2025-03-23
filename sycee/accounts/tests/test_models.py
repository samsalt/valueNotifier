from django.test import TestCase
from django.utils import timezone
from accounts.models import InvitationCode
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class InvitationCodeModelTest(TestCase):

    def test_invitation_code_creation(self):
        """Test that an invitation code is created correctly."""
        invitation = InvitationCode.objects.create()
        self.assertIsNotNone(invitation.code)
        self.assertEqual(len(invitation.code), 10)
        self.assertTrue(invitation.expires_at > timezone.now())

    def test_invitation_code_uniqueness(self):
        """Ensure generated codes are unique."""
        code1 = InvitationCode.objects.create()
        code2 = InvitationCode.objects.create()
        self.assertNotEqual(code1.code, code2.code)

    def test_invitation_code_expiration(self):
        """Check if an invitation code is marked expired correctly."""
        expired_invitation = InvitationCode.objects.create(
            expires_at=timezone.now() - datetime.timedelta(days=1)
        )
        self.assertFalse(expired_invitation.is_valid())

    def test_invitation_code_validity(self):
        """Check if a valid invitation code is recognized."""
        valid_invitation = InvitationCode.objects.create()
        self.assertTrue(valid_invitation.is_valid())

    def test_invitation_code_used(self):
        """Ensure used invitation codes are invalid."""
        user = User.objects.create_user(username='testuser', password='password123')
        used_invitation = InvitationCode.objects.create()
        used_invitation.used_by = user
        used_invitation.used_at = timezone.now()
        used_invitation.save()

        self.assertFalse(used_invitation.is_valid())

    def test_save_generates_unique_code(self):
        """Ensure save generates a unique code only on first save."""
        invitation = InvitationCode.objects.create()
        old_code = invitation.code
        invitation.save()
        self.assertEqual(invitation.code, old_code)  # Code should remain unchanged

    def test_str_representation(self):
        """Ensure the string representation is the code itself."""
        invitation = InvitationCode.objects.create()
        self.assertEqual(str(invitation), invitation.code)
