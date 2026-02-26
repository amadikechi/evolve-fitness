from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('book-coach/', views.book_coach, name='book_coach'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # AI Chat URLs
    path('chat/', views.chat_page, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    
    # Debug
    path('debug/', views.debug_images, name='debug'),
]