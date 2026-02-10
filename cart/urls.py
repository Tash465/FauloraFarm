from django.urls import path
from . import views

app_name = 'cart'   

urlpatterns = [
    path('', views.cart_view, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:key>/', views.update_cart, name='update_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thankyou/<int:order_id>/', views.thankyou, name='thankyou'),

]



