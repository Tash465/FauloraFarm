from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit', 'available', 'featured', 'stock_quantity', 'date_added', 'image_tag')
    list_filter = ('category', 'available', 'featured')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'price', 'unit', 'stock_quantity', 'image', 'available', 'featured')
        }),
        ('Date Info', {
            'fields': ('date_added',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('date_added',)

    # Display a thumbnail in the admin
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'
