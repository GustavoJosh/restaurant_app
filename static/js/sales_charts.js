async function fetchSalesReport() {
    try {
        const response = await fetch('/api/sales_report');
        if (!response.ok) {
            console.warn(`API endpoint returned ${response.status}: ${response.statusText}`);
            
            // If API not available, show mock data
            renderMockSalesChart();
            return;
        }
        
        const data = await response.json();
        
        if (!data.daily_sales || !Array.isArray(data.daily_sales) || data.daily_sales.length === 0) {
            console.warn('Daily sales data missing or empty:', data);
            renderMockSalesChart();
            return;
        }
        
        // Render actual data
        const ctx = document.getElementById('dailySalesChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.daily_sales.map(d => d.date),
                datasets: [{
                    label: 'Ingresos ($)',
                    data: data.daily_sales.map(d => d.revenue),
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching sales report data:', error);
        renderMockSalesChart();
    }
}

async function updateDailySalesChart(days) {
    try {
        const today = new Date();
        const startDate = new Date();
        startDate.setDate(today.getDate() - days);
        
        // Format dates for API
        const startDateStr = startDate.toISOString().split('T')[0];
        const endDateStr = today.toISOString().split('T')[0];
        
        // Fetch data with date range
        const response = await fetch(`/api/sales_report?start_date=${startDateStr}&end_date=${endDateStr}`);
        
        if (!response.ok) {
            console.warn(`API endpoint returned ${response.status}: ${response.statusText}`);
            return;
        }
        
        const data = await response.json();
        
        if (!data.daily_sales || !Array.isArray(data.daily_sales)) {
            console.warn('Daily sales data missing or empty:', data);
            return;
        }
        
        // Get the chart instance and update it
        const chartInstance = Chart.getChart('dailySalesChart');
        
        if (chartInstance) {
            chartInstance.data.labels = data.daily_sales.map(d => d.date);
            chartInstance.data.datasets[0].data = data.daily_sales.map(d => d.revenue);
            chartInstance.update();
        } else {
            // If chart doesn't exist yet, create it
            const ctx = document.getElementById('dailySalesChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.daily_sales.map(d => d.date),
                    datasets: [{
                        label: 'Ingresos ($)',
                        data: data.daily_sales.map(d => d.revenue),
                        fill: true,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        tension: 0.4,
                        pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error updating sales chart:', error);
    }
}

// Best Sellers Chart
async function fetchBestSellers() {
    try {
        const response = await fetch('/api/sales_report');
        if (!response.ok) {
            console.warn(`API endpoint returned ${response.status}: ${response.statusText}`);
            
            // If API not available, show mock data
            renderMockBestSellersChart();
            return;
        }
        
        const data = await response.json();
        
        if (!data.best_sellers || !Array.isArray(data.best_sellers) || data.best_sellers.length === 0) {
            console.warn('Best sellers data missing or empty:', data);
            renderMockBestSellersChart();
            return;
        }
        
        // Render actual data
        const ctx = document.getElementById('bestSellersChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.best_sellers.map(item => item.name),
                datasets: [{
                    label: 'Unidades Vendidas',
                    data: data.best_sellers.map(item => item.sold),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
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
    } catch (error) {
        console.error('Error fetching best sellers data:', error);
        renderMockBestSellersChart();
    }
}

async function fetchPeakHours() {
    try {
        const response = await fetch('/api/sales_report');
        if (!response.ok) {
            console.warn(`API endpoint returned ${response.status}: ${response.statusText}`);
            // If API not available, show mock data
            renderMockPeakHoursChart();
            return;
        }
        
        const data = await response.json();
        
        // Check if the peak_hours data exists in the sales_report response
        if (!data.peak_hours || !Array.isArray(data.peak_hours) || data.peak_hours.length === 0) {
            console.warn('Peak hours data missing or empty:', data);
            renderMockPeakHoursChart();
            return;
        }
        
        // Sort the hours numerically to ensure proper order
        const sortedHourData = [...data.peak_hours].sort((a, b) => a.hour - b.hour);
        
        // Format the hour labels (add :00 to make it clear they are hours)
        const hourLabels = sortedHourData.map(h => `${h.hour.toString().padStart(2, '0')}:00`);
        
        // Get the order counts
        const orderCounts = sortedHourData.map(h => h.orders);
        
        // Render actual data
        const ctx = document.getElementById('peakHoursChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: hourLabels,
                datasets: [{
                    label: 'Órdenes',
                    data: orderCounts,
                    backgroundColor: 'rgba(255, 159, 64, 0.6)',
                    borderColor: 'rgba(255, 159, 64, 1)',
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
    } catch (error) {
        console.error('Error fetching peak hours data:', error);
        renderMockPeakHoursChart();
    }
}