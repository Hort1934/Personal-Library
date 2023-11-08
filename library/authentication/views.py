from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import CustomUser
from .forms import RegistrationForm, LoginForm


def auth(request):
    return render(request, "authentication/auth.html")


def register_form(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['confirm']:
            error_message = '<div><font size="5">Unsuccessful registration. Invalid information.</font></div>'
            messages.error(request, mark_safe(error_message))
        else:
            user = CustomUser.create(
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                form.cleaned_data['first_name'],
                form.cleaned_data['middle_name'],
                form.cleaned_data['last_name'],
                form.cleaned_data.get('role', 0)
            )
            if user:
                login(request, user)
                success_message = '<div><font size="5">Registration successful.</font></div>'
                messages.success(request, mark_safe(success_message))
                return redirect("home")
            else:
                error_message = '<div><font size="5">Unsuccessful registration. Invalid information.</font></div>'
                messages.error(request, mark_safe(error_message))
    return render(request, "authentication/register.html", {'form': form})


def login_form(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = CustomUser.get_by_email(form.cleaned_data['email'])
        if user and user.password == form.cleaned_data['password']:
            login(request, user)
            success_message = '<div><font size="5">Login successful.</font></div>'
            messages.success(request, mark_safe(success_message))
            return redirect("home")
        else:
            error_message = '<div><font size="5">Unsuccessful login. Invalid information.</font></div>'
            messages.error(request, mark_safe(error_message))
    return render(request, "authentication/login.html", {'form': form})


def logout_request(request):
    logout(request)
    info_message = '<div><font size="5">You have successfully logged out.</font></div>'
    messages.info(request, mark_safe(info_message))
    return redirect("home")


def all_users(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        users = CustomUser.objects.all()
        return render(request, 'authentication/all_users.html', {'users': users})
    else:
        return render(request, 'authentication/error.html')


def view_user(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        users = CustomUser.objects.all()
        return render(request, 'authentication/view_user.html', {'user': user})
    else:
        return render(request, 'authentication/error.html')


def user_profile(request):
    # Логіка для обробки сторінки особистого кабінету тут
    return render(request, 'authentication/user_profile.html')
