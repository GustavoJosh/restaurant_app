function toggleDebugMode() {
    // Create debug panel if it doesn't exist
    if (!document.getElementById('debug-panel')) {
        const debugPanel = document.createElement('div');
        debugPanel.id = 'debug-panel';
        debugPanel.className = 'fixed bottom-0 left-0 right-0 bg-gray-800 text-white p-4 z-50 max-h-64 overflow-y-auto';
        debugPanel.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <h3 class="font-bold">Debug Panel</h3>
                <button id="close-debug" class="text-white bg-red-500 rounded px-2">×</button>
            </div>
            <div id="debug-log" class="text-xs font-mono"></div>
            <div class="mt-2 space-x-2">
                <button id="check-apis" class="bg-blue-500 text-white px-2 py-1 rounded text-xs">Check APIs</button>
                <button id="retry-all" class="bg-green-500 text-white px-2 py-1 rounded text-xs">Retry All</button>
                <button id="force-mock" class="bg-yellow-500 text-white px-2 py-1 rounded text-xs">Use Mock Data</button>
            </div>
        `;
        document.body.appendChild(debugPanel);
        
        // Add event listeners to debug buttons
        document.getElementById('close-debug').addEventListener('click', toggleDebugMode);
        document.getElementById('check-apis').addEventListener('click', debugAPIEndpoints);
        document.getElementById('retry-all').addEventListener('click', () => {
            fetchIngredientStock();
            fetchPeakHours();
            fetchBestSellers();
            fetchSalesReport();
            fetchRecentOrders();
            updateDashboardSummary();
        });
        document.getElementById('force-mock').addEventListener('click', () => {
            renderMockPeakHoursChart();
            renderMockBestSellersChart();
            renderMockSalesChart();
            
            // Also update the cards with mock data
            document.getElementById('orders-today').textContent = '36';
            document.getElementById('sales-today').textContent = '$2,450.75';
            document.getElementById('top-product').textContent = 'Gordita Chicharrón';
            document.getElementById('inventory-alerts').textContent = '2';
            
            // Mock ingredient stock chart
            const ctx = document.getElementById('ingredientStockChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Masa', 'Chicharrón', 'Deshebrada', 'Queso', 'Picadillo', 'Frijol'],
                    datasets: [{
                        label: 'Nivel (Unidad)',
                        data: [75, 45, 60, 80, 55, 90],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(153, 102, 255, 0.6)',
                            'rgba(255, 159, 64, 0.6)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            
            // Mock recent orders
            document.getElementById('recent-orders-table').innerHTML = generatePlaceholderOrders();
        });
        
        // Override console.log for debug panel
        const originalConsoleLog = console.log;
        const originalConsoleWarn = console.warn;
        const originalConsoleError = console.error;
        
        console.log = function() {
            originalConsoleLog.apply(console, arguments);
            addToDebugLog('LOG', arguments);
        };
        
        console.warn = function() {
            originalConsoleWarn.apply(console, arguments);
            addToDebugLog('WARN', arguments);
        };
        
        console.error = function() {
            originalConsoleError.apply(console, arguments);
            addToDebugLog('ERROR', arguments);
        };
        
        function addToDebugLog(type, args) {
            const debugLog = document.getElementById('debug-log');
            const timestamp = new Date().toISOString().substr(11, 8);
            const message = Array.from(args).map(arg => {
                if (typeof arg === 'object') {
                    try {
                        return JSON.stringify(arg);
                    } catch (e) {
                        return String(arg);
                    }
                }
                return String(arg);
            }).join(' ');
            
            const logItem = document.createElement('div');
            logItem.className = type === 'ERROR' ? 'text-red-400' : (type === 'WARN' ? 'text-yellow-400' : 'text-gray-300');
            logItem.textContent = `[${timestamp}] [${type}] ${message}`;
            debugLog.appendChild(logItem);
            
            // Auto-scroll to bottom
            debugLog.scrollTop = debugLog.scrollHeight;
        }
    } else {
        // Remove debug panel if it exists
        const debugPanel = document.getElementById('debug-panel');
        debugPanel.remove();
        
        // Restore original console methods
        console.log = console._originalLog || console.log;
        console.warn = console._originalWarn || console.warn;
        console.error = console._originalError || console.error;
    }
}
