from django.test import TestCase
from accounts.forms import RegistrationForm
from accounts.models import InvitationCode
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class RegistrationFormTest(TestCase):

    def setUp(self):
        # Create a valid invitation code for testing
        self.invitation = InvitationCode.objects.create()
        self.expired_invitation = InvitationCode.objects.create(expires_at=timezone.now() - timezone.timedelta(days=1))

    def test_valid_registration_form(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone_number": "1234567890",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "invitation_code": self.invitation.code,
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.invitation.refresh_from_db()  # refresh invitation from db manually.
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(self.invitation.used_by, user)

    def test_missing_required_fields(self):
        form_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
            "invitation_code": self.invitation.code
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("password1", form.errors)

    def test_invalid_invitation_code(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "invitation_code": "wrongcode"
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("invitation_code", form.errors)
        self.assertEqual(form.errors["invitation_code"][0], "Invalid invitation code.")

    def test_expired_invitation_code(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "invitation_code": self.expired_invitation.code
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("invitation_code", form.errors)
        self.assertEqual(form.errors["invitation_code"][0], "This invitation code is expired or already used.")

    def test_optional_phone_number(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "invitation_code": self.invitation.code,
            "phone_number": ""
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.phone_number, "")
