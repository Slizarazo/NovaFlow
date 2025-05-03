
// Configuración global de Chart.js
Chart.defaults.font.family = 'Poppins, sans-serif';
Chart.defaults.color = '#560591';

// Almacenar las instancias de los gráficos
let charts = {};

// Inicializar los gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
});

function initCharts() {
    // Inicializar gráfico de ventas
    const ventasCtx = document.getElementById('ventasChart');
    if (ventasCtx) {
        const data = JSON.parse(ventasCtx.getAttribute('data-chart'));
        charts.ventas = new Chart(ventasCtx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(86,5,145,0.8)',
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return `Ventas: $${context.raw.toLocaleString()}`;
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
    }

    // Inicializar gráfico de distribución
    const distribucionCtx = document.getElementById('distribucionChart');
    if (distribucionCtx) {
        const data = JSON.parse(distribucionCtx.getAttribute('data-chart'));
        charts.distribucion = new Chart(distribucionCtx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(86,5,145,0.8)',
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }
}

// Alternar entre tipos de gráfico
function toggleChartType(chartId) {
    const chart = charts[chartId.replace('Chart', '')];
    if (!chart) return;

    const types = {
        'bar': 'line',
        'line': 'bar',
        'doughnut': 'pie',
        'pie': 'doughnut'
    };

    const currentType = chart.config.type;
    const newType = types[currentType] || currentType;

    chart.config.type = newType;
    chart.update('none');
}

// Alternar pantalla completa
function toggleChartFullscreen(chartId) {
    const chartContainer = document.getElementById(chartId).parentElement;
    
    if (!document.fullscreenElement) {
        chartContainer.requestFullscreen().catch(err => {
            console.log(`Error al intentar modo pantalla completa: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

// charts.js - Handles all chart visualizations using Chart.js

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
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

// Initialize Ventas por Portafolio chart (Bar chart)
function initVentasPortafolioChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('ventasPortafolioChart').getContext('2d');
        
        // Get data from data attribute
        const chartContainer = document.getElementById('ventasPortafolioChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));
        
        const labels = chartData.map(item => item.nombre);
        const data = chartData.map(item => item.ventas);
        
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ventas por Portafolio',
                    data: data,
                    backgroundColor: 'rgba(52, 152, 219, 0.7)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }]
            },
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
                        beginAtZero: true,
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

// Initialize Distribución por Industria chart (Pie chart)
function initDistribucionIndustriaChart() {
    loadChartJS(function() {
        const ctx = document.getElementById('distribucionIndustriaChart').getContext('2d');
        
        // Get data from data attribute
        const chartContainer = document.getElementById('distribucionIndustriaChart');
        const chartData = JSON.parse(chartContainer.getAttribute('data-chart'));
        
        const labels = chartData.map(item => item.industria);
        const data = chartData.map(item => item.porcentaje);
        
        // Custom colors for industries
        const backgroundColors = [
            'rgba(52, 152, 219, 0.7)',  // Blue
            'rgba(155, 89, 182, 0.7)',  // Purple
            'rgba(46, 204, 113, 0.7)',  // Green
            'rgba(230, 126, 34, 0.7)',  // Orange
            'rgba(149, 165, 166, 0.7)'  // Gray
        ];
        
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                    borderWidth: 1
                }]
            },
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
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += context.parsed + '%';
                                }
                                return label;
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
