from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .analytics import user_activity_analysis


from .models import CustomUser
from .forms import RegistrationForm, LoginForm


def main(request):
    return render(request, "authentication/main.html")


def auth(request):
    return render(request, "authentication/auth.html")


def about(request):
    return render(request, "authentication/about.html")


def register_form(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['confirm']:
            error_message = '<p><div><font size="4" color: white>Unsuccessful registration. Invalid information.</font></div>'
            messages.error(request, mark_safe(error_message))
        else:
            # Використовуйте make_password для шифрування пароля
            hashed_password = make_password(form.cleaned_data['password'])

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
                success_message = '<p><div css="margin-top: 70"><font size="4" css="color: white">Registration successful.</font></div>'
                messages.success(request, mark_safe(success_message))
                return redirect("home")
            else:
                error_message = ('<p><div><font size="4" css="color: white">Unsuccessful registration. Invalid '
                                 'information.</font></div>')
                messages.error(request, mark_safe(error_message))
    return render(request, "authentication/register.html", {'form': form})


from django.contrib.auth.hashers import check_password


def login_form(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = CustomUser.get_by_email(form.cleaned_data['email'])
            if user and check_password(form.cleaned_data['password'], user.password):
                # Використовуйте check_password для порівняння зашифрованих паролів
                login(request, user)
                success_message = '<p><div css="margin-top: 70"><font size="4" css="color: white">Login successful.</font></div>'
                messages.success(request, mark_safe(success_message))
                return redirect("/auth")
            else:
                error_message = '<p><div><font size="4" css="color: white">Unsuccessful login. Invalid information.</font></div>'
                messages.error(request, mark_safe(error_message))
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors below.')
    return render(request, "authentication/login.html", {'form': form})


def logout_request(request):
    logout(request)
    info_message = '<p><div><font size="4" css="color: white">You have successfully logged out.</font></div>'
    messages.info(request, mark_safe(info_message))
    return redirect("login")


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


@login_required
def user_profile(request):
    user_data = request.user.get_user_data()
    return render(request, 'authentication/user_profile.html', {'user_data': user_data})


from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def submit_question(request):
    if request.method == 'POST':
        # Получение текста вопроса из запроса
        question_text = request.POST.get('question_text', '')

        # Отправка электронного письма
        send_mail(
            'New Question',
            question_text,
            settings.EMAIL_HOST_USER,  # Sender's email
            ['hort19345@gmail.com'],  # Recipient's email
            fail_silently=False,
        )

        # Возвращаем успешный ответ
        return JsonResponse({'status': 'success'})

    # Возвращаем ошибку, если запрос не является POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

import matplotlib.pyplot as plt

from django.shortcuts import render
from .models import CustomUser


def user_role_distribution(request):
    users = CustomUser.objects.all()
    roles = [user.get_role_name() for user in users]
    role_counts = {role: roles.count(role) for role in set(roles)}

    role_labels = list(role_counts.keys())  # Метки ролей
    role_values = list(role_counts.values())  # Количество пользователей по ролям

    return render(request, 'authentication/analytics.html', {
        'role_labels': role_labels,
        'role_counts': role_values,
    })

