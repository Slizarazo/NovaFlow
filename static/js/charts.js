// Inicializar los gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráfico de desempeño estratégico si existe
    if (document.getElementById('strategicPerformanceChart')) {
        initStrategicPerformanceChart();
    }
});

// Function to toggle chart fullscreen mode
function toggleChartFullscreen(chartCard) {
    if (!chartCard) return;
    chartCard.classList.toggle('fullscreen');
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
        r: [...values, values[0]],
        theta: [...metrics, metrics[0]],
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
        },
        height: 400,
        autosize: true
    };

    const config = {
        displayModeBar: true,
        responsive: true,
        showLink: false
    };

    Plotly.newPlot('strategicPerformanceChart', data, layout, config);
}