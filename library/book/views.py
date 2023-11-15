import codecs

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import MinValueValidator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe

from .models import Book
from authentication.models import CustomUser
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'date_of_issue']

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength': '50'}))
    description = forms.CharField(required=True,
                                  widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'style': 'resize:none;'}))
    count = forms.IntegerField(required=True, validators=[MinValueValidator(0)],
                               widget=forms.NumberInput(attrs={'style': 'width: 5em;'}))
    date_of_issue = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))


from django.http import Http404


def all_books(request):
    books = Book.objects.all()
    search_id = request.GET.get('id')

    if search_id:
        try:
            book_id = int(search_id)
            book = get_object_or_404(Book, id=book_id)
            return view_book(request, book.id)
        except (ValueError, Http404):
            messages.error(request, f"Book not found for ID: {search_id}. Please enter a valid numeric ID.")
            return render(request, 'book/all_books.html', {'books': books})

    # Отримання номера сторінки з параметра запиту
    page = request.GET.get('page')
    paginator = Paginator(books, 10)  # Розділити на сторінки по 20 книг на кожній

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # Якщо номер сторінки не є цілим числом, показати першу сторінку.
        books = paginator.page(1)
    except EmptyPage:
        # Якщо номер сторінки за межами доступних сторінок, показати останню сторінку.
        books = paginator.page(paginator.num_pages)

    if not books:
        messages.info(request, "No books available.")

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
        success_message = f'<div size="5" style="color: white">Book "{book.name}" has been deleted.</div>'
        messages.success(request, mark_safe(success_message))
        return HttpResponseRedirect(reverse('all_books'))

    return render(request, 'book/delete_book.html', {'book': book})


import csv
from django.http import HttpResponse


def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Description', 'Count', 'Date of Issue'])

    books = Book.objects.all()
    for book in books:
        writer.writerow([book.id, book.name, book.description, book.count, book.date_of_issue])

    return response
