from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('register_success')  # بعد التسجيل يروح صفحة النجاح
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def register_success(request):
    return render(request, 'accounts/register_success.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"مرحباً {user.first_name}! سعدنا بعودتك 🎉")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
