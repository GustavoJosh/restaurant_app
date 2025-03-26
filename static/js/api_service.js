function debugAPIEndpoints() {
    const apiEndpoints = [
        '/api/dashboard/summary',
        '/api/ingredients/stock',
        '/api/orders/peak_hours',
        '/api/orders/recent',
        '/api/sales_report'
    ];
    
    console.log('Starting API endpoints debug check...');
    
    apiEndpoints.forEach(async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            console.log(`API Endpoint ${endpoint}: Status ${response.status} ${response.statusText}`);
            
            if (response.ok) {
                const data = await response.json();
                console.log(`API Endpoint ${endpoint}: Data structure`, data);
            }
        } catch (error) {
            console.error(`API Endpoint ${endpoint}: Error`, error);
        }
    });
}
