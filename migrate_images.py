import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolve_project.settings')
django.setup()

from main.models import Product
from django.core.files import File
import os

# Path to your local media folder
media_path = os.path.join(os.path.dirname(__file__), 'media', 'products')

print(f"Looking for images in: {media_path}")

# Loop through all products
for product in Product.objects.all():
    if product.image:
        # Get the filename from the current image field
        filename = os.path.basename(product.image.name)
        local_file_path = os.path.join(media_path, filename)
        
        print(f"Checking: {filename}")
        
        if os.path.exists(local_file_path):
            print(f"✅ Found: {filename} - Uploading to Cloudinary...")
            with open(local_file_path, 'rb') as f:
                product.image.save(filename, File(f), save=True)
            print(f"   Uploaded!")
        else:
            print(f"❌ Not found: {filename}")

print("\n✅ Migration complete!")