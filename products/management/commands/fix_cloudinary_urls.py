from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Fix products that have incorrect Cloudinary URLs"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        fixed_count = 0

        for product in products:
            if product.image and "faulora-farm.onrender.com/https%3A" in product.image.url:
                # Extract the real Cloudinary URL
                corrected_url = product.image.url.split("https%3A/")[-1].replace("%2F", "/")
                product.image = f"https://{corrected_url}"
                product.save()
                self.stdout.write(self.style.SUCCESS(f"Fixed {product.name}"))
                fixed_count += 1

        self.stdout.write(self.style.SUCCESS(f"Done! Fixed {fixed_count} products."))
