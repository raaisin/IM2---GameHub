        
        // Robust Storage Mechanism
        const StorageManager = {
            // Primary storage method
            _storage: {},

            getItem: function(key) {
                try {
                    // Try localStorage first
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : null;
                } catch (e) {
                    // Fallback to in-memory storage
                    console.warn('localStorage access failed, using fallback');
                    return this._storage[key] ? JSON.parse(this._storage[key]) : null;
                }
            },

            setItem: function(key, value) {
                try {
                    // Try localStorage first
                    localStorage.setItem(key, JSON.stringify(value));
                } catch (e) {
                    // Fallback to in-memory storage
                    console.warn('localStorage access failed, using fallback');
                    this._storage[key] = JSON.stringify(value);
                }
            },

            removeItem: function(key) {
                try {
                    localStorage.removeItem(key);
                } catch (e) {
                    delete this._storage[key];
                }
            }
        };

        document.addEventListener('DOMContentLoaded', function() {
            const cartContainer = document.getElementById('cart-container');
            const TAX_RATE = 0.08;

            function renderCart() {
                // Retrieve cart items
                const cartItems = StorageManager.getItem('cartItems') || [];
                
                // Clear previous content
                cartContainer.innerHTML = '';

                // Handle empty cart
                if (cartItems.length === 0) {
                    cartContainer.innerHTML = `
                        <div class="empty-cart">
                            <h2>Your cart is empty</h2>
                            <p>Looks like you haven't added any items to your cart yet.</p>
                            <a href="{% url 'home' %}" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #f57224; color: white; text-decoration: none; border-radius: 4px;">
                                Continue Shopping
                            </a>
                        </div>
                    `;
                    return;
                }

                // Render cart items
                cartItems.forEach((item, index) => {
                    const itemTotal = item.price * item.quantity;
                    const cartItemElement = document.createElement('div');
                    cartItemElement.className = 'cart-item';
                    cartItemElement.innerHTML = `
                        <img src="${item.image}" alt="${item.name}">
                        <div class="item-info">
                            <div>
                                <h3>${item.name}</h3>
                                <p>Price: $${item.price.toFixed(2)}</p>
                                <p>Color: ${item.color}</p>
                            </div>
                            <div class="quantity-control">
                                <button onclick="updateQuantity(${index}, 'decrease')">-</button>
                                <span>${item.quantity}</span>
                                <button onclick="updateQuantity(${index}, 'increase')">+</button>
                            </div>
                            <div>
                                <p>Total: $${itemTotal.toFixed(2)}</p>
                                <button onclick="removeItem(${index})" style="background:none; border:none; color:red; cursor:pointer;">Remove</button>
                            </div>
                        </div>
                    `;
                    cartContainer.appendChild(cartItemElement);
                });

                // Render cart summary
                renderCartSummary(cartItems);
            }

            function renderCartSummary(cartItems) {
                const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                const tax = subtotal * TAX_RATE;
                const total = subtotal + tax;

                const summaryElement = document.createElement('div');
                summaryElement.innerHTML = `
                    <div style="background:white; padding:1rem; margin-top:1rem; border-radius:8px;">
                        <h3>Order Summary</h3>
                        <p>Subtotal: $${subtotal.toFixed(2)}</p>
                        <p>Tax (8%): $${tax.toFixed(2)}</p>
                        <p><strong>Total: $${total.toFixed(2)}</strong></p>
                        <button class="checkout-btn" onclick="processCheckout()">
                            Proceed to Checkout
                        </button>
                    </div>
                `;
                cartContainer.appendChild(summaryElement);
            }

            // Attach to window to make globally accessible
            window.updateQuantity = function(index, action) {
                const cartItems = StorageManager.getItem('cartItems') || [];
                
                if (action === 'increase') {
                    cartItems[index].quantity++;
                } else if (action === 'decrease' && cartItems[index].quantity > 1) {
                    cartItems[index].quantity--;
                }

                StorageManager.setItem('cartItems', cartItems);
                renderCart();
            }

            window.removeItem = function(index) {
                const cartItems = StorageManager.getItem('cartItems') || [];
                cartItems.splice(index, 1);
                StorageManager.setItem('cartItems', cartItems);
                renderCart();
            }

// In carts.html: Enhanced processCheckout function
window.processCheckout = function() {
const cartItems = StorageManager.getItem('cartItems') || [];

if (cartItems.length === 0) {
    alert('Your cart is empty');
    return;
}

const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
const TAX_RATE = 0.08;
const tax = subtotal * TAX_RATE;
const total = subtotal + tax;

// Create a comprehensive order object
const order = {
    id: Date.now(),
    items: cartItems,
    subtotal: subtotal,
    tax: tax,
    total: total,
    date: new Date().toISOString(),
    status: 'pending',
    trackingNumber: `ORD-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
};

// Save order to orders list
const orders = StorageManager.getItem('orders') || [];
orders.push(order);
StorageManager.setItem('orders', orders);

// Also save to dashboard orders
const dashboardOrders = StorageManager.getItem('dashboardOrders') || [];
dashboardOrders.push({...order, dashboardAddedDate: new Date().toISOString()});
StorageManager.setItem('dashboardOrders', dashboardOrders);

// Clear cart
StorageManager.removeItem('cartItems');

// Show success message
const successMessage = document.createElement('div');
successMessage.className = 'success-message';
successMessage.innerHTML = `
    <h2>Order Successful!</h2>
    <p>Your order has been processed.</p>
    <p>Tracking Number: ${order.trackingNumber}</p>
    <p>Total: $${total.toFixed(2)}</p>
    <button onclick="window.location.href='{% url 'orders' %}'" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #f57224; color: white; border: none; border-radius: 4px;">
        View Orders
    </button>
`;
document.body.appendChild(successMessage);

// Redirect after a delay
setTimeout(() => {
    window.location.href = "{% url 'orders' %}";
}, 3000);
}

            // Initial render
            renderCart();
        });

        // Add to cart function (to be used on product pages)
        function addToCart(product) {
            // Retrieve existing cart items
            const cartItems = StorageManager.getItem('cartItems') || [];
            
            // Check if product already exists in cart
            const existingItemIndex = cartItems.findIndex(item => item.name === product.name);
            
            if (existingItemIndex > -1) {
                // Increment quantity if item exists
                cartItems[existingItemIndex].quantity++;
            } else {
                // Add new item with quantity 1
                cartItems.push({...product, quantity: 1});
            }
            
            // Save updated cart
            StorageManager.setItem('cartItems', cartItems);
        }