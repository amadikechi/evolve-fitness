from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.contrib.auth.models import User  # Add this import for User model

class Product(models.Model):
    # Add category choices
    CATEGORY_CHOICES = [
        ('supplements', 'Supplements'),
        ('activewear_male', 'Active Wear (Male)'),
        ('activewear_female', 'Active Wear (Female)'),
        ('equipment', 'Gym Equipment'),
        ('meal_plan', 'Meal Plans'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='activewear_male')
    image = CloudinaryField('image', blank=True, null=True)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class CoachBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Booking by {self.name} on {self.date}"
    
    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Message from {self.user or 'Guest'} at {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']