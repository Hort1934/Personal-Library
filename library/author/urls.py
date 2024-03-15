from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_author, name='create_author'),
    path('', views.all_authors, name='all_authors'),
    path('delete/<int:id>', views.delete_author, name='delete_author'),
    path('edit/<int:id>', views.edit_author, name='edit_author'),
]