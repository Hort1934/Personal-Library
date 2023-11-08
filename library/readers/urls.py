from django.urls import path
from . import views

app_name = 'readers'

urlpatterns = [
    path('list/', views.reader_list, name='list'),
    # path('detail/<int:reader_id>/', views.reader_detail, name='detail'),
    # Інші URL-шляхи вашого додатку.
]
