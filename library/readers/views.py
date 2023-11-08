from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Reader

def reader_list(request):
    readers = Reader.objects.all()
    return render(request, 'reader_list.html', {'readers': readers})
