// Inicializar los gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráfico de ventas
    const ventasContainer = document.getElementById('ventasChart');
    if (ventasContainer) {
        const data = JSON.parse(ventasContainer.getAttribute('data-chart'));
        Plotly.newPlot('ventasChart', data.data, data.layout, {responsive: true});
    }

    // Inicializar gráfico de distribución
    const distribucionContainer = document.getElementById('distribucionChart');
    if (distribucionContainer) {
        const data = JSON.parse(distribucionContainer.getAttribute('data-chart'));
        Plotly.newPlot('distribucionChart', data.data, data.layout, {responsive: true});
    }

    // Initialize charts if their containers exist
    if (document.getElementById('ventasPortafolioChart')) {
        initVentasPortafolioChart();
    }

    if (document.getElementById('distribucionIndustriaChart')) {
        initDistribucionIndustriaChart();
    }

    if (document.getElementById('crecimientoYoYChart')) {
        initCrecimientoYoYChart();
    }

    if (document.getElementById('funnelProyectosChart')) {
        initFunnelProyectosChart();
    }

    if (document.getElementById('strategicPerformanceChart')) {
        initStrategicPerformanceChart();
    }
});

// Load Chart.js from CDN
function loadChartJS(callback) {
    if (window.Chart) {
        callback();
        return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js';
    script.onload = callback;
    document.head.appendChild(script);
}

// Initialize Ventas por Portafolio chart
function initVentasPortafolioChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('ventasPortafolioChart').getContext('2d');
        const chartContainer = document.getElementById('ventasPortafolioChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));

        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `$${context.raw.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    });
}

// Initialize Distribución por Industria chart
function initDistribucionIndustriaChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('distribucionIndustriaChart').getContext('2d');
        const chartContainer = document.getElementById('distribucionIndustriaChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));

        new Chart(ctx, {
            type: 'doughnut',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    });
}

// Initialize Crecimiento YoY chart (Line chart)
function initCrecimientoYoYChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('crecimientoYoYChart').getContext('2d');

        // Get data from data attribute
        const chartContainer = document.getElementById('crecimientoYoYChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));

        const labels = chartData.map(item => item.mes);
        const currentYearData = chartData.map(item => item.actual);
        const previousYearData = chartData.map(item => item.anterior);

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Año Actual',
                        data: currentYearData,
                        borderColor: 'rgba(52, 152, 219, 1)',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Año Anterior',
                        data: previousYearData,
                        borderColor: 'rgba(149, 165, 166, 1)',
                        backgroundColor: 'rgba(149, 165, 166, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('es-MX', {
                                        style: 'currency',
                                        currency: 'MXN'
                                    }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString('es-MX');
                            }
                        }
                    }
                }
            }
        });
    });
}

// Initialize Funnel de Proyectos chart (Horizontal bar chart for funnel representation)
function initFunnelProyectosChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('funnelProyectosChart').getContext('2d');

        // Get data from data attribute
        const chartContainer = document.getElementById('funnelProyectosChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));

        const labels = chartData.map(item => item.etapa);
        const data = chartData.map(item => item.cantidad);

        // Colors from darker to lighter
        const backgroundColors = [
            'rgba(52, 152, 219, 0.9)',  // Propuesta
            'rgba(52, 152, 219, 0.8)',  // Planificación
            'rgba(52, 152, 219, 0.7)',  // Ejecución
            'rgba(52, 152, 219, 0.6)',  // Cierre
            'rgba(52, 152, 219, 0.5)'   // Post-evaluación
        ];

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    axis: 'y',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Proyectos: ${context.parsed.x}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
}

// Function to create a custom progress chart
function createProgressChart(elementId, value, maxValue, color) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const percentage = (value / maxValue) * 100;

    element.innerHTML = `
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: ${percentage}%; background-color: ${color};"></div>
        </div>
        <div class="progress-value">${value} / ${maxValue}</div>
    `;
}

function initStrategicPerformanceChart() {
    const metrics = [
        'Cumplimiento de Objetivos',
        'Satisfacción del Cliente',
        'Retención de Consultores',
        'Eficiencia Operativa'
    ];
    const values = [92, 88, 85, 94];

    const data = [{
        type: 'scatterpolar',
        r: [...values, values[0]], // Repeat first value to close the shape
        theta: [...metrics, metrics[0]], // Repeat first label to close the shape
        fill: 'toself',
        fillcolor: 'rgba(86, 5, 145, 0.2)',
        line: {
            color: '#560591',
            width: 2
        },
        name: 'Desempeño Actual'
    }];

    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 100],
                ticksuffix: '%',
                showline: false,
                tickfont: {
                    color: '#560591'
                }
            },
            angularaxis: {
                tickfont: {
                    color: '#560591'
                }
            }
        },
        showlegend: false,
        paper_bgcolor: '#F0F0F3',
        plot_bgcolor: '#F0F0F3',
        margin: {
            l: 50,
            r: 50,
            t: 30,
            b: 30
        }
    };

    Plotly.newPlot('strategicPerformanceChart', data, layout, {
        displayModeBar: false,
        responsive: true
    });
}