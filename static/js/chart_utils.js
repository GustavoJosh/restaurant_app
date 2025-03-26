function renderMockSalesChart() {
    const dates = [];
    const sales = [];
    
    // Generate last 30 days of data
    const today = new Date();
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        dates.push(date.toLocaleDateString('es-MX'));
        
        // More sales on weekends (0 = Sunday, 6 = Saturday)
        const dayOfWeek = date.getDay();
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            sales.push(Math.floor(Math.random() * 1000) + 4000); // 4000-5000
        } else if (dayOfWeek === 5) { // Friday
            sales.push(Math.floor(Math.random() * 1000) + 3500); // 3500-4500
        } else {
            sales.push(Math.floor(Math.random() * 1000) + 2500); // 2500-3500
        }
    }
    
    const ctx = document.getElementById('dailySalesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Ingresos ($)',
                data: sales,
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

function renderMockBestSellersChart() {
    const products = [
        'Gordita Chicharrón', 
        'Gordita Deshebrada', 
        'Gordita Queso', 
        'Gordita Picadillo', 
        'Gordita Frijol'
    ];
    
    const sales = [
        Math.floor(Math.random() * 50) + 100, // 100-150
        Math.floor(Math.random() * 40) + 80,  // 80-120
        Math.floor(Math.random() * 30) + 70,  // 70-100
        Math.floor(Math.random() * 30) + 50,  // 50-80
        Math.floor(Math.random() * 20) + 40   // 40-60
    ];
    
    const ctx = document.getElementById('bestSellersChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: products,
            datasets: [{
                label: 'Unidades Vendidas',
                data: sales,
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
}


function renderMockPeakHoursChart() {
    const hours = [];
    const counts = [];
    
    // Generate mock data with a peak during lunch and dinner hours
    for (let i = 0; i < 24; i++) {
        hours.push(`${i.toString().padStart(2, '0')}:00`);
        
        // More orders during lunch (12-14) and dinner (18-20)
        if (i >= 12 && i <= 14) {
            counts.push(Math.floor(Math.random() * 15) + 20); // 20-35 orders
        } else if (i >= 18 && i <= 20) {
            counts.push(Math.floor(Math.random() * 20) + 25); // 25-45 orders
        } else if (i >= 7 && i <= 22) {
            counts.push(Math.floor(Math.random() * 10) + 5); // 5-15 orders
        } else {
            counts.push(Math.floor(Math.random() * 3)); // 0-3 orders (late night)
        }
    }
    
    const ctx = document.getElementById('peakHoursChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hours,
            datasets: [{
                label: 'Órdenes',
                data: counts,
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
}

