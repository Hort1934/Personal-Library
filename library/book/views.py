from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from authentication.models import CustomUser
from django.http import HttpResponseNotFound


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'date_of_issue']


def all_books(request):
    books = Book.objects.all()
    search_id = request.GET.get('id')

    if search_id:
        book = get_object_or_404(Book, id=search_id)
        return view_book(request, book.id)

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
