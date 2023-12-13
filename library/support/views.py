# support/views.py
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse

def support(request):
    if request.method == 'POST':
        # Обработка формы отправки вопроса
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        email_from = request.POST.get('email', '')
        recipient_list = ['hort19345@gmail.com']

        send_mail(subject, message, email_from, recipient_list)

        # После отправки вопроса перенаправляем пользователя на страницу поддержки
        return HttpResponseRedirect(reverse('support'))

    return render(request, 'support.html')
