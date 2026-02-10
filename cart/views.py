from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

def _get_cart(request):
    """Helper function to get or create a cart in the session."""
    cart = request.session.get('cart', {})
    if not cart:
        request.session['cart'] = {}
    return cart


def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart:cart_detail')



def remove_from_cart(request, key):
    """Remove a product completely from the cart."""
    cart = _get_cart(request)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        messages.info(request, "Item removed from your cart.")
        return redirect('cart:cart_detail')    


def update_cart(request, key):
    """Update quantity of a specific product in the cart."""
    cart = _get_cart(request)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key] = new_quantity
        request.session['cart'] = cart
        messages.success(request, "Cart updated successfully.")
        return redirect('cart:cart_detail')



def clear_cart(request):
    """Completely clear the cart."""
    request.session['cart'] = {}
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart:cart_detail')



def cart_view(request):
    """Display the cart contents."""
    cart = _get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')  # redirect to login if not logged in
def checkout_view(request):
    """Handle checkout form submission and order creation."""
    cart = _get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())

    if not products:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')


    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Create Order
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_price=total_price
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear cart
        request.session['cart'] = {}

        messages.success(request, " Order placed successfully! Thank you for shopping with Faulora Farm .")
        return redirect('cart:thankyou', order_id=order.id)



    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def thankyou(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/thankyou.html', {'order': order})



