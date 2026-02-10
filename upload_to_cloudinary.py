import os
import cloudinary
import cloudinary.uploader

# Load from environment or fallback to manual config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dhcwh9q6v"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "131213486265151"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "Ok9t2ycWlqcv86uRt4iytOsYbRY")
)

# Directory containing your images
upload_dir = "media/products"  # adjust path if needed

for filename in os.listdir(upload_dir):
    file_path = os.path.join(upload_dir, filename)
    if os.path.isfile(file_path):
        print(f"Uploading {filename}...")
        try:
            response = cloudinary.uploader.upload(file_path)
            print(f"Uploaded: {response['secure_url']}")
        except Exception as e:
            print(f"Error uploading {filename}: {e}")
