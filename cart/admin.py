from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')
    inlines = [OrderItemInline]

    fieldsets = (
        ("Customer Info", {
            "fields": ("full_name", "email", "phone", "address")
        }),
        ("Order Details", {
            "fields": ("total_price", "created_at")
        }),
    )
