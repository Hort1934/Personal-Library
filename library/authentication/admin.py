from django.contrib import admin
from book.models import Book
from author.models import Author
from order.models import Order
from .models import CustomUser


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_of_issue', 'isbn')  # Добавляем 'isbn' в список отображаемых полей
    list_filter = ('date_of_issue',)  # Добавляем фильтр по дате выпуска
    search_fields = ('name', 'description', 'isbn')  # Добавляем поля поиска по имени, описанию и ISBN
    fieldsets = (
        ('Information', {
            'fields': ('name', 'description', 'date_of_issue', 'isbn', 'image', 'authors')  # Добавляем 'image' и 'isbn'
        }),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'created_at', 'end_at', 'plated_end_at')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')
    readonly_fields = ('id',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser)
admin.site.register(Order, OrderAdmin)
