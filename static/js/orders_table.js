 // Fetch Recent Orders (New function)
 async function fetchRecentOrders() {
    try {
        const tableBody = document.getElementById('recent-orders-table');
        tableBody.innerHTML = '<tr><td class="py-3 px-4" colspan="6">Cargando órdenes recientes...</td></tr>';
        
        const response = await fetch('/api/orders/recent');
        
        // If endpoint doesn't exist yet, show placeholder data
        if (!response.ok) {
            tableBody.innerHTML = generatePlaceholderOrders();
            return;
        }
        
        const orders = await response.json();
        
        if (orders.length === 0) {
            tableBody.innerHTML = '<tr><td class="py-3 px-4" colspan="6">No hay órdenes recientes</td></tr>';
            return;
        }
        
        let html = '';
        orders.forEach(order => {
            html += `
            <tr class="hover:bg-gray-50 text-sm">
                <td class="py-3 px-4">#${order.id}</td>
                <td class="py-3 px-4">${order.table}</td>
                <td class="py-3 px-4">${formatTime(order.created_at)}</td>
                <td class="py-3 px-4">$${order.total.toFixed(2)}</td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 rounded-full text-xs ${getStatusColor(order.status)}">
                        ${capitalizeFirstLetter(order.status)}
                    </span>
                </td>
                <td class="py-3 px-4">
                    <button class="text-blue-500 hover:text-blue-700 mr-2">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
            `;
        });
        
        tableBody.innerHTML = html;
    } catch (error) {
        console.error('Error fetching recent orders:', error);
        document.getElementById('recent-orders-table').innerHTML = 
            '<tr><td class="py-3 px-4 text-red-500" colspan="6">Error al cargar órdenes recientes</td></tr>';
    }
}

// Helper functions
function generatePlaceholderOrders() {
    return `
        <tr class="hover:bg-gray-50 text-sm">
            <td class="py-3 px-4">#1025</td>
            <td class="py-3 px-4">4</td>
            <td class="py-3 px-4">Hace 10 minutos</td>
            <td class="py-3 px-4">$125.50</td>
            <td class="py-3 px-4">
                <span class="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                    Completado
                </span>
            </td>
            <td class="py-3 px-4">
                <button class="text-blue-500 hover:text-blue-700 mr-2">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        </tr>
    `;
}

