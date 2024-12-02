const StorageManager = {
    getItem: function (key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : [];
        } catch (e) {
            console.warn('localStorage access failed');
            return [];
        }
    },
    setItem: function (key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn('localStorage write failed');
        }
    }
};

document.addEventListener('DOMContentLoaded', function () {
    const activeOrdersContainer = document.getElementById('active-orders-container');
    const orderHistoryContainer = document.getElementById('order-history-container');
    let orders = StorageManager.getItem('orders') || [];
    let dashboardNotifications = StorageManager.getItem('dashboardNotifications') || [];
    let dashboardOrders = StorageManager.getItem('dashboardOrders') || [];

    function renderOrders() {
        // Separate active and received orders
        const activeOrders = orders.filter(order => order.status !== 'Received');
        const receivedOrders = orders.filter(order => order.status === 'Received');

        // Render Active Orders
        activeOrdersContainer.innerHTML = '';
        if (activeOrders.length === 0) {
            activeOrdersContainer.innerHTML = `
                <div class="empty-orders">
                    <h2>No active orders</h2>
                    <p>You don't have any active orders.</p>
                    <a href="{% url 'home' %}" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #f57224; color: white; text-decoration: none; border-radius: 4px;">
                        Continue Shopping
                    </a>
                </div>`;
        } else {
            activeOrders.sort((a, b) => new Date(b.date) - new Date(a.date));
            activeOrders.forEach((order, index) => {
                activeOrdersContainer.innerHTML += createOrderCard(order, index, false);
            });
        }

        // Render Order History
        orderHistoryContainer.innerHTML = '';
        if (receivedOrders.length === 0) {
            orderHistoryContainer.innerHTML = `
                <div class="empty-orders">
                    <h2>No order history</h2>
                    <p>Your completed orders will appear here.</p>
                </div>`;
        } else {
            receivedOrders.sort((a, b) => new Date(b.date) - new Date(a.date));
            receivedOrders.forEach((order, index) => {
                orderHistoryContainer.innerHTML += createOrderCard(order, index, true);
            });
        }

        // Update total orders in localStorage
        StorageManager.setItem('orders', orders);
    }

    function createOrderCard(order, index, isHistoryOrder) {
        return `
            <div class="order-card">
                <div class="order-header">
                    <h3>Order #${order.trackingNumber}</h3>
                    <span class="order-date">${new Date(order.date).toLocaleString()}</span>
                    <span class="order-total">Total: $${order.total.toFixed(2)}</span>
                    <span class="order-status">Status: ${order.status}</span>
                </div>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div class="order-item">
                            <div style="display: flex; align-items: center;">
                                <img src="${item.image}" alt="${item.name}">
                                <span class="item-name">${item.name} (x${item.quantity})</span>
                            </div>
                            <span>$${(item.price * item.quantity).toFixed(2)}</span>
                        </div>`).join('')}
                </div>
                <div class="order-summary">
                    <p>Subtotal: $${order.subtotal.toFixed(2)}</p>
                    <p>Tax: $${order.tax.toFixed(2)}</p>
                </div>
                ${!isHistoryOrder ? `
                <div class="order-actions">
                    <button class="checkout-dashboard-btn" data-index="${index}">Order Received</button>
                    <button class="cancel-order-btn" data-index="${index}">Cancel Order</button>
                </div>` : ''}
            </div>`;
    }

    activeOrdersContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('checkout-dashboard-btn')) {
            const index = e.target.getAttribute('data-index');
            const selectedOrder = orders.find(order => order.status !== 'Received');

            if (selectedOrder.status === 'Received') {
                alert('This order is already marked as received.');
                return;
            }

            // Mark order as received
            selectedOrder.status = 'Received';

            // Create notification
            const notification = {
                trackingNumber: selectedOrder.trackingNumber,
                message: `Order #${selectedOrder.trackingNumber} has been marked as received.`,
                date: new Date().toISOString(),
                read: false
            };

            // Add to dashboard notifications
            dashboardNotifications.push(notification);

            // Ensure order is added to dashboard orders
            dashboardOrders.push(selectedOrder);

            // Update localStorage
            StorageManager.setItem('dashboardNotifications', dashboardNotifications);
            StorageManager.setItem('dashboardOrders', dashboardOrders);

            // Render orders to reflect the change
            renderOrders();

            alert('Order marked as received and notification sent to admin.');
        }

        if (e.target.classList.contains('cancel-order-btn')) {
            const index = e.target.getAttribute('data-index');
            const confirmation = confirm('Are you sure you want to cancel this order?');
            if (confirmation) {
                // Remove the order from the orders list
                orders.splice(index, 1);
                StorageManager.setItem('orders', orders);
                renderOrders();
            }
        }
    });

    renderOrders();
});