from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login
from django.utils import timezone
from .forms import RegistrationForm
from .models import InvitationCode
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            code_value = form.cleaned_data['invitation_code']
            with transaction.atomic():
                try:
                    # Lock the invitation code row to prevent concurrent use
                    code = InvitationCode.objects.select_for_update().get(code=code_value)
                except InvitationCode.DoesNotExist:
                    form.add_error('invitation_code', 'Invalid code.')
                    return render(request, 'registration/register.html', {'form': form})

                if not code.is_valid():
                    form.add_error('invitation_code', 'Code is invalid or expired.')
                    return render(request, 'registration/register.html', {'form': form})

                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )

                # Assign the code to the user
                code.used_by = user
                code.used_at = timezone.now()
                code.save()

                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})