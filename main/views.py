from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CoachBooking, ContactMessage
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, CoachBooking, ContactMessage, ChatMessage
def home(request):
    # Get products by category for the homepage
    supplements = Product.objects.filter(category='supplements', available=True)[:4]
    activewear_male = Product.objects.filter(category='activewear_male', available=True)[:4]
    activewear_female = Product.objects.filter(category='activewear_female', available=True)[:4]
    equipment = Product.objects.filter(category='equipment', available=True)[:4]
    meal_plans = Product.objects.filter(category='meal_plan', available=True)[:4]
    
    # Slideshow content with better styling
    slides = [
        {
            'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48',
            'title': 'ELEVATE YOUR <span style="color: #2ecc71;">PERFORMANCE</span>',
            'description': 'Premium active wear engineered for champions. Experience the difference.',
            'button_text': 'Shop Men\'s Collection',
            'button_link': '/products/?category=activewear_male'
        },
        {
            'image': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2',
            'title': 'STRENGTH MEETS <span style="color: #2ecc71;">STYLE</span>',
            'description': 'Discover our women\'s collection - where comfort meets fashion.',
            'button_text': 'Shop Women\'s Collection',
            'button_link': '/products/?category=activewear_female'
        },
        {
            'image': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f',
            'title': 'FUEL YOUR <span style="color: #2ecc71;">FITNESS</span>',
            'description': 'Premium supplements and meal plans for optimal results.',
            'button_text': 'Explore Supplements',
            'button_link': '/products/?category=supplements'
        },
    ]
    
    context = {
        'supplements': supplements,
        'activewear_male': activewear_male,
        'activewear_female': activewear_female,
        'equipment': equipment,
        'meal_plans': meal_plans,
        'slides': slides,
    }
    return render(request, 'main/home.html', context)

def product_list(request):
    category = request.GET.get('category', '')
    if category:
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)
    
    context = {
        'products': products,
        'current_category': category,
    }
    return render(request, 'main/product_list.html', context)

def book_coach(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')
        
        booking = CoachBooking(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            message=message
        )
        booking.save()
        
        messages.success(request, 'Booking request sent successfully! We will contact you soon.')
        return redirect('book_coach')
    
    return render(request, 'main/book_coach.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        contact.save()
        
        messages.success(request, 'Message sent successfully! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'main/contact.html')

# ========== AUTHENTICATION VIEWS ==========

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('signup')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Log the user in
        login(request, user)
        messages.success(request, f'Welcome {username}! You have successfully signed up.')
        return redirect('dashboard')
    
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    # Get user's bookings
    user_bookings = CoachBooking.objects.filter(email=request.user.email).order_by('-created_at')
    
    # Get user's contact messages
    user_messages = ContactMessage.objects.filter(email=request.user.email).order_by('-created_at')
    
    context = {
        'user_bookings': user_bookings,
        'user_messages': user_messages,
    }
    return render(request, 'main/dashboard.html', context)

def debug_images(request):
    html = "<h1>Debug Images</h1>"
    for product in Product.objects.all():
        html += f"<div style='border:1px solid black; margin:10px; padding:10px;'>"
        html += f"<h2>{product.name}</h2>"
        html += f"<p>Price: ${product.price}</p>"
        html += f"<p>Category: {product.category}</p>"
        html += f"<p>Image field: {product.image}</p>"
        if product.image:
            html += f"<p>Image URL: {product.image.url}</p>"
            html += f"<img src='{product.image.url}' style='max-width:200px;'>"
        else:
            html += "<p style='color:red;'>No image</p>"
        html += "</div>"
    return HttpResponse(html)

# ========== AI CHAT ASSISTANT VIEWS ==========

def get_ai_response(message):
    """Simple AI response function - you can replace with real AI API"""
    
    # Convert message to lowercase for matching
    msg = message.lower()
    
    # Simple rule-based responses (for demo)
    if any(word in msg for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your Evolve Fitness Assistant. How can I help you today?"
    
    elif any(word in msg for word in ['product', 'shop', 'buy']):
        return "We have premium active wear, supplements, and gym equipment! Check our Products page."
    
    elif any(word in msg for word in ['workout', 'exercise', 'train']):
        return "I can help with workouts! What's your goal? (weight loss, muscle gain, general fitness)"
    
    elif any(word in msg for word in ['weight loss', 'lose weight', 'fat loss']):
        return "For weight loss, try: 1) Cardio 3-4x/week 2) Strength training 2-3x/week 3) Calorie deficit diet 4) Stay hydrated! Would you like a sample plan?"
    
    elif any(word in msg for word in ['muscle', 'gain', 'build']):
        return "For muscle building: 1) Lift heavy 3-4x/week 2) Eat protein-rich foods 3) Get enough sleep 4) Progressive overload. Want specific exercises?"
    
    elif any(word in msg for word in ['diet', 'food', 'eat', 'nutrition']):
        return "Good nutrition is key! Focus on: lean proteins, complex carbs, healthy fats, and veggies. Stay away from processed foods. Need meal ideas?"
    
    elif any(word in msg for word in ['supplement', 'protein', 'creatine']):
        return "We have premium supplements! Protein powder, creatine, pre-workout, and more. Check our Supplements category!"
    
    elif any(word in msg for word in ['coach', 'trainer', 'personal training']):
        return "We have expert coaches! You can book a session through our 'Book Coach' page. They'll create personalized plans for you!"
    
    elif any(word in msg for word in ['price', 'cost', 'how much']):
        return "Our products range from $20-$200. Check our Products page for specific prices!"
    
    elif any(word in msg for word in ['contact', 'support', 'help']):
        return "You can reach us at info@evolvefitness.com or WhatsApp +234 816 288 7359"
    
    else:
        return "I'm not sure about that. Could you ask about our products, workouts, nutrition, or coaching? Or visit our Contact page for more help!"

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get AI response
            ai_response = get_ai_response(user_message)
            
            # Save to database if user is logged in
            if request.user.is_authenticated:
                ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=ai_response
                )
            
            return JsonResponse({
                'response': ai_response,
                'user': request.user.username if request.user.is_authenticated else 'Guest'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def chat_page(request):
    # Get chat history for logged in users
    chat_history = []
    if request.user.is_authenticated:
        chat_history = ChatMessage.objects.filter(user=request.user)[:10]
    
    context = {
        'chat_history': chat_history
    }
    return render(request, 'main/chat.html', context)