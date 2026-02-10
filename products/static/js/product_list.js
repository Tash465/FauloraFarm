document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-input');
    const productCards = document.querySelectorAll('.product-card');
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');

    const cartCountElem = document.querySelector('.cart-dropdown > a'); // Header cart count (e.g., "Cart (3)")
    const cartPreviewElem = document.querySelector('.cart-preview'); // Mini cart preview

    // =========================
    // Helper: Parse initial cart count from header
    // =========================
    function getInitialCartCount() {
        const text = cartCountElem ? cartCountElem.textContent : '';
        const match = text.match(/Cart \$(\d+)\$/);
        return match ? parseInt(match[1], 10) : 0;
    }

    // =========================
    // Helper: Load and display mini cart preview
    // =========================
    function loadCartPreview() {
        // Assuming you have an endpoint that returns cart summary as JSON (e.g., GET to cart detail URL)
        // If not, you'll need to add one in your Django views (e.g., a view that returns cart_items_summary and cart_total_price)
        const cartUrl = '{% url "cart:cart_detail" %}'; // Or a dedicated AJAX endpoint like '{% url "cart:cart_summary" %}'

        fetch(cartUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.cart_items_summary && data.cart_total_price !== undefined) {
                let html = '';
                data.cart_items_summary.forEach(item => {
                    html += `<div>${item.product_name} × ${item.quantity} - KSh ${item.subtotal.toFixed(2)}</div>`;
                });
                html += `<strong>Total: KSh ${data.cart_total_price.toFixed(2)}</strong>`;
                html += `<a href="{% url 'cart:cart_detail' %}" class="view-cart-link">View Full Cart 🛒</a>`;
                cartPreviewElem.innerHTML = html;
            }
        })
        .catch(err => {
            console.error('Error loading cart preview:', err);
        });
    }

    // =========================
    // Load initial cart preview if cart has items
    // =========================
    const initialCount = getInitialCartCount();
    if (initialCount > 0 && cartPreviewElem) {
        loadCartPreview();
    }

    // =========================
    // Client-side search/filter
    // =========================
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = searchInput.value.toLowerCase().trim();
            productCards.forEach(card => {
                const name = card.getAttribute('data-name');
                card.style.display = name.includes(query) ? 'block' : 'none';
            });
        });
    }

    // =========================
    // Add to Cart via AJAX
    // =========================
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const button = form.querySelector('.add-to-cart-btn');
            const originalText = button.innerHTML;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            const url = form.action;

            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            button.disabled = true;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    button.innerHTML = '<i class="fas fa-check"></i> Added!';
                    button.style.background = '#66bb6a';

                    // Update cart count in header
                    if (cartCountElem && data.total_items !== undefined) {
                        const iconHtml = '<i class="fa-solid fa-cart-shopping"></i> ';
                        cartCountElem.innerHTML = `${iconHtml}Cart (${data.total_items})`;
                    }

                    // Update mini cart preview (if your view returns cart_items_summary and cart_total_price)
                    if (cartPreviewElem && data.cart_items_summary && data.cart_total_price !== undefined) {
                        let html = '';
                        data.cart_items_summary.forEach(item => {
                            html += `<div>${item.product_name} × ${item.quantity} - KSh ${item.subtotal.toFixed(2)}</div>`;
                        });
                        html += `<strong>Total: KSh ${data.cart_total_price.toFixed(2)}</strong>`;
                        html += `<a href="{% url 'cart:cart_detail' %}" class="view-cart-link">View Full Cart 🛒</a>`;
                        cartPreviewElem.innerHTML = html;
                    }

                    // Show sliding success message
                    showMessage(`${data.product_name} added to cart!`, 'success');

                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.background = '';
                        button.disabled = false;
                    }, 2000);
                } else {
                    button.innerHTML = '<i class="fas fa-times"></i> Failed!';
                    button.style.background = '#e57373';
                    showMessage(data.error || 'Error adding to cart.', 'error');
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.background = '';
                        button.disabled = false;
                    }, 2000);
                }
            })
            .catch(err => {
                console.error('Error adding to cart:', err);
                button.innerHTML = '<i class="fas fa-times"></i> Error!';
                button.style.background = '#e57373';
                showMessage('Something went wrong. Please try again.', 'error');
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '';
                    button.disabled = false;
                }, 2000);
            });
        });
    });

    // =========================
    // Helper: Show Sliding Message
    // =========================
    function showMessage(message, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message-notification';
        msgDiv.textContent = message;
        msgDiv.style.background = type === 'success' ? '#4caf50' : '#f44336';
        document.body.appendChild(msgDiv);
        setTimeout(() => msgDiv.remove(), 3000);
    }
});
