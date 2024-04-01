from django.contrib import admin
from book.models import Book
from author.models import Author
from order.models import Order
from .models import CustomUser


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date_of_issue', 'image', 'isbn')
    list_filter = ('id', 'name', 'authors')
    search_fields = ('name', 'authors__name', 'authors__surname')

    fieldsets = (
        ('Fixed Information', {
            'fields': ('name', 'date_of_issue'),
        }),
        ('Variable Information', {
            'fields': ('description', 'count'),
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
