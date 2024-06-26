import codecs
import csv
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import MinValueValidator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from authentication.models import CustomUser
from django.urls import reverse
from django.db.models import Count
from .models import Book, User
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Book
from author.models import Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'isbn', 'date_of_issue', 'image', 'author']

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength': '50'}))
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Author', empty_label=None)

    description = forms.CharField(required=True,
                                  widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'css': 'resize:none;'}))
    isbn = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength': '10','minlength': '10'}))
    date_of_issue = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))


@login_required
def all_books(request):
    books = Book.objects.all()
    user_data = request.user.get_user_data()
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

    return render(request, 'book/all_books.html', {'books': books, 'user_data': user_data})


def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/view_book.html', {'book': book})


def filter_books(request):
    name = request.GET.get('name')
    description = request.GET.get('description')
    count_min = request.GET.get('count_min')
    count_max = request.GET.get('count_max')

    # Фільтрація за назвою і описом
    books = Book.objects.all()

    if name:
        books = books.filter(name__icontains=name)

    if description:
        books = books.filter(description__icontains=description)

    # Фільтрація за кількістю книг
    if count_min is not None and count_max is not None:
        try:
            count_min = int(count_min)
            count_max = int(count_max)
            books = books.filter(count__range=(count_min, count_max))
        except ValueError:
            messages.error(request, "Invalid count range. Please enter valid numeric values.")

    return render(request, 'book/filter_books.html', {'books': books})


def user_books(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    books = user.books.all()
    return render(request, 'book/user_books.html', {'user': user, 'books': books})


from django.shortcuts import get_object_or_404


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем форму, но пока без сохранения в базу данных
            book_instance = form.save(commit=False)

            # Теперь сохраняем книгу в базу данных
            book_instance.save()

            # Получаем ID сохраненной книги
            book_id = book_instance.id

            # Проверяем, есть ли выбранный автор в форме
            if 'author' in request.POST:
                author_id = request.POST['author']
                author = get_object_or_404(Author, pk=author_id)
                book_instance.authors.add(author)  # Добавляем автора к книге

            return redirect('all_books')
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book_instance = form.save(commit=False)
            # Перевіряємо, чи завантажено нове зображення
            if 'image' in request.FILES:
                # Обробляємо та зберігаємо нове зображення
                handle_uploaded_image(request.FILES['image'], book_instance)
            book_instance.save()
            return redirect('view_book', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form, 'book': book})


def handle_uploaded_image(image, book_instance):
    # Визначте шлях, куди зберегти зображення
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', image.name)
    with open(image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    book_instance.image = os.path.join('images', image.name)


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        success_message = f'<div size="5" css="color: white">Book "{book.name}" has been deleted.</div>'
        messages.success(request, mark_safe(success_message))
        return HttpResponseRedirect(reverse('all_books'))

    return render(request, 'book/delete_book.html', {'book': book})


def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)

    # Отримання значень вибраних колонок з форми
    export_id = request.GET.get('export_id') == 'on'
    export_name = request.GET.get('export_name') == 'on'
    export_description = request.GET.get('export_description') == 'on'
    export_count = request.GET.get('export_count') == 'on'
    export_date_of_issue = request.GET.get('export_date_of_issue') == 'on'

    # Запис колонок в CSV-файл відповідно до вибору користувача
    header = []
    if export_id:
        header.append('ID')
    if export_name:
        header.append('Name')
    if export_description:
        header.append('Description')
    if export_count:
        header.append('Count')
    if export_date_of_issue:
        header.append('Date of Issue')

    writer.writerow(header)

    books = Book.objects.all()
    for book in books:
        row = []
        if export_id:
            row.append(book.id)
        if export_name:
            row.append(book.name)
        if export_description:
            row.append(book.description)
        if export_count:
            row.append(book.count)
        if export_date_of_issue:
            row.append(book.date_of_issue)

        writer.writerow(row)

    return response


def analytics(request):
    # Аналітика користувачів
    total_users = User.objects.count()

    # Аналітика книг
    total_books = Book.objects.count()

    # Аналітика інтеракцій
    books_per_user = {user.name: user.get_all_books().count() for user in User.objects.all()}
    popular_books = Book.objects.order_by('-count')[:5]

    # Темпоральна аналітика
    # Припустимо, що у книги є поле `date_of_issue`
    books_issued_by_month = Book.objects.extra({'month': "EXTRACT(month FROM date_of_issue)"}).values('month').annotate(
        total=Count('id'))

    context = {
        'total_users': total_users,
        'total_books': total_books,
        'books_per_user': books_per_user,
        'popular_books': popular_books,
        'books_issued_by_month': books_issued_by_month,
    }
    return render(request, 'book/analytics.html', context)
