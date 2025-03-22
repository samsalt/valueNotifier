from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login
from django.utils import timezone
from .forms import RegistrationForm
from .models import InvitationCode
# from django.contrib.auth import get_user_model

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('stock:index')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})