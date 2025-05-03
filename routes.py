from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from models import User, Aliado, Proyecto, Consultor, DatosDashboard
from config import Config
from graphs import *
import logging, json

# Importamos los datos de demostración extendidos
try:
    from data_demo import DatosDemoCompleto
    USAR_DATOS_EXTENDIDOS = True
    app.logger.info("Datos de demostración extendidos cargados correctamente")
except ImportError:
    USAR_DATOS_EXTENDIDOS = False
    app.logger.warning(
        "No se pudieron cargar los datos de demostración extendidos")


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_by_username(username)

        if user and user.password == password:  # In a real app, use proper password hashing
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña inválidos', 'danger')

    # Usamos app.config para acceder a la configuración
    return render_template('login.html',
                           title='Iniciar Sesión',
                           config=app.config,
                           role=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('dashboard_growth'))


@app.route('/dashboard/growth')
@login_required
def dashboard_growth():
    # Data for growth dashboard
    aliados = Aliado.ALIADOS
    ventas_trimestre_total = sum(aliado.ventas_trimestre for aliado in aliados)
    ventas_promedio_cuenta = ventas_trimestre_total / len(aliados)

    proyectos = Proyecto.PROYECTOS
    ventas_promedio_proyecto = ventas_trimestre_total / len(
        proyectos) if proyectos else 0

    # Assume rentabilidad is 30% of total sales for this mock
    rentabilidad = ventas_trimestre_total * 0.3

    kpis = {
        'ventas_trimestre': ventas_trimestre_total,
        'ventas_promedio_cuenta': ventas_promedio_cuenta,
        'ventas_promedio_proyecto': ventas_promedio_proyecto,
        'rentabilidad': rentabilidad
    }

    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        ventas_por_region = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'ventas_por_region']
        tendencias_industria = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'tendencias_industria']
        pipeline_ventas = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'pipeline_ventas']
        aliados_extendidos = DatosDemoCompleto.ALIADOS_EXTENDIDOS
        app.logger.info(
            "Usando datos extendidos para dashboard de crecimiento")
    else:
        # Usar datos estándar
        ventas_por_region = None
        tendencias_industria = None
        pipeline_ventas = None
        aliados_extendidos = None
        app.logger.info("Usando datos estándar para dashboard de crecimiento")

    ubicaciones = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
        'ubicaciones_operaciones'] if USAR_DATOS_EXTENDIDOS else DatosDashboard.UBICACIONES
    ventas_por_portafolio = DatosDashboard.VENTAS_POR_PORTAFOLIO
    distribucion_industria_data = DatosDashboard.DISTRIBUCION_INDUSTRIA

    sesiones = [{
        'pais': 'USA',
        'sesiones': 120
    }, {
        'pais': 'CAN',
        'sesiones': 80
    }, {
        'pais': 'FRA',
        'sesiones': 60
    }, {
        'pais': 'ITA',
        'sesiones': 50
    }, {
        'pais': 'CHN',
        'sesiones': 150
    }, {
        'pais': 'IND',
        'sesiones': 140
    }, {
        'pais': 'GBR',
        'sesiones': 100
    }]

    mapa_html = generar_html_mapa_operaciones(ubicaciones)
    datos_grafico = generar_grafico_ventas(ventas_por_portafolio)
    distribucion_industria = generar_grafico_distribucion_industria_html(
        distribucion_industria_data)
    mapa_sesions = generar_mapa_sesiones_por_pais(sesiones)

    # Generar gráfico de crecimiento YoY
    crecimiento_yoy = generar_grafico_crecimiento_yoy(DatosDashboard.CRECIMIENTO_ANUAL)
    
    return render_template(
        'dashboard/growth.html',
        title='Dashboard de Crecimiento',
        kpis=kpis,
        aliados=aliados,
        mapa_sesiones=mapa_sesions,
        mapa_html=mapa_html,
        datos_grafico=datos_grafico,
        distribucion_industria=distribucion_industria,
        crecimiento_yoy=crecimiento_yoy,
        crecimiento_anual=DatosDashboard.CRECIMIENTO_ANUAL,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        ventas_por_region=ventas_por_region,
        tendencias_industria=tendencias_industria,
        pipeline_ventas=pipeline_ventas,
        aliados_extendidos=aliados_extendidos,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/dashboard/performance')
@login_required
def dashboard_performance():
    # Data for performance dashboard
    proyectos = Proyecto.PROYECTOS
    consultores = Consultor.CONSULTORES

    proyectos_activos = len(
        [p for p in proyectos if p.etapa in ['planificacion', 'ejecucion']])
    consultores_activos = len(consultores)

    # Mock tasa de conversión and ciclo promedio de ventas
    tasa_conversion = 65  # percentage
    ciclo_promedio_ventas = 45  # days

    kpis = {
        'proyectos_activos': proyectos_activos,
        'consultores_activos': consultores_activos,
        'tasa_conversion': tasa_conversion,
        'ciclo_promedio_ventas': ciclo_promedio_ventas
    }

    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        proyectos_extendidos = DatosDemoCompleto.PROYECTOS_EXTENDIDOS
        resultados_proyectos = DatosDemoCompleto.RESULTADOS_PROYECTOS
        consultores_extendidos = DatosDemoCompleto.CONSULTORES_EXTENDIDOS
        matriz_competencias = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'matriz_competencias']
        proyectos_por_etapa = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'proyectos_por_etapa']
        app.logger.info("Usando datos extendidos para dashboard de desempeño")
    else:
        # Usar datos estándar
        proyectos_extendidos = None
        resultados_proyectos = None
        consultores_extendidos = None
        matriz_competencias = None
        proyectos_por_etapa = None
        app.logger.info("Usando datos estándar para dashboard de desempeño")

    return render_template(
        'dashboard/performance.html',
        title='Dashboard de Desempeño',
        kpis=kpis,
        funnel_proyectos=DatosDashboard.FUNNEL_PROYECTOS,
        actividades_planificadas=DatosDashboard.ACTIVIDADES_PLANIFICADAS,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        proyectos_extendidos=proyectos_extendidos,
        resultados_proyectos=resultados_proyectos,
        consultores_extendidos=consultores_extendidos,
        matriz_competencias=matriz_competencias,
        proyectos_por_etapa=proyectos_por_etapa,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/dashboard/community')
@login_required
def dashboard_community():
    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        desarrollo_profesional = DatosDemoCompleto.DESARROLLO_PROFESIONAL
        metricas_comunidad = DatosDemoCompleto.METRICAS_COMUNIDAD
        consultores_extendidos = DatosDemoCompleto.CONSULTORES_EXTENDIDOS
        evaluaciones_consultores = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'evaluaciones_consultores']
        app.logger.info("Usando datos extendidos para dashboard de comunidad")
    else:
        # Usar datos estándar
        desarrollo_profesional = None
        metricas_comunidad = None
        consultores_extendidos = None
        evaluaciones_consultores = None
        app.logger.info("Usando datos estándar para dashboard de comunidad")

    return render_template(
        'dashboard/community.html',
        title='Dashboard de Comunidad',
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        desarrollo_profesional=desarrollo_profesional,
        metricas_comunidad=metricas_comunidad,
        consultores_extendidos=consultores_extendidos,
        evaluaciones_consultores=evaluaciones_consultores,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/aliados/cuentas')
@login_required
def aliados_cuentas():
    aliados = Aliado.ALIADOS

    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        aliados_extendidos = DatosDemoCompleto.ALIADOS_EXTENDIDOS
        ventas_por_region = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'ventas_por_region']
        app.logger.info("Usando datos extendidos para cuentas de aliados")
    else:
        # Usar datos estándar
        aliados_extendidos = None
        ventas_por_region = None
        app.logger.info("Usando datos estándar para cuentas de aliados")

    return render_template(
        'aliados/cuentas.html',
        title='Cuentas de Aliados',
        aliados=aliados,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        aliados_extendidos=aliados_extendidos,
        ventas_por_region=ventas_por_region,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/aliados/portfolio')
@login_required
def aliados_portfolio():
    proyectos = Proyecto.PROYECTOS
    aliados = {aliado.id: aliado for aliado in Aliado.ALIADOS}

    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        proyectos_extendidos = DatosDemoCompleto.PROYECTOS_EXTENDIDOS
        resultados_proyectos = DatosDemoCompleto.RESULTADOS_PROYECTOS
        proyectos_por_etapa = DatosDemoCompleto.DATOS_DASHBOARD_EXTENDIDOS[
            'proyectos_por_etapa']
        app.logger.info("Usando datos extendidos para portafolio de proyectos")
    else:
        # Usar datos estándar
        proyectos_extendidos = None
        resultados_proyectos = None
        proyectos_por_etapa = None
        app.logger.info("Usando datos estándar para portafolio de proyectos")

    return render_template(
        'aliados/portfolio.html',
        title='Portafolio de Proyectos',
        proyectos=proyectos,
        aliados=aliados,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        proyectos_extendidos=proyectos_extendidos,
        resultados_proyectos=resultados_proyectos,
        proyectos_por_etapa=proyectos_por_etapa,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/aliados/asignaciones')
@login_required
def aliados_asignaciones():
    consultores = Consultor.CONSULTORES
    proyectos = {proyecto.id: proyecto for proyecto in Proyecto.PROYECTOS}

    # Datos estándar o extendidos según disponibilidad
    if USAR_DATOS_EXTENDIDOS:
        # Usar datos extendidos para visualizaciones más completas
        consultores_extendidos = DatosDemoCompleto.CONSULTORES_EXTENDIDOS
        proyectos_extendidos = DatosDemoCompleto.PROYECTOS_EXTENDIDOS
        desarrollo_profesional = DatosDemoCompleto.DESARROLLO_PROFESIONAL
        app.logger.info(
            "Usando datos extendidos para asignaciones de consultores")
    else:
        # Usar datos estándar
        consultores_extendidos = None
        proyectos_extendidos = None
        desarrollo_profesional = None
        app.logger.info(
            "Usando datos estándar para asignaciones de consultores")

    return render_template(
        'aliados/asignaciones.html',
        title='Asignaciones de Consultores',
        consultores=consultores,
        proyectos=proyectos,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        consultores_extendidos=consultores_extendidos,
        proyectos_extendidos=proyectos_extendidos,
        desarrollo_profesional=desarrollo_profesional,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    # Para páginas de error, no hay usuario autenticado, por lo que pasamos role=None
    return render_template('404.html',
                           title='Página no encontrada',
                           config=app.config,
                           role=None), 404


@app.errorhandler(500)
def internal_server_error(e):
    # Para páginas de error, no hay usuario autenticado, por lo que pasamos role=None
    return render_template('500.html',
                           title='Error interno del servidor',
                           config=app.config,
                           role=None), 500
