from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import InvitationCode

User = get_user_model()


class RegisterViewTest(TestCase):

    def setUp(self):
        """Set up a valid invitation code before each test."""
        self.invitation = InvitationCode.objects.create()
        self.register_url = reverse('register')

    def test_register_page_loads_successfully(self):
        """Ensure the register page loads with a GET request."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_with_valid_data(self):
        """Test registering with valid data and a valid invitation code."""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'email': 'newuser@example.com',
            'invitation_code': self.invitation.code,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('stock:index'))

        # Verify user is created
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)

        # Check the user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

        # Ensure invitation code is marked as used
        self.invitation.refresh_from_db()
        self.assertEqual(self.invitation.used_by, user)

    def test_register_with_invalid_invitation_code(self):
        """Test registration fails with an invalid invitation code."""
        response = self.client.post(self.register_url, {
            'username': 'baduser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'baduser@example.com',
            'invitation_code': 'invalidcode',
        })
        self.assertEqual(response.status_code, 200)  # Stays on the page
        self.assertFormError(response, 'form', 'invitation_code', 'Invalid invitation code.')

        # Ensure user wasn't created
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_register_with_missing_data(self):
        """Test registration fails with missing fields."""
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': '',
            'password2': '',
            'email': '',
            'invitation_code': self.invitation.code,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='').exists())
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password1', 'This field is required.')

    def test_register_with_mismatched_passwords(self):
        """Ensure registration fails if passwords don't match."""
        response = self.client.post(self.register_url, {
            'username': 'mismatchuser',
            'password1': 'password123',
            'password2': 'differentpassword',
            'email': 'mismatch@example.com',
            'invitation_code': self.invitation.code,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")
