import os
import django
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolve_project.settings')
django.setup()

from main.models import Product

# Path to your images
media_path = os.path.join(os.path.dirname(__file__), 'media', 'products')

print(f"Looking in: {media_path}")
print("-" * 50)

# Get all products
products = Product.objects.all()
print(f"Found {products.count()} products")
print("=" * 50)

for product in products:
    print(f"Product: {product.name}")
    
    if product.image:
        # For CloudinaryField, we need to check differently
        print(f"  Has Cloudinary image: {product.image}")
        print(f"  Public ID: {product.image.public_id}")
        
        # Try to find local file based on product name or ID
        # Look for common image extensions
        possible_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            # Try product name
            test_file = os.path.join(media_path, f"{product.name}{ext}")
            if os.path.exists(test_file):
                possible_files.append(test_file)
            
            # Try product ID
            test_file = os.path.join(media_path, f"{product.id}{ext}")
            if os.path.exists(test_file):
                possible_files.append(test_file)
        
        if possible_files:
            print(f"  ✅ Found local files: {possible_files}")
        else:
            print(f"  ❌ No local file found for this product")
    else:
        print(f"  No image")
    
    print("-" * 30)