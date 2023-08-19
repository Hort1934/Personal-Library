# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Book, CustomUser
from django.http import HttpResponseNotFound
from .forms import OrderForm


def all_orders(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'visitor':
        orders = Order.objects.all()
        orders.status = 'Open'
        return render(request, 'order/all_orders.html', {'orders': orders})
    else:
        return HttpResponseNotFound("page not found")


def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'order/my_orders.html', {'orders': orders})


def create_order(request):
    user = request.user
    if user and user.is_authenticated and user.get_role_name() == 'visitor':
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = user
                order.save()
                return redirect('my_orders')
        else:
            form = OrderForm()
        return render(request, 'order/create_order.html', {'form': form})
    else:
        return HttpResponseNotFound("page not found")


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
        return HttpResponseNotFound("page not found")


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
    # Perform the deletion logic here
    order.delete()
    return redirect('all_orders')


