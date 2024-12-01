document.addEventListener('DOMContentLoaded', function () {
    const notificationIcon = document.getElementById('notification-icon');
    const notificationDropdown = document.getElementById('notification-dropdown');
    const notificationList = document.getElementById('notification-list');
    const notificationBadge = document.getElementById('notification-badge');
    const orderList = document.getElementById('order-list');
    const totalSalesElement = document.getElementById('total-sales');
    const totalOrdersElement = document.getElementById('total-orders');
    const pendingOrdersElement = document.getElementById('pending-orders');
    const generateOrderButton = document.getElementById('generate-order');
    const clearNotificationsButton = document.getElementById('clear-all-notifications');
    const markAllReadButton = document.getElementById('mark-all-read');

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

    function generateTrackingNumber() {
        return 'ORD' + Math.random().toString(36).substr(2, 9).toUpperCase();
    }

    function generateRandomPrice() {
        return Math.floor(Math.random() * 500) + 50;
    }

    let dashboardNotifications = StorageManager.getItem('dashboardNotifications') || [];
    let dashboardOrders = StorageManager.getItem('dashboardOrders') || [];

    function updateNotificationBadge() {
        const unreadNotifications = dashboardNotifications.filter(n => !n.read).length;
        notificationBadge.textContent = unreadNotifications;
    }

    function renderNotifications() {
        notificationList.innerHTML = ''; 
        
        if (dashboardNotifications.length === 0) {
            notificationList.innerHTML = '<li>No new notifications</li>';
        } else {
            const sortedNotifications = dashboardNotifications.sort((a, b) => new Date(b.date) - new Date(a.date));
            sortedNotifications.forEach((notification, index) => {
                const notificationItem = document.createElement('li');
                notificationItem.innerHTML = `
                    <div>
                        <p>${notification.message}</p>
                        <span>${new Date(notification.date).toLocaleString()}</span>
                    </div>
                    ${!notification.read ? `<button class="mark-read-btn" data-index="${index}">Mark Read</button>` : ''}
                `;
                notificationList.appendChild(notificationItem);
            });

            document.querySelectorAll('.mark-read-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const index = this.getAttribute('data-index');
                    dashboardNotifications[index].read = true;
                    StorageManager.setItem('dashboardNotifications', dashboardNotifications);
                    renderNotifications();
                    updateNotificationBadge();
                });
            });
        }
        
        updateNotificationBadge();
    }

    function renderOrders() {
        orderList.innerHTML = ''; 
        
        if (dashboardOrders.length === 0) {
            orderList.innerHTML = '<div class="order-item">No recent orders</div>';
            totalOrdersElement.textContent = '0';
            pendingOrdersElement.textContent = '0';
            totalSalesElement.textContent = '$0.00';
            return;
        }

        const sortedOrders = dashboardOrders.sort((a, b) => new Date(b.date) - new Date(a.date));
        const totalSales = sortedOrders.reduce((total, order) => total + order.total, 0);
        const pendingOrders = sortedOrders.filter(order => !order.delivered).length;

        totalOrdersElement.textContent = sortedOrders.length;
        pendingOrdersElement.textContent = pendingOrders;
        totalSalesElement.textContent = `$${totalSales.toFixed(2)}`;

        sortedOrders.forEach((order, index) => {
            const orderItem = document.createElement('div');
            orderItem.classList.add('order-item');
            orderItem.innerHTML = `
                <span>Order #${order.trackingNumber}</span>
                <span>$${order.total.toFixed(2)}</span>
                <span>${new Date(order.date).toLocaleDateString()}</span>
                ${!order.delivered ? `<button class="mark-delivered-btn" data-index="${index}">Mark Delivered</button>` : '<span>Delivered</span>'}
            `;
            orderList.appendChild(orderItem);
        });

        document.querySelectorAll('.mark-delivered-btn').forEach(button => {
            button.addEventListener('click', function() {
                const index = this.getAttribute('data-index');
                sortedOrders[index].delivered = true;
                dashboardNotifications.push({
                    message: `Order #${sortedOrders[index].trackingNumber} has been delivered`,
                    date: new Date().toISOString(),
                    read: false
                });
                dashboardOrders = sortedOrders;
                StorageManager.setItem('dashboardOrders', dashboardOrders);
                StorageManager.setItem('dashboardNotifications', dashboardNotifications);
                renderOrders();
                renderNotifications();
            });
        });
    }

    notificationIcon.addEventListener('click', function () {
        notificationDropdown.classList.toggle('active');
    });

    document.addEventListener('click', function(event) {
        if (!notificationIcon.contains(event.target) && !notificationDropdown.contains(event.target)) {
            notificationDropdown.classList.remove('active');
        }
    });

    generateOrderButton.addEventListener('click', function() {
        const newOrder = {
            trackingNumber: generateTrackingNumber(),
            total: generateRandomPrice(),
            date: new Date().toISOString(),
            delivered: false
        };

        dashboardOrders.push(newOrder);
        dashboardNotifications.push({
            message: `New order #${newOrder.trackingNumber} received`,
            date: new Date().toISOString(),
            read: false
        });

        StorageManager.setItem('dashboardOrders', dashboardOrders);
        StorageManager.setItem('dashboardNotifications', dashboardNotifications);
        renderOrders();
        renderNotifications();
    });

    clearNotificationsButton.addEventListener('click', function() {
        dashboardNotifications = [];
        StorageManager.setItem('dashboardNotifications', dashboardNotifications);
        renderNotifications();
    });

    markAllReadButton.addEventListener('click', function() {
        dashboardNotifications.forEach(notification => notification.read = true);
        StorageManager.setItem('dashboardNotifications', dashboardNotifications);
        renderNotifications();
    });

    renderOrders();
    renderNotifications();
});