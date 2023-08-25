from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import UserLoginForm, UserRegForm, UserProfileForm


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Profile', 'form': form}
    return render(request, 'users/profile.html', context)


def login(request):
    if request.method == 'POST':
        data = request.POST
        form = UserLoginForm(data=data)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))
            else:
                return PermissionDenied()
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        data = request.POST
        form = UserRegForm(data=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь зарегистрирован!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegForm()
    return render(request, 'users/registration.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
