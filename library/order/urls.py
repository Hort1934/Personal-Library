from django.urls import path
from . import views

urlpatterns = [
    path('all_orders/', views.all_orders, name='all_orders'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('close_order/<int:order_id>/', views.close_order, name='close_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
