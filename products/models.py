from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('field_crops', 'Field Crops'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('herbs_spices', 'Herbs & Spices'),
        ('dairy', 'Dairy Products'),
        ('eggs', 'Eggs'),
        ('meat', 'Meat'),
    ]

    UNIT_CHOICES = [
        ('kg', 'per kilogram'),
        ('g', 'per gram'),
        ('bunch', 'per bunch'),
        ('pack', 'per pack'),
        ('piece', 'per piece'),
        ('ml', 'per millilitre'),
        ('litre', 'per litre'),
        ('dozen', 'per dozen'),
        ('crate', 'per crate'),
        ('packet', 'per packet'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Enter price in Kenyan Shillings (KES)"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Available stock quantity (kg, pieces, litres, etc.)"
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # Featured flag for seasonal or special products
    featured = models.BooleanField(default=False, help_text="Tick to display this product in the featured section on the homepage")

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
