from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.create_author, name='create'),
    path('', views.all_authors, name='all_authors'),
    path('delete/<int:id>', views.delete_author, name='delete')
    
]