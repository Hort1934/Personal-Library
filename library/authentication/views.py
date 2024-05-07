from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .analytics import user_activity_analysis
import matplotlib.pyplot as plt
from .models import CustomUser
from collections import Counter
import calendar
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


def main(request):
    return render(request, "authentication/main.html")


def auth(request):
    user_data = request.user.get_user_data()
    return render(request, "authentication/auth.html", {'user_data': user_data})


def about(request):
    user_data = request.user.get_user_data()
    return render(request, "authentication/about.html", {'user_data': user_data})


def register_form(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['confirm']:
            error_message = '<p><div><font size="4" color: white>Unsuccessful registration. Invalid information.</font></div>'
            messages.error(request, mark_safe(error_message))
        else:
            hashed_password = make_password(form.cleaned_data['password'])

            user = CustomUser.create(
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                form.cleaned_data['first_name'],
                # form.cleaned_data['middle_name'],
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


def login_form(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = CustomUser.get_by_email(form.cleaned_data['email'])
            if user and check_password(form.cleaned_data['password'], user.password):
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
    return redirect("/")


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


@csrf_exempt
def submit_question(request):
    if request.method == 'POST':
        # Отримання тексту запитання із запиту
        question_text = request.POST.get('question_text', '')

        # Надсилання електронного листа
        send_mail(
            'New Question',
            question_text,
            settings.EMAIL_HOST_USER,  # Email відправника
            ['hort19345@gmail.com'],  # Email одержувача
            fail_silently=False,
        )

        # Повертаємо успішну відповідь
        return JsonResponse({'status': 'success'})

    # Повертаємо помилку, якщо запит не є POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def user_role_distribution(request):
    users = CustomUser.objects.all()
    roles = [user.get_role_name() for user in users]
    role_counts = {role: roles.count(role) for role in set(roles)}

    role_labels = list(role_counts.keys())  # Мітки ролей
    role_values = list(role_counts.values())  # Кількість користувачів за ролями

    return render(request, 'authentication/analytics.html', {
        'role_labels': role_labels,
        'role_counts': role_values,
    })


def user_registration_by_year(request):
    users = CustomUser.objects.all()
    registration_years = [user.created_at.year for user in users]
    year_counts = Counter(registration_years)

    years = sorted(year_counts.keys())
    registration_counts = [year_counts[year] for year in years]

    return render(request, 'authentication/user_registration_by_year.html', {
        'years': years,
        'registration_counts': registration_counts,
    })


def user_registration_by_day(request):
    users = CustomUser.objects.all()
    registration_days = [user.created_at.weekday() for user in users]
    day_counts = Counter(registration_days)

    day_names = list(calendar.day_name)
    registration_counts = [day_counts[i] for i in range(7)]

    return render(request, 'authentication/user_registration_by_day.html', {
        'day_names': day_names,
        'registration_counts': registration_counts,
    })


def analytics_dashboard(request):
    # Отримуємо дані для всіх трьох графіків
    users = CustomUser.objects.all()

    # Розподіл ролей користувачів
    roles = [user.get_role_name() for user in users]
    role_counts = Counter(roles)
    role_labels = list(role_counts.keys())
    role_values = list(role_counts.values())

    # Реєстрація користувачів за роками
    registration_years = [user.created_at.year for user in users]
    year_counts = Counter(registration_years)
    years = sorted(year_counts.keys())
    registration_counts_by_year = [year_counts[year] for year in years]

    # Реєстрація користувачів за днями тижня
    registration_days = [user.created_at.weekday() for user in users]
    day_counts = Counter(registration_days)
    day_names = list(calendar.day_name)
    registration_counts_by_day = [day_counts[i] for i in range(7)]

    return render(request, 'authentication/analytics_dashboard.html', {
        'role_labels': role_labels,
        'role_values': role_values,
        'years': years,
        'registration_counts_by_year': registration_counts_by_year,
        'day_names': day_names,
        'registration_counts_by_day': registration_counts_by_day,
    })


@login_required
def user_profile(request):
    # Отримуємо дані для всіх трьох графіків
    users = CustomUser.objects.all()

    # Розподіл ролей користувачів
    roles = [user.get_role_name() for user in users]
    role_counts = Counter(roles)
    role_labels = list(role_counts.keys())
    role_values = list(role_counts.values())

    # Реєстрація користувачів за роками
    registration_years = [user.created_at.year for user in users]
    year_counts = Counter(registration_years)
    years = sorted(year_counts.keys())
    registration_counts_by_year = [year_counts[year] for year in years]

    # Реєстрація користувачів за днями тижня
    registration_days = [user.created_at.weekday() for user in users]
    day_counts = Counter(registration_days)
    day_names = list(calendar.day_name)
    registration_counts_by_day = [day_counts[i] for i in range(7)]

    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileEditForm(instance=user)
    user_data = user.get_user_data()
    return render(request, 'authentication/user_profile.html', {
        'user_data': user_data,
        'profile_edit_form': form,
        'role_labels': role_labels,
        'role_values': role_values,
        'years': years,
        'registration_counts_by_year': registration_counts_by_year,
        'day_names': day_names,
        'registration_counts_by_day': registration_counts_by_day,
    })


