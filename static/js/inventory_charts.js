async function fetchIngredientStock() {
    try {
        const response = await fetch('/api/ingredients/stock');
        if (!response.ok) {
            console.warn(`Ingredient stock API returned ${response.status}: ${response.statusText}`);
            
            // If API fails, display mock data
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
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
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
            
            return;
        }
        
        const data = await response.json();
        
        if (!data || !data.labels || !data.data) {
            console.warn('Ingredient stock data is invalid:', data);
            throw new Error('Invalid data structure');
        }

        const ctx = document.getElementById('ingredientStockChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Nivel (Unidad)',
                    data: data.data,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
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
    } catch (error) {
        console.error('Error fetching ingredient stock data:', error);
        document.getElementById('ingredientStockChart').parentNode.innerHTML = 
            '<div class="chart-container flex items-center justify-center">' +
            '<div class="text-red-500 text-center">Error al cargar datos de inventario<br>' +
            '<button class="mt-2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600" ' +
            'onclick="fetchIngredientStock()">Reintentar</button></div></div>';
    }
}
