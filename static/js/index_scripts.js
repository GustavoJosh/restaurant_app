// Add functionality to the period buttons for the daily sales chart
document.addEventListener('DOMContentLoaded', function() {
    // Get the period buttons
    const periodButtons = document.querySelectorAll('[data-period]');
    
    // Add click event listeners to each button
    periodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const period = this.getAttribute('data-period');
            updateDailySalesChart(period);
            
            // Highlight the active button
            periodButtons.forEach(btn => btn.classList.remove('bg-yellow-500', 'text-white'));
            this.classList.add('bg-yellow-500', 'text-white');
        });
    });
    
    // If there are period buttons on the page, make sure to add the data-period attributes
    // Example implementation:
    // <button data-period="7" class="px-3 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300">7 Días</button>
    // <button data-period="30" class="px-3 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300">30 Días</button>
    // <button data-period="365" class="px-3 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300">Este Año</button>
});


// Improved initialization code
document.addEventListener('DOMContentLoaded', function() {
    // Add error handling to each chart initialization
    Promise.allSettled([
        fetchIngredientStock(),
        fetchPeakHours(),
        fetchBestSellers(),
        fetchSalesReport(),
        fetchRecentOrders(),
        updateDashboardSummary()
    ]).then(results => {
        // Check results of each initialization task
        results.forEach((result, index) => {
            if (result.status === 'rejected') {
                const functions = ['Ingredient Stock', 'Peak Hours', 'Best Sellers', 'Sales Report', 'Recent Orders', 'Dashboard Summary'];
                console.error(`Failed to initialize ${functions[index]}: ${result.reason}`);
            }
        });
        
        // Hook up the period buttons for daily sales chart
        const periodButtons = document.querySelectorAll('.px-3.py-1.text-xs.bg-gray-200.rounded');
        
        // Add data-period attributes if they don't exist
        if (periodButtons.length === 3) {
            const periods = [7, 30, 365];
            periodButtons.forEach((button, index) => {
                if (!button.hasAttribute('data-period')) {
                    button.setAttribute('data-period', periods[index]);
                }
                
                // Add click event listener
                button.addEventListener('click', function() {
                    const period = this.getAttribute('data-period');
                    updateDailySalesChart(period);
                    
                    // Highlight active button
                    periodButtons.forEach(btn => {
                        btn.classList.remove('bg-yellow-500', 'text-white');
                        btn.classList.add('bg-gray-200');
                    });
                    this.classList.remove('bg-gray-200');
                    this.classList.add('bg-yellow-500', 'text-white');
                });
            });
            
            // Set the first button (7 days) as active by default
            periodButtons[0].click();
        }
    });
});

// Add keyboard shortcut for toggling debug panel (Ctrl+Shift+D)
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.shiftKey && event.key === 'D') {
        event.preventDefault();
        toggleDebugMode();
    }
});
