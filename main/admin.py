from django.contrib import admin
from .models import Product, CoachBooking, ContactMessage, ChatMessage  # Add ChatMessage here

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('available', 'category', 'created_at')
    list_editable = ('price', 'stock', 'available')

@admin.register(CoachBooking)
class CoachBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'status', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('status', 'date')
    list_editable = ('status',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'created_at')
    search_fields = ('message', 'response')
    list_filter = ('created_at',)
    readonly_fields = ('message', 'response', 'created_at')