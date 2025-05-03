import folium
import matplotlib

matplotlib.use('Agg')  # Muy importante

import matplotlib.pyplot as plt
import io
import base64
import requests
import pandas as pd
import json


def generar_html_mapa_operaciones(ubicaciones,
                                  centro_mapa=[23.6345, -102.5528],
                                  zoom_inicio=5):
    """
    Genera el HTML del mapa de operaciones como string, sin guardar archivos.
    Aplica una paleta de colores personalizada a los marcadores.
    """

    # Definimos la paleta de colores (usaremos los colores más oscuros para los íconos)
    colores_personalizados = [
        '#560591', '#D400AC', '#00A0FF', '#000000', '#808080'
    ]

    # Crear mapa
    m = folium.Map(location=centro_mapa, zoom_start=zoom_inicio)

    for idx, ub in enumerate(ubicaciones):
        # Asignar color rotando en la lista
        color_actual = colores_personalizados[idx %
                                              len(colores_personalizados)]

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
        folium.Marker(location=[ub['lat'], ub['lng']],
                      popup=folium.Popup(popup_html, max_width=300),
                      tooltip=ub['nombre'],
                      icon=folium.Icon(color="white",
                                       icon_color=color_actual,
                                       icon='info-sign')).add_to(m)

    # Renderizar el mapa en memoria (sin archivo)
    return m.get_root().render()


def generar_grafico_ventas(ventas):
    """
    Genera un gráfico interactivo de barras horizontal con Plotly y lo retorna como HTML embebido.
    """
    try:
        import plotly.graph_objects as go
        import plotly.io as pio

        nombres = [v['nombre'] for v in ventas]
        valores = [v['ventas'] for v in ventas]

        # Paleta Deepnova
        colores = [
            '#560591', '#D400AC', '#00A0FF', '#000000', '#808080', '#F0F0F3',
            '#FFFFFF'
        ]
        colores_asignados = [
            colores[i % len(colores)] for i in range(len(nombres))
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(y=nombres,
                   x=valores,
                   orientation='h',
                   marker=dict(color=colores_asignados),
                   hoverinfo='x+y',
                   text=valores,
                   textposition='auto'))

        fig.update_layout(title='Ventas por Portafolio',
                          xaxis_title='Ventas ($)',
                          yaxis_title='',
                          plot_bgcolor='#FFFFFF',
                          paper_bgcolor='#F0F0F3',
                          font=dict(color='#560591', size=10),
                          title_font=dict(size=14, color='#560591'),
                          margin=dict(l=80, r=30, t=50, b=30),
                          height=300,
                          width=400)

        # Retornar como HTML embebido sin configuración visible
        return pio.to_html(fig,
                           full_html=False,
                           include_plotlyjs='cdn',
                           config={
                               'displayModeBar': True,
                               'showLink': False
                           })
    except Exception as e:
        print(f"Error generando gráfico de ventas: {e}")
        # Fallback a un gráfico básico usando matplotlib
        return generar_grafico_ventas_fallback(ventas)


def generar_grafico_ventas_fallback(ventas):
    """
    Genera un gráfico de barras horizontal usando matplotlib como fallback.
    """
    import matplotlib.pyplot as plt
    import io

    nombres = [v['nombre'] for v in ventas]
    valores = [v['ventas'] for v in ventas]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(nombres, valores, color='#560591')

    ax.set_title('Ventas por Portafolio', color='#560591', pad=20)
    ax.set_xlabel('Ventas ($)', color='#560591')

    # Estética
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#F0F0F3')

    # Guardar en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return imagen_base64


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
    colores_asignados = [
        colores[i % len(colores)] for i in range(len(etiquetas))
    ]

    # Crear la figura con dimensiones más pequeñas
    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(valores,
                                      labels=etiquetas,
                                      autopct='%1.1f%%',
                                      startangle=140,
                                      colors=colores_asignados,
                                      pctdistance=0.85)

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


def generar_grafico_distribucion_industria_html(distribucion):
    """
    Genera un gráfico de dona interactivo de la distribución por industria como HTML embebido.

    Args:
        distribucion (list): Lista de dicts con 'industria' y 'porcentaje'.

    Returns:
        str: HTML embebido del gráfico listo para insertar en una plantilla.
    """
    etiquetas = [item['industria'] for item in distribucion]
    valores = [item['porcentaje'] for item in distribucion]

    # Paleta Deepnova
    colores = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080']
    colores_asignados = [
        colores[i % len(colores)] for i in range(len(etiquetas))
    ]

    fig = go.Figure(data=[
        go.Pie(
            labels=etiquetas,
            values=valores,
            hole=0.5,
            marker=dict(colors=colores_asignados),
            hoverinfo='label+percent',
            textinfo='percent+label',
            textfont=dict(size=12, color='white'),
        )
    ])

    fig.update_layout(title='Distribución por Industria',
                      title_font=dict(size=16, color='#560591'),
                      font=dict(color='#560591'),
                      paper_bgcolor='#F0F0F3',
                      plot_bgcolor='#FFFFFF',
                      margin=dict(t=60, b=20, l=20, r=20))

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')


def generar_grafico_distribucion_industria_html(distribucion):
    """
    Genera un gráfico de dona interactivo de la distribución por industria como HTML embebido.

    Args:
        distribucion (list): Lista de dicts con 'industria' y 'porcentaje'.

    Returns:
        str: HTML embebido del gráfico listo para insertar en una plantilla.
    """
    try:
        import plotly.graph_objects as go
        import plotly.io as pio

        etiquetas = [item['industria'] for item in distribucion]
        valores = [item['porcentaje'] for item in distribucion]

        # Paleta Deepnova
        colores = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080']
        colores_asignados = [
            colores[i % len(colores)] for i in range(len(etiquetas))
        ]

        fig = go.Figure(data=[
            go.Pie(
                labels=etiquetas,
                values=valores,
                hole=0.5,
                marker=dict(colors=colores_asignados),
                hoverinfo='label+percent',
                textinfo='percent+label',
                textfont=dict(size=10, color='white'),
            )
        ])

        fig.update_layout(title='Distribución por Industria',
                          title_font=dict(size=14, color='#560591'),
                          font=dict(color='#560591', size=10),
                          paper_bgcolor='#F0F0F3',
                          plot_bgcolor='#FFFFFF',
                          margin=dict(l=30, r=30, t=50, b=30),
                          height=300,
                          width=400)

        # Retornar como HTML embebido sin configuración visible
        return pio.to_html(fig,
                           full_html=False,
                           include_plotlyjs='cdn',
                           config={
                               'displayModeBar': True,
                               'showLink': False
                           })
    except Exception as e:
        print(f"Error generando gráfico de distribución: {e}")
        return None
def generar_grafico_crecimiento_yoy(data):
    """
    Genera un gráfico de líneas para mostrar el crecimiento año tras año.
    
    Args:
        data (list): Lista de diccionarios con datos de crecimiento YoY.
        
    Returns:
        str: HTML del gráfico generado.
    """
    try:
        import plotly.graph_objects as go
        import plotly.io as pio

        # Extraer datos
        meses = [item['mes'] for item in data]
        actual = [item['actual'] for item in data]
        anterior = [item['anterior'] for item in data]

        # Crear figura
        fig = go.Figure()

        # Agregar líneas para año actual y anterior
        fig.add_trace(
            go.Scatter(
                x=meses,
                y=actual,
                name='Año Actual',
                line=dict(color='#560591', width=3),
                hovertemplate='%{y:$,.0f}<extra>Año Actual</extra>'
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=meses,
                y=anterior,
                name='Año Anterior',
                line=dict(color='#00A0FF', width=3, dash='dash'),
                hovertemplate='%{y:$,.0f}<extra>Año Anterior</extra>'
            )
        )

        # Actualizar layout
        fig.update_layout(
            title='Crecimiento Año a Año',
            title_font=dict(size=14, color='#560591'),
            font=dict(color='#560591', size=10),
            paper_bgcolor='#F0F0F3',
            plot_bgcolor='#FFFFFF',
            margin=dict(l=30, r=30, t=50, b=30),
            height=300,
            width=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            yaxis=dict(
                gridcolor='#E1E1E1',
                tickformat='$,.0f'
            ),
            xaxis=dict(
                gridcolor='#E1E1E1'
            )
        )

        return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={'displayModeBar': True, 'showLink': False})
    except Exception as e:
        print(f"Error generando gráfico de crecimiento YoY: {e}")
        return None

def generar_mapa_sesiones_por_pais(sesiones):
    """
    Genera un mapa de sesiones por país usando Folium.
    
    Args:
        sesiones (list): Lista de diccionarios con 'pais' y 'sesiones'.
        
    Returns:
        str: HTML del mapa generado.
    """
    import folium
    from branca.colormap import LinearColormap

    # Crear mapa base
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Obtener valores para la escala de color
    valores = [s['sesiones'] for s in sesiones]
    min_valor = min(valores)
    max_valor = max(valores)

    # Crear escala de color personalizada
    colormap = LinearColormap(
        colors=['#F0F0F3', '#560591'],
        vmin=min_valor,
        vmax=max_valor
    )
    
    # Agregar el mapa de coropletas
    folium.GeoJson(
        'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json',
        style_function=lambda feature: {
            'fillColor': colormap(next((s['sesiones'] for s in sesiones if s['pais'] == feature['id']), 0)),
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['name'],
            aliases=['País'],
            style=('background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;')
        )
    ).add_to(m)

    # Agregar la leyenda del mapa
    colormap.add_to(m)
    colormap.caption = 'Número de Sesiones'

    return m.get_root().render()
