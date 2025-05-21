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
                          width=500)

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
                          width=500)

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

def generar_grafico_funnel_proyectos(funnel_data):
    """
    Genera un gráfico de embudo interactivo con la estética Deepnova
    para visualizar el avance de proyectos en sus diferentes etapas.
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    etapas = [item['etapa'] for item in funnel_data]
    valores = [item['cantidad'] for item in funnel_data]

    # Paleta Deepnova extendida
    colores_base = ['#560591', '#D400AC', '#00A0FF', '#000000', '#808080']
    colores_asignados = [colores_base[i % len(colores_base)] for i in range(len(etapas))]

    fig = go.Figure()

    fig.add_trace(go.Funnel(
        y=etapas[::-1],  # De arriba hacia abajo
        x=valores[::-1],  # Correspondencia inversa
        textposition="inside",
        textinfo="value+percent initial",
        opacity=0.85,
        marker=dict(color=colores_asignados),
        connector=dict(line=dict(color="#560591", width=1))
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=12),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#F0F0F3',
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        showlegend=False,
        autosize=True
    )

    config = {
        'displayModeBar': True,
        'responsive': True,
        'showLink': False
    }

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config=config)

def generar_grafico_desempeno_estrategico(aliados=None, cuentas=None, supervisores=None, consultores=None):
    """
    Genera un gráfico de radar para mostrar el desempeño estratégico con filtros
    """
    import plotly.graph_objects as go
    import plotly.io as pio
    from models import Aliado, Consultor

    # Datos base del desempeño
    metrics = [
        'Cumplimiento de Objetivos',
        'Satisfacción del Cliente', 
        'Retención de Consultores',
        'Eficiencia Operativa'
    ]
    values = [92, 88, 85, 94]

    # Crear figura con dropdown menus
    fig = go.Figure()

    # Agregar trace principal
    fig.add_trace(go.Scatterpolar(
        r=[*values, values[0]],
        theta=[*metrics, metrics[0]],
        fill='toself',
        fillcolor='rgba(86, 5, 145, 0.2)',
        line=dict(color='#560591', width=2),
        name='Desempeño Actual'
    ))

    # Agregar dropdowns para filtros
    updatemenus = [
        dict(
            buttons=[
                dict(
                    args=[{"visible": [True]}],
                    label="Todos",
                    method="update"
                ),
            ],
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top",
            name="Aliado"
        ),
        dict(
            buttons=[
                dict(
                    args=[{"visible": [True]}],
                    label="Todas",
                    method="update"
                ),
            ],
            direction="down",
            showactive=True,
            x=0.3,
            xanchor="left",
            y=1.1,
            yanchor="top",
            name="Cuenta"
        ),
        dict(
            buttons=[
                dict(
                    args=[{"visible": [True]}],
                    label="Todos",
                    method="update"
                ),
            ],
            direction="down",
            showactive=True,
            x=0.5,
            xanchor="left",
            y=1.1,
            yanchor="top",
            name="Supervisor"
        ),
        dict(
            buttons=[
                dict(
                    args=[{"visible": [True]}],
                    label="Todos",
                    method="update"
                ),
            ],
            direction="down",
            showactive=True,
            x=0.7,
            xanchor="left", 
            y=1.1,
            yanchor="top",
            name="Consultor"
        )
    ]

    # Agregar botones para cada aliado
    for aliado in Aliado.ALIADOS:
        updatemenus[0]["buttons"].append(
            dict(
                args=[{"visible": [True]}],
                label=aliado.nombre,
                method="update"
            )
        )

    # Agregar botones para cada consultor  
    for consultor in Consultor.CONSULTORES:
        updatemenus[3]["buttons"].append(
            dict(
                args=[{"visible": [True]}],
                label=consultor.nombre,
                method="update"
            )
        )

    # Actualizar layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%',
                showline=False,
                tickfont=dict(color='#560591')
            ),
            angularaxis=dict(
                tickfont=dict(color='#560591')
            )
        ),
        updatemenus=updatemenus,
        showlegend=False,
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#F0F0F3',
        margin=dict(l=50, r=50, t=80, b=30),  # Increased top margin for filters
        height=500  # Increased height to accommodate filters
    )

    # Agregar títulos para los filtros
    annotations = [
        dict(text="Filtrar por:", x=0, y=1.1, xref="paper", yref="paper",
             showarrow=False, font=dict(size=12, color="#560591"))
    ]
    fig.update_layout(annotations=annotations)

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

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
            margin=dict(l=50, r=50, t=50, b=30),
            height=300,
            width=1000,
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
def generar_grafico_ingresos_vs_costos(data):
    """
    Genera un gráfico de líneas comparando ingresos vs costos
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['ingresos'],
        name='Ingresos',
        line=dict(color='#560591', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['costos'],
        name='Costos',
        line=dict(color='#D400AC', width=3)
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(gridcolor='#E1E1E1', tickformat='$,.0f'),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_tasa_crecimiento(data):
    """
    Genera un gráfico de barras con la tasa de crecimiento
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data['trimestres'],
        y=data['tasa_crecimiento'],
        marker_color='#560591'
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(
            gridcolor='#E1E1E1',
            tickformat='.1%',
            title='Tasa de Crecimiento'
        ),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_clientes_nuevos_vs_recurrentes(data):
    """
    Genera un gráfico de barras apiladas para clientes nuevos vs recurrentes
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data['meses'],
        y=data['clientes_nuevos'],
        name='Nuevos',
        marker_color='#560591'
    ))

    fig.add_trace(go.Bar(
        x=data['meses'],
        y=data['clientes_recurrentes'],
        name='Recurrentes',
        marker_color='#00A0FF'
    ))

    fig.update_layout(
        barmode='stack',
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_proyectos_activos(data):
    """
    Genera un gráfico de barras para proyectos activos por etapa
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Bar(
            x=data['etapas'],
            y=data['cantidad'],
            marker_color='#560591'
        )
    ])

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(gridcolor='#E1E1E1', title='Cantidad de Proyectos'),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_pipeline(data):
    """
    Genera un gráfico de embudo para el pipeline de oportunidades
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Funnel(
            y=data['etapas'],
            x=data['cantidad'],
            textinfo="value+percent initial",
            marker=dict(color=['#560591', '#D400AC', '#00A0FF', '#000000'])
        )
    ])

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_desempeno_proyectos(data):
    """
    Genera un gráfico de radar para el desempeño de proyectos
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    for i, proyecto in enumerate(data['proyectos']):
        fig.add_trace(go.Scatterpolar(
            r=[data['avance'][i], data['calidad'][i], data['satisfaccion'][i]],
            theta=['Avance', 'Calidad', 'Satisfacción'],
            fill='toself',
            name=proyecto
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%'
            )),
        showlegend=True,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_tiempos(data):
    """
    Genera un gráfico de barras comparando tiempos estimados vs reales
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Bar(
            name='Tiempo Estimado',
            x=data['proyectos'],
            y=data['estimado'],
            marker_color='#560591'
        ),
        go.Bar(
            name='Tiempo Real',
            x=data['proyectos'],
            y=data['real'],
            marker_color='#D400AC'
        )
    ])

    fig.update_layout(
        barmode='group',
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(gridcolor='#E1E1E1', title='Días'),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_segmentacion_clientes(data):
    """
    Genera un gráfico de dona para la segmentación de clientes
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Pie(
            labels=data['segmentos'],
            values=data['cantidad'],
            hole=0.6,
            marker=dict(colors=data['colores']),
            textinfo='label+percent',
            textposition='outside'
        )
    ])

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        showlegend=False
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_clv(data):
    """
    Genera un gráfico de líneas para el CLV por segmento
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['premium'],
        name='Premium',
        line=dict(color='#560591', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['business'],
        name='Business',
        line=dict(color='#D400AC', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['standard'],
        name='Standard',
        line=dict(color='#00A0FF', width=3)
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(
            gridcolor='#E1E1E1',
            title='CLV ($)',
            tickformat='$,.0f'
        ),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_retencion(data):
    """
    Genera un gráfico de área para la tasa de retención
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['tasa_retencion'],
        fill='tozeroy',
        fillcolor='rgba(86, 5, 145, 0.2)',
        line=dict(color='#560591', width=3)
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(
            gridcolor='#E1E1E1',
            title='Tasa de Retención',
            tickformat='.0%',
            range=[0, 100]
        ),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_consultores_proyecto(data):
    """
    Genera un gráfico de barras para mostrar consultores por proyecto
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Bar(
            x=data['proyectos'],
            y=data['consultores'],
            marker_color='#560591'
        )
    ])

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Número de Consultores', gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_horas_vs_progreso(data):
    """
    Genera un gráfico de dispersión para horas vs progreso
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['horas'],
        y=data['progreso'],
        mode='markers+text',
        text=data['proyectos'],
        textposition="top center",
        marker=dict(
            size=15,
            color='#560591',
            symbol='circle'
        )
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Progreso (%)', gridcolor='#E1E1E1'),
        xaxis=dict(title='Horas Trabajadas', gridcolor='#E1E1E1')
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_consultores_eficientes(data):
    """
    Genera un gráfico de radar para eficiencia de consultores
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    for i, consultor in enumerate(data['consultores']):
        fig.add_trace(go.Scatterpolar(
            r=[data['eficiencia'][i], data['tareas_completadas'][i], 100-data['horas_promedio'][i]*10],
            theta=['Eficiencia', 'Tareas Completadas', 'Optimización de Tiempo'],
            fill='toself',
            name=consultor
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_tareas_completadas(data):
    """
    Genera un gráfico de barras apiladas para tareas por consultor
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure(data=[
        go.Bar(name='Completadas', x=data['consultores'], y=data['completadas'], marker_color='#560591'),
        go.Bar(name='En Progreso', x=data['consultores'], y=data['en_progreso'], marker_color='#D400AC'),
        go.Bar(name='Pendientes', x=data['consultores'], y=data['pendientes'], marker_color='#00A0FF')
    ])

    fig.update_layout(
        barmode='stack',
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Número de Tareas', gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_facturacion(data):
    """
    Genera un gráfico combinado de facturación mensual y anual
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=2, cols=1, subplot_titles=('Facturación Mensual', 'Facturación Anual'))

    # Facturación Mensual
    fig.add_trace(
        go.Bar(
            x=data['meses'],
            y=data['facturacion'],
            marker_color='#560591',
            name='Mensual'
        ),
        row=1, col=1
    )

    # Facturación Anual
    fig.add_trace(
        go.Scatter(
            x=['2022', '2023', '2024', '2025'],
            y=data['anual'],
            mode='lines+markers',
            line=dict(color='#D400AC', width=3),
            name='Anual'
        ),
        row=2, col=1
    )

    fig.update_layout(
        height=500,
        showlegend=True,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=50, b=30)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_deudas(data):
    """
    Genera un gráfico de barras apiladas para deudas y cobros
    """
    import plotly.graph_objects as go

    fig = go.Figure(data=[
        go.Bar(
            name='Por Cobrar',
            x=data['clientes'],
            y=data['por_cobrar'],
            marker_color='#560591'
        ),
        go.Bar(
            name='Vencido',
            x=data['clientes'],
            y=data['vencido'],
            marker_color='#D400AC'
        )
    ])

    fig.update_layout(
        barmode='stack',
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Monto ($)', gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_rentabilidad_proyecto(data):
    """
    Genera un gráfico de cascada para rentabilidad por proyecto
    """
    import plotly.graph_objects as go

    fig = go.Figure(data=[
        go.Bar(
            name='Ingresos',
            x=data['proyectos'],
            y=data['ingresos'],
            marker_color='#560591'
        ),
        go.Bar(
            name='Costos',
            x=data['proyectos'],
            y=[-x for x in data['costos']],
            marker_color='#D400AC'
        )
    ])

    fig.update_layout(
        barmode='relative',
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Monto ($)', gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_flujo_caja(data):
    """
    Genera un gráfico de área para el flujo de caja
    """
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['ingresos'],
        name='Ingresos',
        line=dict(color='#560591', width=3),
        fill=None
    ))

    fig.add_trace(go.Scatter(
        x=data['meses'],
        y=data['egresos'],
        name='Egresos',
        line=dict(color='#D400AC', width=3),
        fill='tonexty'
    ))

    fig.update_layout(
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(title='Monto ($)', gridcolor='#E1E1E1'),
        xaxis=dict(gridcolor='#E1E1E1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_satisfaccion(data):
    """
    Genera un gráfico combinado de NPS y calificación
    """
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "scatter"}]])

    # NPS Donut
    fig.add_trace(
        go.Pie(
            labels=data['nps_categorias'],
            values=data['nps_valores'],
            hole=0.7,
            marker=dict(colors=['#560591', '#D400AC', '#00A0FF']),
            textinfo='label+percent',
            textposition='inside',
            showlegend=False
        ),
        row=1, col=1
    )

    # Tendencia de calificación
    fig.add_trace(
        go.Scatter(
            y=data['tendencia'],
            mode='lines+markers',
            line=dict(color='#560591', width=3),
            showlegend=False
        ),
        row=1, col=2
    )

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        yaxis=dict(
            gridcolor='#E1E1E1',
            title='Calificación',
            range=[0, 5]
        )
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generar_grafico_rentabilidad(data):
    """
    Genera un gráfico de burbujas para el análisis de rentabilidad
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['ingresos'],
        y=data['margenes'],
        mode='markers',
        marker=dict(
            size=data['volumen'],
            color=data['rentabilidad'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Rentabilidad')
        ),
        text=data['servicios'],
        hovertemplate="<b>%{text}</b><br>" +
                      "Ingresos: $%{x:,.0f}<br>" +
                      "Margen: %{y:.1%}<br>" +
                      "<extra></extra>"
    ))

    fig.update_layout(
        title=None,
        font=dict(color='#560591', size=10),
        paper_bgcolor='#F0F0F3',
        plot_bgcolor='#FFFFFF',
        margin=dict(l=50, r=50, t=30, b=30),
        height=300,
        xaxis=dict(
            title='Ingresos',
            gridcolor='#E1E1E1',
            tickformat='$,.0f'
        ),
        yaxis=dict(
            title='Margen',
            gridcolor='#E1E1E1',
            tickformat='.1%'
        )
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
