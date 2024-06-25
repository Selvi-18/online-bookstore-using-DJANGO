from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order, OrderItem
from django.db.models import Q
from django.urls import reverse


def home(request):
    return render(request, 'shope/home.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'shope/book_list.html', {'books': books})

def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'shope/book_list.html', {'books': books})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', [])
    cart.append(book.id)
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'shope/cart_detail.html', {'books': books})

def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart = request.session.get('cart', [])
        books = Book.objects.filter(id__in=cart)
        total_cost = sum(book.price for book in books)
        order = Order.objects.create(total_cost=total_cost, shipping_address=address)
        for book in books:
            OrderItem.objects.create(order=order, book=book, quantity=1)
        request.session['cart'] = []
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'shope/checkout.html')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shope/order_confirmation.html', {'order': order})

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'shope/orders_list.html', {'orders': orders})
