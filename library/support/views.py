from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse


def support(request):
    user_data = request.user.get_user_data()
    if request.method == 'POST':
        # Обробка форми надсилання запитання
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        email_from = request.POST.get('email', '')
        recipient_list = ['hort19345@gmail.com']

        send_mail(subject, message, email_from, recipient_list)

        # Після надсилання запитання перенаправляємо користувача на сторінку підтримки
        return HttpResponseRedirect(reverse('support'))

    return render(request, 'support.html', {'user_data': user_data})
