from django import forms
from django.contrib import messages
from django.core.validators import MinValueValidator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe

from .models import Book
from authentication.models import CustomUser
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'date_of_issue']

    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    count = forms.IntegerField(required=True, validators=[MinValueValidator(0)])
    date_of_issue = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2051)))

from django.http import Http404


def all_books(request):
    books = Book.objects.all()
    search_id = request.GET.get('id')

    if search_id:
        try:
            book = get_object_or_404(Book, id=search_id)
            return view_book(request, book.id)
        except Http404:
            messages.error(request, "Book not found in the database.")
            return render(request, 'book/all_books.html', {'books': books})

    return render(request, 'book/all_books.html', {'books': books})


def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/view_book.html', {'book': book})


def filter_books(request):
    name = request.GET.get('name')
    description = request.GET.get('description')

    if name and description:
        books = Book.objects.filter(name__icontains=name, description__icontains=description)
    elif name:
        books = Book.objects.filter(name__icontains=name)
    elif description:
        books = Book.objects.filter(description__icontains=description)
    else:
        books = Book.objects.none()  # Return an empty queryset

    return render(request, 'book/filter_books.html', {'books': books})


def user_books(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    books = user.books.all()
    return render(request, 'book/user_books.html', {'user': user, 'books': books})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('view_book', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form, 'book': book})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        success_message = f'<div size="5">Book "{book.name}" has been deleted.</div>'
        messages.success(request, mark_safe(success_message))
        return HttpResponseRedirect(reverse('all_books'))

    return render(request, 'book/delete_book.html', {'book': book})