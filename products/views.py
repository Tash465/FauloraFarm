from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Product
from cart.models import Order, OrderItem  # Adjust if these are in another app

# ---------------- ABOUT ----------------
def about(request):
    """Display the About Us page."""
    return render(request, 'about.html')


# ---------------- HOME / FEATURED ----------------
def home(request):
    """Display 2 seasonal featured products on homepage."""
    featured_products = Product.objects.filter(available=True, featured=True)[:2]
    return render(request, 'home.html', {'featured_products': featured_products})


# ---------------- PRODUCTS ----------------
def product_list(request):
    """Display available products with filtering and pagination."""
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    products = Product.objects.filter(available=True)

    if category:
        products = products.filter(category=category)
    if search_query:
        search_query = search_query.strip()
        if search_query:
            products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = dict(Product.CATEGORY_CHOICES)

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """Display a single product and related items."""
    product = get_object_or_404(Product, pk=pk, available=True)
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


# ---------------- CART ----------------
def get_cart(request):
    """Helper to get cart from session."""
    return request.session.get('cart', {})


def save_cart(request, cart):
    """Helper to save cart to session."""
    request.session['cart'] = cart


def add_to_cart(request, pk):
    """
    Add a product to the cart (supports AJAX and normal POST).
    Returns JSON for AJAX or redirects back for normal requests.
    """
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    try:
        product = get_object_or_404(Product, pk=pk, available=True)
        cart = get_cart(request)
        cart[str(pk)] = cart.get(str(pk), 0) + 1
        save_cart(request, cart)

        total_items = sum(cart.values())

        # Return JSON if AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'product_name': product.name,
                'total_items': total_items
            })

        messages.success(request, f"{product.name} added to cart!")

    except Exception:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Could not add item to cart.'})
        messages.error(request, "Error adding item to cart.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_cart(request, pk):
    """Remove a product completely from the cart."""
    try:
        cart = get_cart(request)
        if str(pk) in cart:
            del cart[str(pk)]
            save_cart(request, cart)
            messages.info(request, "Item removed from cart.")
        else:
            messages.warning(request, "Item not found in cart.")
    except Exception:
        messages.error(request, "Error removing item from cart.")
    return redirect('cart:cart_detail')


def update_cart(request, pk):
    """Update quantity of a product in the cart."""
    try:
        cart = get_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        if str(pk) in cart:
            if quantity > 0:
                cart[str(pk)] = quantity
                messages.success(request, "Cart updated successfully.")
            else:
                del cart[str(pk)]
                messages.info(request, "Item removed from cart.")
            save_cart(request, cart)
        else:
            messages.warning(request, "Item not found in cart.")
    except ValueError:
        messages.error(request, "Invalid quantity. Please enter a number.")
    except Exception:
        messages.error(request, "Error updating cart.")
    return redirect('cart:cart_detail')


def cart(request):
    """Display all products in the shopping cart."""
    cart = get_cart(request)
    cart_items = []
    total = 0

    for pk, qty in cart.items():
        try:
            product = get_object_or_404(Product, pk=pk)
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
        except Exception:
            messages.warning(request, f"Some items in your cart are no longer available.")

    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'cart/cart.html', context)


# ---------------- CHECKOUT ----------------
@login_required(login_url='accounts:login')
def checkout(request):
    """Process checkout and create order items."""
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    cart_items = []
    total = 0
    for pk, qty in cart.items():
        try:
            product = get_object_or_404(Product, pk=pk)
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
        except Exception:
            messages.error(request, "Some items in your cart are invalid.")
            return redirect('cart:cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if not all([full_name, email, phone, address]):
            messages.error(request, "All fields are required.")
            return redirect('cart:checkout')

        try:
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                total_price=total
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
            request.session['cart'] = {}
            messages.success(request, "Order placed successfully!")
            return redirect('cart:thankyou', order_id=order.id)
        except Exception:
            messages.error(request, "Error placing order. Please try again.")

    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'cart/checkout.html', context)


# ---------------- NEWSLETTER ----------------
@require_POST
def newsletter_signup(request):
    """Handle newsletter signup submissions."""
    email = request.POST.get('email')
    if email:
        print(f"New newsletter signup: {email}")
        # Optional: Save to a model here
    return redirect('/')
