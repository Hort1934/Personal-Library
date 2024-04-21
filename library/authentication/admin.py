from django.contrib import admin
from book.models import Book
from author.models import Author
from order.models import Order
from .models import CustomUser

# Змінюємо назву Django Admin Panel на ваш варіант
admin.site.site_header = "Book collection management system"
admin.site.index_title = "Welcome to my Book collection management system"
admin.site.site_title = "Admin panel of Book collection management system"


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'date_of_issue', 'link']
    search_fields = ['name', 'description']
    list_filter = ['date_of_issue']
    actions = ['export_books']

    def export_books(self, request, queryset):
        import csv
        from django.http import HttpResponse
        import datetime

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="books_{datetime.date.today()}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Date of Issue', 'Link'])

        for book in queryset:
            writer.writerow([book.name, book.description, book.date_of_issue, book.link])

        return response

    export_books.short_description = "Export selected books as CSV"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'created_at', 'end_at', 'plated_end_at')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')
    readonly_fields = ('id',)


from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )
    ordering = ['email']



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)
