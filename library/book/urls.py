from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/', views.all_books, name='all_books'),
    path('books/<int:book_id>/', views.view_book, name='view_book'),
    path('books/filter/', views.filter_books, name='filter_books'),
    path('users/<int:user_id>/', views.user_books, name='user_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('export/csv/', views.export_books_csv, name='export_books_csv'),
    path('books/analytics/', views.analytics, name='analytics'),
    # path('export/csv-site/', views.export_books_csv_site, name='export_books_csv_site'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)