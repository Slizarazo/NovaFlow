// maps.js - Handles maps functionality using Leaflet.js

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize map if the container exists
    if (document.getElementById('operationsMap')) {
        initOperationsMap();
    }
});

// Load Leaflet.js from CDN
function loadLeaflet(callback) {
    if (window.L) {
        callback();
        return;
    }
    
    // Load CSS
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    cssLink.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';
    cssLink.crossOrigin = '';
    document.head.appendChild(cssLink);
    
    // Load JS
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
    script.crossOrigin = '';
    script.onload = callback;
    document.head.appendChild(script);
}

// Initialize Operations Map
function initOperationsMap() {
    loadLeaflet(function() {
        const mapContainer = document.getElementById('operationsMap');
        let mapData = [];

        try {
            mapData = JSON.parse(mapContainer.dataset.locations || '[]');
            console.log("Ubicaciones cargadas:", mapData);
        } catch (error) {
            console.error('Error al parsear las ubicaciones:', error);
            mapData = [];
        }

        const map = L.map('operationsMap').setView([19.4326, -99.1332], 5);

        const tileLayers = {
            light: L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors & CartoDB',
                subdomains: 'abcd',
                maxZoom: 19
            }),
            dark: L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors & CartoDB',
                subdomains: 'abcd',
                maxZoom: 19
            }),
            toner: L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png', {
                attribution: 'Map tiles by Stamen Design, OpenStreetMap contributors',
                maxZoom: 20
            }),
            watercolor: L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg', {
                attribution: 'Map tiles by Stamen Design, OpenStreetMap contributors',
                maxZoom: 18
            }),
            satellite: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri & Earthstar Geographics',
                maxZoom: 18
            })
        };

        // Agregar inicialmente estilo claro
        tileLayers.light.addTo(map);
        let currentLayer = tileLayers.light;

        // Asegurar que marcadores se agregan después que el mapa esté listo
        map.whenReady(() => {
            const markers = [];

            mapData.forEach(location => {
                if (location.lat && location.lng) {
                    const marker = L.marker([location.lat, location.lng])
                        .addTo(map)
                        .bindPopup(`
                            <strong>${location.nombre}</strong><br>
                            Proyectos activos: ${location.proyectos}<br>
                            Consultores asignados: ${location.consultores}
                        `);
                    markers.push(marker);
                } else {
                    console.warn("Ubicación inválida:", location);
                }
            });

            console.log("Marcadores creados:", markers.length);

            if (markers.length > 0) {
                const group = L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.1));
            } else {
                console.warn("No hay marcadores para mostrar.");
            }
        });

        // Selector de estilo dinámico
        const styleSelector = document.getElementById('mapStyleSelect');
        styleSelector.addEventListener('change', function() {
            const selectedStyle = styleSelector.value;
            if (tileLayers[selectedStyle]) {
                map.removeLayer(currentLayer);
                currentLayer = tileLayers[selectedStyle];
                currentLayer.addTo(map);
            }
        });

        // Agregar leyenda
        const legend = L.control({position: 'bottomright'});
        legend.onAdd = function(map) {
            const div = L.DomUtil.create('div', 'info legend');
            div.style.backgroundColor = 'white';
            div.style.padding = '10px';
            div.style.borderRadius = '5px';
            div.style.boxShadow = '0 1px 5px rgba(0,0,0,0.4)';
            div.innerHTML = `
                <strong>Operaciones</strong><br>
                <div style="margin-top: 5px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background-color: #2c3e50; border-radius: 50%; margin-right: 5px;"></span> Ubicaciones
                </div>
            `;
            return div;
        };
        legend.addTo(map);
    });
}


