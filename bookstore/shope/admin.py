from django.contrib import admin
from .models import Book, Order, OrderItem

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    search_fields = ('title', 'author')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_cost', 'shipping_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('shipping_address',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity')
    list_filter = ('order',)
    search_fields = ('book__title', 'book__author')

