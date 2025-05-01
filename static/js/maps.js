
// maps.js - Handles maps functionality using Leaflet.js

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('operationsMap')) {
        initOperationsMap();
    }
});

function loadLeaflet(callback) {
    if (window.L) {
        callback();
        return;
    }
    
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    cssLink.crossOrigin = '';
    document.head.appendChild(cssLink);
    
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.crossOrigin = '';
    script.onload = callback;
    document.head.appendChild(script);
}

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

        // Personalización del mapa
        const map = L.map('operationsMap', {
            zoomControl: false,
            scrollWheelZoom: true
        }).setView([19.4326, -99.1332], 5);

        // Estilos personalizados para el mapa base
        const customStyle = {
            default: {
                url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                options: {
                    attribution: '&copy; OpenStreetMap, CartoDB',
                    subdomains: 'abcd',
                    maxZoom: 19
                }
            },
            dark: {
                url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                options: {
                    attribution: '&copy; OpenStreetMap, CartoDB',
                    subdomains: 'abcd',
                    maxZoom: 19
                }
            }
        };

        // Agregar capa base
        const baseLayer = L.tileLayer(customStyle.default.url, customStyle.default.options);
        baseLayer.addTo(map);

        // Personalizar los controles
        L.control.zoom({
            position: 'bottomright'
        }).addTo(map);

        // Estilo personalizado para los marcadores
        const customIcon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="
                width: 30px;
                height: 30px;
                background: var(--primary-purple);
                border-radius: 50%;
                border: 3px solid white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 14px;
                font-weight: bold;
            ">
                <span style="transform: translateY(-1px);">●</span>
            </div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });

        // Agregar marcadores al mapa
        const markers = [];
        mapData.forEach(location => {
            if (location.lat && location.lng) {
                const marker = L.marker([location.lat, location.lng], {
                    icon: customIcon
                }).addTo(map);

                // Personalizar popup
                const popupContent = `
                    <div style="
                        padding: 10px;
                        min-width: 200px;
                        font-family: var(--font-primary);
                    ">
                        <h4 style="
                            color: var(--dark-purple);
                            margin: 0 0 10px 0;
                            font-size: 16px;
                            font-weight: 600;
                        ">${location.nombre}</h4>
                        <div style="
                            display: grid;
                            grid-gap: 5px;
                            font-size: 14px;
                        ">
                            <div style="
                                display: flex;
                                align-items: center;
                                color: var(--dark-gray);
                            ">
                                <span style="
                                    width: 10px;
                                    height: 10px;
                                    background: var(--primary-blue);
                                    border-radius: 50%;
                                    margin-right: 8px;
                                "></span>
                                Proyectos activos: ${location.proyectos}
                            </div>
                            <div style="
                                display: flex;
                                align-items: center;
                                color: var(--dark-gray);
                            ">
                                <span style="
                                    width: 10px;
                                    height: 10px;
                                    background: var(--primary-pink);
                                    border-radius: 50%;
                                    margin-right: 8px;
                                "></span>
                                Consultores: ${location.consultores}
                            </div>
                        </div>
                    </div>
                `;

                marker.bindPopup(popupContent, {
                    className: 'custom-popup',
                    closeButton: false,
                    maxWidth: 300,
                    minWidth: 200,
                    autoPan: true,
                    autoPanPadding: [50, 50]
                });

                markers.push(marker);
            }
        });

        // Ajustar vista a los marcadores
        if (markers.length > 0) {
            const group = L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }

        // Agregar leyenda personalizada
        const legend = L.control({ position: 'bottomleft' });
        legend.onAdd = function() {
            const div = L.DomUtil.create('div', 'map-legend');
            div.innerHTML = `
                <div style="
                    background: white;
                    padding: 15px;
                    border-radius: var(--border-radius-md);
                    box-shadow: var(--shadow-md);
                    font-family: var(--font-primary);
                    min-width: 200px;
                ">
                    <h4 style="
                        margin: 0 0 10px 0;
                        color: var(--dark-purple);
                        font-size: 14px;
                        font-weight: 600;
                    ">Operaciones</h4>
                    <div style="
                        display: grid;
                        grid-gap: 8px;
                        font-size: 12px;
                    ">
                        <div style="display: flex; align-items: center;">
                            <span style="
                                width: 10px;
                                height: 10px;
                                background: var(--primary-purple);
                                border-radius: 50%;
                                margin-right: 8px;
                            "></span>
                            Ubicaciones
                        </div>
                    </div>
                </div>
            `;
            return div;
        };
        legend.addTo(map);
    });
}
