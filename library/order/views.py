from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Book, CustomUser
from django.http import HttpResponseNotFound
from .forms import OrderForm
from django.utils import timezone  # Імпорт бібліотеки для отримання поточного часу


# Оновлення функції all_orders для передачі інформації про користувача
def all_orders(request):
    user = request.user
    user_data = request.user.get_user_data()
    orders = Order.objects.all()
    orders.status = 'Open'
    return render(request, 'order/all_orders.html', {'orders': orders, 'user_data': user_data})


def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'order/my_orders.html', {'orders': orders})


def create_order(request):
    user = request.user
    if user.is_authenticated and user.get_role_name() == 'visitor':
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                if order.book:
                    order.user = user  # Прив'язка до поточного користувача
                    order.created_at = timezone.now()
                    order.status = '1'
                    order.save()

                    # order.book.count -= 1
                    order.book.save()
                    return redirect('my_orders')
                else:
                    form.add_error('book', 'The selected book is not available.')
        else:
            form = OrderForm()
        return render(request, 'order/create_order.html', {'form': form})
    else:
        return render(request, 'order/error.html')


def close_order(request, order_id):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'librarian':
        order = Order.objects.get(id=order_id)
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('all_orders')
        else:
            form = OrderForm(instance=order)
        return render(request, 'order/close_order.html', {'form': form, 'order': order})
    else:
        return render(request, 'author/error.html')


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_orders')
    else:
        form = OrderForm(instance=order)

    return render(request, 'order/edit_order.html', {'form': form, 'order': order})


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    # Виконуємо логіку видалення тут
    order.delete()
    return redirect('all_orders')

from django.shortcuts import render
from .models import Order, Book
from django.db.models import Count

def book_analytics(request):
    # Получение топ-10 книг по популярности
    top_books = Order.objects.values('book_id').annotate(total_orders=Count('book_id')).order_by('-total_orders')[:10]

    # Получение объектов книг для отображения в шаблоне
    top_books_data = []
    for item in top_books:
        book = Book.objects.get(pk=item['book_id'])
        top_books_data.append({'book': book, 'total_orders': item['total_orders']})

    return render(request, 'order/analytics.html', {'top_books_data': top_books_data})


def orders_by_genre(request):
    orders_by_genre = Order.orders_by_genre()
    return render(request, 'order/orders_by_genre.html', {'orders_by_genre': orders_by_genre})