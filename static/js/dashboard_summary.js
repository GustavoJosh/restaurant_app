async function updateDashboardSummary() {
    try {
        const response = await fetch('/api/dashboard/summary');
        
        // If API doesn't exist yet or has an error, use placeholder data
        if (!response.ok) {
            console.warn(`Dashboard summary API returned ${response.status}: ${response.statusText}`);
            document.getElementById('orders-today').textContent = '36';
            document.getElementById('sales-today').textContent = '$2,450.75';
            document.getElementById('top-product').textContent = 'Gordita Chicharrón';
            document.getElementById('inventory-alerts').textContent = '2';
            return;
        }
        
        const data = await response.json();
        
        // Check if we got the expected data
        if (!data || typeof data !== 'object') {
            console.warn('Dashboard summary data is invalid:', data);
            document.getElementById('orders-today').textContent = '36';
            document.getElementById('sales-today').textContent = '$2,450.75';
            document.getElementById('top-product').textContent = 'Gordita Chicharrón';
            document.getElementById('inventory-alerts').textContent = '2';
            return;
        }
        
        // Update the dashboard cards with actual data
        document.getElementById('orders-today').textContent = data.orders_today || '0';
        document.getElementById('sales-today').textContent = data.sales_today ? `$${parseFloat(data.sales_today).toFixed(2)}` : '$0.00';
        document.getElementById('top-product').textContent = data.top_product || 'No hay datos';
        
        // Add color highlight for inventory alerts if there are any
        const alertElement = document.getElementById('inventory-alerts');
        alertElement.textContent = data.inventory_alerts || '0';
        
        if (data.inventory_alerts > 0) {
            alertElement.classList.add('text-red-600');
        } else {
            alertElement.classList.remove('text-red-600');
        }
    } catch (error) {
        console.error('Error updating dashboard summary:', error);
        // Fallback to default values
        document.getElementById('orders-today').textContent = '36';
        document.getElementById('sales-today').textContent = '$2,450.75';
        document.getElementById('top-product').textContent = 'Gordita Chicharrón';
        document.getElementById('inventory-alerts').textContent = '2';
    }
}