document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('ventasPortafolioChart').getContext('2d');

    const chartData = JSON.parse('{{ datos_grafico|safe }}');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Ventas ($)',
                data: chartData.data,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});