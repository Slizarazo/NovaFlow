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

def generar_datos_graficos(ventas, distribucion):
    """
    Genera los datos para los gráficos usando Plotly.
    """
    import plotly.express as px
    import plotly.graph_objects as go
    import json

    # Gráfico de ventas
    fig_ventas = go.Figure(data=[
        go.Bar(
            x=[str(v['nombre']) for v in ventas],
            y=[float(v['ventas']) for v in ventas],
            marker_color=['rgba(86,5,145,0.7)', 'rgba(212,0,172,0.7)', 'rgba(0,160,255,0.7)', 
                         'rgba(0,0,0,0.7)', 'rgba(128,128,128,0.7)']
        )
    ])
    fig_ventas.update_layout(
        title='Ventas por Portafolio',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#560591')
    )

    # Gráfico de distribución
    fig_distribucion = go.Figure(data=[
        go.Pie(
            labels=[str(d['industria']) for d in distribucion],
            values=[float(d['porcentaje']) for d in distribucion],
            marker=dict(colors=['rgba(86,5,145,0.7)', 'rgba(212,0,172,0.7)', 
                              'rgba(0,160,255,0.7)', 'rgba(0,0,0,0.7)', 'rgba(128,128,128,0.7)'])
        )
    ])
    fig_distribucion.update_layout(
        title='Distribución por Industria',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#560591')
    )

    return json.dumps(fig_ventas.to_dict()), json.dumps(fig_distribucion.to_dict())

def generar_mapa_sesiones_por_pais(sesiones):
    """
    Genera un mapa mundial con indicadores de intensidad y etiquetas.
    """
    # Crear DataFrame
    df = pd.DataFrame(sesiones)
    
    # Definir rangos para la leyenda
    max_sesiones = df['sesiones'].max()
    bins = list(range(0, int(max_sesiones) + 50, 50))
    
    # Cargar GeoJSON de países
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    geo_json_data = requests.get(url).json()

    # Crear mapa base
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='cartodbpositron',
        control_scale=False,
        zoom_control=False,
        dragging=False,
        scrollWheelZoom=False
    )

    # Agregar capa choropleth con colores más intensos
    choropleth = folium.Choropleth(
        geo_data=geo_json_data,
        name='choropleth',
        data=df,
        columns=['pais', 'sesiones'],
        key_on='feature.id',
        fill_color='YlOrRd',  # Paleta amarillo a rojo para mejor visualización
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins,
        legend_name='Número de Sesiones',
        highlight=True
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

    # Agregar etiquetas con número de sesiones
    style_function = lambda x: {
        'fillColor': '#ffffff',
        'color': '#000000',
        'fillOpacity': 0.1,
        'weight': 0.1
    }
    
    highlight_function = lambda x: {
        'fillColor': '#560591',
        'color': '#000000',
        'fillOpacity': 0.5,
        'weight': 0.1
    }

    # Agregar los tooltips y etiquetas
    folium.features.GeoJson(
        geo_json_data,
        name="Labels",
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['tooltip_text'],
            aliases=[''],
            labels=False,
            sticky=True,
            style=("background-color: rgba(86,5,145,0.8); color: white; font-family: Arial; font-size: 12px; padding: 8px; border-radius: 4px; box-shadow: 0px 0px 5px rgba(0,0,0,0.2);")
        )
    ).add_to(m)

    # Agregar leyenda personalizada
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; font-family: Arial; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 10px 0; color: #560591;">Intensidad de Actividad</h4>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: #ffffb2; margin-right: 8px;"></div>
            <span>Baja (0-50)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: #fecc5c; margin-right: 8px;"></div>
            <span>Media (51-100)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: #fd8d3c; margin-right: 8px;"></div>
            <span>Alta (101-150)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: #e31a1c; margin-right: 8px;"></div>
            <span>Muy Alta (>150)</span>
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    return m.get_root().render()







