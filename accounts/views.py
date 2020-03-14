from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import (
    LoginView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
)
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages

from django.contrib.auth.models import User


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:index')

    context= {'form': UserCreationForm()}
    return render(request, 'registration/signup.html', context)

