from django.core.management.base import BaseCommand
from products.models import Product
import cloudinary.uploader
import os
from django.conf import settings  # <-- to get BASE_DIR

class Command(BaseCommand):
    help = 'Uploads product images to Cloudinary and updates their URLs'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        total = products.count()
        self.stdout.write(self.style.SUCCESS(f"Found {total} products."))

        for product in products:
            # Skip if already a Cloudinary URL
            if product.image and not str(product.image).startswith('http'):
                # Build full local path from media folder
                local_path = os.path.join(settings.BASE_DIR, 'media', str(product.image))

                if os.path.exists(local_path):
                    self.stdout.write(f"Uploading {product.name}...")
                    try:
                        result = cloudinary.uploader.upload(local_path, folder="faulora_products")
                        product.image = result['secure_url']  # Save Cloudinary URL
                        product.save()
                        self.stdout.write(self.style.SUCCESS(f"Uploaded {product.name} to Cloudinary."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to upload {product.name}: {e}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Local file for {product.name} not found at {local_path}."))
            else:
                self.stdout.write(f"{product.name} already has a Cloudinary URL.")
