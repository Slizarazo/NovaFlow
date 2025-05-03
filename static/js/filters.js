
// Función para obtener los valores de los filtros
function getFilterValues() {
    return {
        aliado: document.getElementById('aliado').value,
        periodo: document.getElementById('periodo').value,
        cuenta: document.getElementById('cuenta').value,
        supervisor: document.getElementById('supervisor').value
    };
}

// Función para aplicar los filtros
function applyFilters() {
    const filters = getFilterValues();
    
    // Hacer la petición al servidor con los filtros
    fetch('/api/filter_dashboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        // Actualizar los KPIs
        updateKPIs(data.kpis);
        // Actualizar los gráficos
        updateCharts(data.charts);
    })
    .catch(error => console.error('Error:', error));
}

// Función para actualizar los KPIs
function updateKPIs(kpis) {
    document.querySelector('[data-kpi="ventas_trimestre"]').textContent = formatCurrency(kpis.ventas_trimestre);
    document.querySelector('[data-kpi="ventas_promedio_cuenta"]').textContent = formatCurrency(kpis.ventas_promedio_cuenta);
    document.querySelector('[data-kpi="ventas_promedio_proyecto"]').textContent = formatCurrency(kpis.ventas_promedio_proyecto);
    document.querySelector('[data-kpi="rentabilidad"]').textContent = formatCurrency(kpis.rentabilidad);
}

// Función para actualizar los gráficos
function updateCharts(charts) {
    // Actualizar mapa
    if (charts.mapa_sesiones) {
        document.getElementById('mapa-container').innerHTML = charts.mapa_sesiones;
    }
    
    // Actualizar gráfico de ventas
    if (charts.ventas_portafolio) {
        Plotly.react('ventas-container', charts.ventas_portafolio.data, charts.ventas_portafolio.layout);
    }
    
    // Actualizar distribución por industria
    if (charts.distribucion_industria) {
        Plotly.react('distribucion-container', charts.distribucion_industria.data, charts.distribucion_industria.layout);
    }
    
    // Actualizar crecimiento YoY
    if (charts.crecimiento_yoy) {
        Plotly.react('crecimiento-container', charts.crecimiento_yoy.data, charts.crecimiento_yoy.layout);
    }
}

// Función para formatear moneda
function formatCurrency(value) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(value);
}

// Inicializar los eventos de los filtros
document.addEventListener('DOMContentLoaded', function() {
    // Botón de aplicar filtros
    document.querySelector('.filter-apply').addEventListener('click', applyFilters);
    
    // Botón de restablecer filtros
    document.querySelector('.filter-reset').addEventListener('click', function() {
        document.querySelector('.filter-form').reset();
        applyFilters();
    });
});
