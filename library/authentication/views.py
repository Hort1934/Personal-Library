from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser
from .forms import RegistrationForm, LoginForm


def auth(request):
    return render(request, "authentication/auth.html")


def register_form(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['confirm']:
            messages.error(request, "Unsuccessful registration. Invalid information.")
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
                messages.success(request, "Registration successful.")
                return redirect("home")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, "authentication/register.html", {'form': form})


def login_form(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = CustomUser.get_by_email(form.cleaned_data['email'])
        if user and user.password == form.cleaned_data['password']:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful login. Invalid information.")
    return render(request, "authentication/login.html", {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def all_users(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        users = CustomUser.objects.all()
        return render(request, 'authentication/all_users.html', {'users': users})
    else:
        return HttpResponseNotFound("page not found")


def view_user(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        users = CustomUser.objects.all()
        return render(request, 'authentication/view_user.html', {'user': user})
    else:
        return HttpResponseNotFound("page not found")
