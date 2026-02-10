from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Homepage
    path('home/', views.home, name='home'),

    # Product pages
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # Add to cart
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    # Newsletter signup
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),

]
