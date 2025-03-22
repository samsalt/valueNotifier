from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import InvitationCode

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    invitation_code = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2", "invitation_code")

    def clean_invitation_code(self):
        code = self.cleaned_data.get("invitation_code")
        try:
            invitation = InvitationCode.objects.get(code=code)
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError("Invalid invitation code.")

        if not invitation.is_valid():
            raise forms.ValidationError("This invitation code is expired or already used.")

        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.phone_number = self.cleaned_data.get("phone_number")

        if commit:
            user.save()
            invitation = InvitationCode.objects.get(code=self.cleaned_data.get("invitation_code"))
            invitation.used_by = user
            invitation.used_at = timezone.now()
            invitation.save()

        return user
