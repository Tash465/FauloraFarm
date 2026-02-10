from products.models import Product

def cart_summary(request):
    cart = request.session.get('cart', {})
    items = []
    total_qty = 0
    total_price = 0

    if cart:
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            quantity = cart[str(product.id)]
            subtotal = product.price * quantity
            total_qty += quantity
            total_price += subtotal
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    return {
        'cart_items_summary': items,
        'cart_total_qty': total_qty,
        'cart_total_price': total_price,
    }
