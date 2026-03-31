from django.urls import path
from . import views
from products.views import create_admin
app_name = 'products'

urlpatterns = [
    # Homepage
    path('home/', views.home, name='home'),
    path('create-admin/', create_admin, name='create_admin'),
    # Product pages
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # Add to cart
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    # Newsletter signup
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),

]
