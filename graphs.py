import folium
import matplotlib
matplotlib.use('Agg')  # Muy importante

import matplotlib.pyplot as plt
import io
import base64
import requests
import pandas as pd
import json

def generar_html_mapa_operaciones(ubicaciones, centro_mapa=[23.6345, -102.5528], zoom_inicio=5):
    """
    Genera el HTML del mapa de operaciones como string, sin guardar archivos.
    Aplica una paleta de colores personalizada a los marcadores.
    """

    # Definimos la paleta de colores (usaremos los colores más oscuros para los íconos)
    colores_personalizados = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080']

    # Crear mapa
    m = folium.Map(location=centro_mapa, zoom_start=zoom_inicio)

    for idx, ub in enumerate(ubicaciones):
        # Asignar color rotando en la lista
        color_actual = colores_personalizados[idx % len(colores_personalizados)]

        # Crear popup con más detalles
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <strong>{ub['nombre']}</strong><br>
            <b>Proyectos activos:</b> {ub['proyectos']}<br>
            <b>Consultores asignados:</b> {ub['consultores']}<br>
            <b>Coordenadas:</b> {ub['lat']}, {ub['lng']}
        </div>
        """

        # Agregar marcador personalizado
        folium.Marker(
            location=[ub['lat'], ub['lng']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=ub['nombre'],
            icon=folium.Icon(color="white", icon_color=color_actual, icon='info-sign')
        ).add_to(m)

    # Renderizar el mapa en memoria (sin archivo)
    return m.get_root().render()

def generar_grafico_ventas(ventas):
    """
    Genera el gráfico en memoria con paleta de colores personalizada.
    """
    # Extraer datos
    nombres = [v['nombre'] for v in ventas]
    valores = [v['ventas'] for v in ventas]

    # Paleta de colores Deepnova
    colores = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080', '#F0F0F3', '#FFFFFF']

    # Crear la figura
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Asignar colores cíclicamente si hay más barras que colores
    colores_asignados = [colores[i % len(colores)] for i in range(len(nombres))]

    # Crear el gráfico de barras horizontales
    ax.barh(nombres, valores, color=colores_asignados)

    # Estilizar
    ax.set_xlabel('Ventas ($)', fontsize=12, color='#560591')
    ax.set_title('Ventas por Portafolio', fontsize=14, color='#560591', pad=20)
    ax.tick_params(axis='x', colors='#560591')
    ax.tick_params(axis='y', colors='#560591')
    fig.patch.set_facecolor('#F0F0F3')  # Fondo del gráfico
    ax.set_facecolor('#FFFFFF')          # Fondo de la zona de dibujo
    plt.tight_layout()

    # Guardarlo en un buffer en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return img_base64

def generar_grafico_distribucion_industria(distribucion):
    """
    Genera un gráfico de distribución de industrias en formato base64.

    Args:
        distribucion (list): Lista de dicts con 'industria' y 'porcentaje'.

    Returns:
        str: Imagen en base64 lista para inyectar en HTML.
    """
    # Extraer datos
    etiquetas = [item['industria'] for item in distribucion]
    valores = [item['porcentaje'] for item in distribucion]

    # Paleta de colores Deepnova
    colores = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080']

    # Asignar colores cíclicamente si hay más industrias que colores
    colores_asignados = [colores[i % len(colores)] for i in range(len(etiquetas))]

    # Crear la figura
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        valores, 
        labels=etiquetas, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colores_asignados,
        pctdistance=0.85
    )

    # Dibujar un círculo blanco en el centro para crear el efecto de "dona"
    centro_circulo = plt.Circle((0, 0), 0.70, fc='#F0F0F3')
    fig.gca().add_artist(centro_circulo)

    # Estilos de texto
    for text in texts:
        text.set_color('#560591')
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)

    ax.set_title('Distribución por Industria', color='#560591', fontsize=16)
    fig.patch.set_facecolor('#FFFFFF')  # Fondo blanco para todo el gráfico
    plt.tight_layout()

    # Guardar la figura en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return imagen_base64

def generar_mapa_sesiones_por_pais(sesiones):
    """
    Genera un mapa mundial fijo, sobrio, sin bordes de países, con tooltips elegantes.
    """

    # Crear DataFrame
    df = pd.DataFrame(sesiones)

    # Cargar GeoJSON de países
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    geo_json_data = requests.get(url).json()

    # Crear mapa base
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles=None,  # No tiles = fondo blanco
        control_scale=False,
        zoom_control=False,  # Quitar botones + y -
        dragging=False,      # No mover mapa
        scrollWheelZoom=False # No zoom con rueda
    )

    # Agregar capa choropleth
    folium.Choropleth(
        geo_data=geo_json_data,
        name='choropleth',
        data=df,
        columns=['pais', 'sesiones'],
        key_on='feature.id',
        fill_color='PuBu',  # Paleta muy suave: azul claro
        fill_opacity=0.2,
        line_opacity=0.01,   # Sin bordes
        legend_name='Sesiones por País',
        highlight=False
    ).add_to(m)

    # Crear tooltips elegantes
    for feature in geo_json_data['features']:
        codigo_pais = feature['id']
        nombre_pais = feature['properties']['name']
        matching_row = df[df['pais'] == codigo_pais]

        if not matching_row.empty:
            sesiones_valor = int(matching_row.iloc[0]['sesiones'])
            feature['properties']['tooltip_text'] = f"{nombre_pais}: {sesiones_valor} sesiones"
        else:
            feature['properties']['tooltip_text'] = f"{nombre_pais}: 0 sesiones"

    # Agregar los tooltips
    folium.features.GeoJson(
        geo_json_data,
        name="Labels",
        tooltip=folium.features.GeoJsonTooltip(
            fields=['tooltip_text'],
            aliases=[''],
            labels=False,
            sticky=True,
            style=("background-color: rgba(255,255,255,0.8); color: #333333; font-family: Arial; font-size: 12px; padding: 5px; border-radius: 3px; box-shadow: 0px 0px 5px rgba(0,0,0,0.1);")
        )
    ).add_to(m)

    return m.get_root().render()







