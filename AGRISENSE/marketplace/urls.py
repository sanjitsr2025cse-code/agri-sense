from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('price_trend/<int:listing_id>/', views.price_trend, name='price_trend'),
    path('contact/<int:listing_id>/', views.contact_seller, name='contact_seller'),
]
