# Applying changes to the original code to add routes for project management and details.
from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import current_user
from functools import reduce
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from models import User, Aliado, Proyecto, Consultor, DatosDashboard
from models import Usuario, Organizaciones, Industria, Colaborador
from config import Config
from graphs import *
from datetime import datetime
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
            # Redirigir según el rol del usuario
            if user.role == 'consultor':
                return redirect(url_for('consultor_perfil'))
            else:
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
    if current_user.role == 'supervisor':
        # Obtener proyectos y agrupar por estado
        proyectos = Proyecto.PROYECTOS
        estados = {
            'oportunidad': [p for p in proyectos if p.etapa == 'oportunidad'],
            'propuesta': [p for p in proyectos if p.etapa == 'propuesta'],
            'aprobacion': [p for p in proyectos if p.etapa == 'aprobado'],
            'desarrollo': [p for p in proyectos if p.etapa == 'desarrollo'],
            'testing': [p for p in proyectos if p.etapa == 'testing'],
            'cierre': [p for p in proyectos if p.etapa == 'cierre'],
            'evaluacion': [p for p in proyectos if p.etapa == 'evaluacion'],
            'finalizados': [p for p in proyectos if p.etapa == 'finalizado']
        }
        return render_template('dashboard/supervisor.html', title='Gestión de Proyectos', config=app.config, role=current_user.role, estados=estados)
    elif current_user.role == 'aliado':
        return render_template('dashboard/growth_overview.html', title='Dashboard de Crecimiento', config=app.config, role=current_user.role)
    return redirect(url_for('dashboard_growth'))

@app.route('/dashboard/crecimiento')
@login_required
def dashboard_crecimiento():
    if current_user.role != 'aliado':
        return redirect(url_for('dashboard_growth'))

    # Datos para las gráficas
    datos_ingresos_costos = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'ingresos': [50000, 55000, 58000, 54000, 62000, 65000],
        'costos': [30000, 32000, 35000, 33000, 36000, 38000]
    }

    datos_clientes = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'clientes_nuevos': [10, 12, 8, 15, 11, 14],
        'clientes_recurrentes': [45, 47, 46, 48, 50, 52]
    }

    datos_rentabilidad = {
        'servicios': ['Consultoría', 'Desarrollo', 'Análisis', 'Soporte'],
        'ingresos': [100000, 80000, 60000, 40000],
        'margenes': [0.35, 0.28, 0.42, 0.25],
        'volumen': [30, 25, 20, 15],
        'rentabilidad': [35000, 22400, 25200, 10000]
    }

    return render_template('dashboard/growth.html', 
                         title='Dashboard de Crecimiento',
                         config=app.config,
                         role=current_user.role,
                         ingresos_vs_costos=generar_grafico_ingresos_vs_costos(datos_ingresos_costos),
                         crecimiento_yoy=generar_grafico_crecimiento_yoy(DatosDashboard.CRECIMIENTO_ANUAL),
                         clientes_nuevos_recurrentes=generar_grafico_clientes_nuevos_vs_recurrentes(datos_clientes),
                         rentabilidad=generar_grafico_rentabilidad(datos_rentabilidad))


@app.route('/consultor/perfil')
@login_required
def consultor_perfil():
    return render_template('consultor/perfil.html',
                         title='Perfil del Consultor',
                         config=app.config,
                         role=current_user.role)

@app.route('/dashboard/growth')
@login_required
def dashboard_growth():
    if current_user.role == 'supervisor':
        return redirect(url_for('dashboard'))

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
    crecimiento_yoy = generar_grafico_crecimiento_yoy(
        DatosDashboard.CRECIMIENTO_ANUAL)

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

    # Generar gráficos
    radar_chart = generar_grafico_desempeno_estrategico()
    funnel_chart = generar_grafico_funnel_proyectos(
        DatosDashboard.FUNNEL_PROYECTOS)

    return render_template(
        'dashboard/performance.html',
        title='Dashboard de Desempeño',
        kpis=kpis,
        funnel_proyectos=DatosDashboard.FUNNEL_PROYECTOS,
        actividades_planificadas=DatosDashboard.ACTIVIDADES_PLANIFICADAS,
        radar_chart=radar_chart,
        config=app.config,
        role=current_user.role,
        # Nuevos datos extendidos
        proyectos_extendidos=proyectos_extendidos,
        resultados_proyectos=resultados_proyectos,
        consultores_extendidos=consultores_extendidos,
        matriz_competencias=matriz_competencias,
        proyectos_por_etapa=proyectos_por_etapa,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


@app.route('/dashboard/proyectos')
@login_required
def dashboard_proyectos():
    # Datos de ejemplo para las gráficas
    datos_proyectos_activos = {
        'etapas': ['Planificación', 'Desarrollo', 'Pruebas', 'Implementación'],
        'cantidad': [5, 8, 3, 4]
    }

    datos_pipeline = {
        'etapas': ['Contacto', 'Propuesta', 'Negociación', 'Cierre'],
        'cantidad': [20, 12, 8, 5],
        'valor': [200000, 150000, 100000, 80000]
    }

    datos_desempeno = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'avance': [85, 60, 92, 45],
        'calidad': [90, 85, 95, 80],
        'satisfaccion': [88, 75, 90, 85]
    }

    datos_tiempos = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'estimado': [45, 30, 60, 90],
        'real': [50, 35, 58, 95]
    }

    return render_template(
        'dashboard/proyectos.html',
        title='Dashboard de Proyectos',
        config=app.config,
        role=current_user.role,
        proyectos_activos=generar_grafico_proyectos_activos(datos_proyectos_activos),
        pipeline_oportunidades=generar_grafico_pipeline(datos_pipeline),
        desempeno_proyecto=generar_grafico_desempeno_proyectos(datos_desempeno),
        tiempos_comparacion=generar_grafico_tiempos(datos_tiempos)
    )

@app.route('/dashboard/productividad')
@login_required
def dashboard_productividad():
    # Datos de ejemplo para las gráficas
    datos_consultores_proyecto = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'consultores': [4, 3, 5, 2]
    }

    datos_horas_progreso = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'horas': [120, 80, 160, 40],
        'progreso': [85, 60, 95, 30]
    }

    datos_eficiencia = {
        'consultores': ['Ana S.', 'Carlos M.', 'Laura P.', 'Juan D.', 'María R.'],
        'eficiencia': [95, 92, 88, 85, 82],
        'tareas_completadas': [45, 42, 38, 36, 34],
        'horas_promedio': [6.5, 7.0, 7.8, 8.2, 8.5]
    }

    datos_tareas = {
        'consultores': ['Ana S.', 'Carlos M.', 'Laura P.', 'Juan D.', 'María R.'],
        'completadas': [45, 42, 38, 36, 34],
        'en_progreso': [5, 8, 7, 4, 6],
        'pendientes': [2, 3, 4, 5, 3]
    }

    return render_template(
        'dashboard/productividad.html',
        title='Dashboard de Productividad',
        config=app.config,
        role=current_user.role,
        consultores_proyecto=generar_grafico_consultores_proyecto(datos_consultores_proyecto),
        horas_vs_progreso=generar_grafico_horas_vs_progreso(datos_horas_progreso),
        consultores_eficientes=generar_grafico_consultores_eficientes(datos_eficiencia),
        tareas_completadas=generar_grafico_tareas_completadas(datos_tareas)
    )

@app.route('/dashboard/facturacion')
@login_required
def dashboard_facturacion():
    # Datos de ejemplo para las gráficas
    datos_facturacion = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'facturacion': [120000, 135000, 115000, 140000, 125000, 145000],
        'anual': [1450000, 1600000, 1750000, 1900000]
    }

    datos_deudas = {
        'clientes': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
        'por_cobrar': [45000, 32000, 28000, 15000, 22000],
        'vencido': [15000, 8000, 12000, 5000, 7000],
        'dias_vencimiento': [45, 30, 60, 15, 25]
    }

    datos_rentabilidad = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'ingresos': [180000, 150000, 120000, 90000],
        'costos': [126000, 112500, 84000, 72000],
        'margen': [30, 25, 30, 20]
    }

    datos_flujo = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'ingresos': [150000, 165000, 145000, 170000, 155000, 175000],
        'egresos': [120000, 135000, 115000, 140000, 125000, 145000],
        'neto': [30000, 30000, 30000, 30000, 30000, 30000]
    }

    return render_template(
        'dashboard/facturacion.html',
        title='Dashboard de Facturación',
        config=app.app.config,
        role=current_user.role,
        facturacion_mensual=generar_grafico_facturacion(datos_facturacion),
        deudas_cobros=generar_grafico_deudas(datos_deudas),
        rentabilidad_proyecto=generar_grafico_rentabilidad_proyecto(datos_rentabilidad),
        flujo_caja=generar_grafico_flujo_caja(datos_flujo)
    )

@app.route('/cuentas/clientes')
@login_required
def cuentas_clientes():
    return render_template('cuentas/clientes.html',
                         title='Gestión de Clientes',
                         config=app.config,
                         role=current_user.role)

@app.route('/cuentas/usuarios')
@login_required
def cuentas_usuarios():
    users = User.USERS
    return render_template('cuentas/usuarios.html',
                         title='Gestión de Usuarios',
                         users=users,
                         config=app.config,
                         role=current_user.role)

@app.route('/dashboard/riesgos')
@login_required
def dashboard_riesgos():
    # Datos de ejemplo para las gráficas
    datos_matriz = {
        'severidad': [[9, 6, 3], [6, 4, 2], [3, 2, 1]],
        'impacto': ['Alto', 'Medio', 'Bajo'],
        'probabilidad': ['Alta', 'Media', 'Baja'],
        'valores': [['Alto', 'Alto-Medio', 'Medio'], 
                   ['Alto-Medio', 'Medio', 'Bajo-Medio'],
                   ['Medio', 'Bajo-Medio', 'Bajo']]
    }

    datos_proyectos = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'nivel_riesgo': [85, 65, 45, 25],
        'estado': ['Bloqueado', 'En Riesgo', 'Atención', 'Normal'],
        'colores': ['#FF0000', '#FFA500', '#FFFF00', '#00FF00']
    }

    datos_historial = {
        'fechas': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'problemas_reportados': [12, 15, 10, 8, 13, 9],
        'problemas_resueltos': [10, 13, 9, 7, 11, 8]
    }

    datos_alertas = {
        'tiempo': ['9:00', '10:30', '11:45', '13:15', '14:30'],
        'severidad': [5, 3, 4, 2, 1],
        'mensaje': ['Error Crítico', 'Advertencia', 'Error Mayor', 'Info', 'Debug'],
        'impacto': [25, 15, 20, 10, 5],
        'colores': ['#FF0000', '#FFA500', '#FF4444', '#00A0FF', '#00FF00']
    }

    return render_template(
        'dashboard/riesgos.html',
        title='Dashboard de Riesgos',
        config=app.config,
        role=current_user.role,
        matriz_riesgos=generar_matriz_riesgos(datos_matriz),
        proyectos_riesgo=generar_grafico_proyectos_riesgo(datos_proyectos),
        historial_problemas=generar_historial_problemas(datos_historial),
        alertas_tiempo_real=generar_alertas_tiempo_real(datos_alertas)
    )

def dashboard_facturacion():
    # Datos de ejemplo para las gráficas
    datos_facturacion = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'facturacion': [120000, 135000, 115000, 140000, 125000, 145000],
        'anual': [1450000, 1600000, 1750000, 1900000]
    }

    datos_deudas = {
        'clientes': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
        'por_cobrar': [45000, 32000, 28000, 15000, 22000],
        'vencido': [15000, 8000, 12000, 5000, 7000],
        'dias_vencimiento': [45, 30, 60, 15, 25]
    }

    datos_rentabilidad = {
        'proyectos': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D'],
        'ingresos': [180000, 150000, 120000, 90000],
        'costos': [126000, 112500, 84000, 72000],
        'margen': [30, 25, 30, 20]
    }

    datos_flujo = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'ingresos': [150000, 165000, 145000, 170000, 155000, 175000],
        'egresos': [120000, 135000, 115000, 140000, 125000, 145000],
        'neto': [30000, 30000, 30000, 30000, 30000, 30000]
    }

    return render_template(
        'dashboard/facturacion.html',
        title='Dashboard de Facturación',
        config=app.config,
        role=current_user.role,
        facturacion_mensual=generar_grafico_facturacion(datos_facturacion),
        deudas_cobros=generar_grafico_deudas(datos_deudas),
        rentabilidad_proyecto=generar_grafico_rentabilidad_proyecto(datos_rentabilidad),
        flujo_caja=generar_grafico_flujo_caja(datos_flujo)
    )

@app.route('/dashboard/cuentas')
@login_required
def dashboard_cuentas():
    # Datos de ejemplo para las gráficas
    datos_segmentacion = {
        'segmentos': ['Premium', 'Business', 'Standard', 'Basic'],
        'cantidad': [15, 30, 40, 25],
        'colores': ['#560591', '#D400AC', '#00A0FF', '#000000']
    }

    datos_clv = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'premium': [5000, 5200, 5400, 5600, 5800, 6000],
        'business': [3000, 3100, 3300, 3400, 3600, 3800],
        'standard': [1500, 1600, 1700, 1800, 1900, 2000]
    }

    datos_retencion = {
        'meses': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'tasa_retencion': [95, 93, 94, 92, 95, 96]
    }

    datos_satisfaccion = {
        'nps_categorias': ['Promotores', 'Pasivos', 'Detractores'],
        'nps_valores': [70, 20, 10],
        'calificacion': 4.5,
        'tendencia': [4.2, 4.3, 4.4, 4.5, 4.5, 4.5]
    }

    return render_template(
        'dashboard/cuentas.html',
        title='Dashboard de Cuentas',
        config=app.config,
        role=current_user.role,
        segmentacion_clientes=generar_grafico_segmentacion_clientes(datos_segmentacion),
        clv_trend=generar_grafico_clv(datos_clv),
        retencion_clientes=generar_grafico_retencion(datos_retencion),
        satisfaccion_clientes=generar_grafico_satisfaccion(datos_satisfaccion)
    )

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


@app.route('/aliados/usuarios')
@login_required
def aliados_usuarios():
    users = User.get_all_users() if hasattr(User, 'get_all_users') else []
    industrias = Industria.get_all()
    organizaciones = Usuario.get_organizaciones()
    return render_template('aliados/usuarios.html',
                         title='Gestión de Usuarios',
                         industrias=industrias,
                         organizaciones=organizaciones,
                         users=users,
                         config=app.config,
                         role=current_user.role)

@app.route('/api/usuarios', methods=['POST'])
@login_required
def create_user():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        tipo = data.get('tipo')
        print(f"Tipo de usuario: {tipo}")

        if tipo == 'gestor':
            nuevo_usuario = Usuario(data.get('nombre_completo'), data.get('nombre_organizacion'),  data.get('correo'), "Dnova%2025", 2, "activo", None)
            id_usuario = nuevo_usuario.create()

        elif tipo == 'aliado':
            fecha_registro = datetime.now().strftime('%y/%m/%d %H:%M:%S')
            correo = data.get('correo')
            
            nuevo_usuario = Usuario(data.get('nombre_completo'), data.get('nombre_organizacion'), correo, "Dnova%2025", 1, "activo", None)
            id_usuario = nuevo_usuario.create()

            nuevo_aliado = Organizaciones(id_usuario, data.get('region'), data.get('industria'), fecha_registro, "activo", data.get('contacto_principal'), data.get('tamano'), data.get('empleados'), data.get('direccion'), data.get('ciudad'), data.get('estado_dir'), data.get('codigo_postal'), data.get('pais'))
            nuevo_aliado.create()

        elif tipo == 'empleado':
            print("Datos del empleado:")
            print(f"  - Nombre: {data.get('nombre')}")
            print(f"  - Email: {data.get('email')}")
            print(f"  - Teléfono: {data.get('telefono')}")
            print(f"  - Puesto: {data.get('puesto')}")
            print(f"  - Departamento: {data.get('departamento')}")
            print(f"  - Salario: {data.get('salario')}")

        return jsonify({'status': 'success', 'message': 'Usuario creado exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/usuarios-cuentas', methods=['POST'])
@login_required
def create_usuario_cuenta():
    try:
        data = request.get_json()
        print(f"Datos recibidos para usuario de cuenta: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        print("Datos del usuario:")
        print(f"  - Nombre: {data.get('nombre')}")
        print(f"  - Correo: {data.get('correo')}")
        print(f"  - Cargo: {data.get('cargo')}")
        print(f"  - Rol Laboral: {data.get('rol_laboral')}")

        return jsonify({'status': 'success', 'message': 'Usuario de cuenta creado exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear usuario de cuenta: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
@login_required
def create_cliente():
    try:
        data = request.get_json()
        print(f"Datos recibidos para cliente: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        print("Datos del cliente:")
        print(f"  - Nombre: {data.get('nombre')}")
        print(f"  - Industria: {data.get('industria')}")
        print(f"  - Región: {data.get('region')}")
        print(f"  - Código: {data.get('codigo')}")
        print(f"  - Sector: {data.get('sector')}")

        return jsonify({'status': 'success', 'message': 'Cliente creado exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear cliente: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/informacion-personal', methods=['POST'])
@login_required
def update_informacion_personal():
    try:
        data = request.get_json()

        # Imprimir el JSON completo recibido
        print("=" * 60)
        print("📥 DATOS JSON RECIBIDOS EN /api/informacion-personal")
        print("=" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=" * 60)

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        # Extraer los datos del formulario
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')
        linkedin = data.get('linkedin')
        especialidad = data.get('especialidad')
        nivel = data.get('nivel')
        direccion = data.get('direccion')
        ciudad = data.get('ciudad')
        codigo_postal = data.get('codigo_postal')
        pais = data.get('pais')
        tarifa_hora = data.get('tarifa_hora')
        resumen = data.get('resumen')

        print("Datos de información personal:")
        print(f"  - Nombre: {nombre}")
        print(f"  - Email: {email}")
        print(f"  - Teléfono: {telefono}")
        print(f"  - LinkedIn: {linkedin}")
        print(f"  - Especialidad: {especialidad}")
        print(f"  - Nivel: {nivel}")
        print(f"  - Dirección: {direccion}")
        print(f"  - Ciudad: {ciudad}")
        print(f"  - Código Postal: {codigo_postal}")
        print(f"  - País: {pais}")
        print(f"  - Tarifa por hora: {tarifa_hora}")
        print(f"  - Resumen: {resumen}")

        # Validaciones básicas
        if not nombre or not email:
            return jsonify({'status': 'error', 'message': 'Nombre y email son campos obligatorios'}), 400

        # Aquí podrías agregar la lógica para actualizar la base de datos
        # Por ejemplo: current_user.update_profile(data)

        return jsonify({
            'status': 'success', 
            'message': 'Información personal actualizada exitosamente',
            'data': {
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'linkedin': linkedin,
                'especialidad': especialidad,
                'nivel': nivel,
                'direccion': direccion,
                'ciudad': ciudad,
                'codigo_postal': codigo_postal,
                'pais': pais,
                'tarifa_hora': tarifa_hora,
                'resumen': resumen
            }
        })

    except Exception as e:
        app.logger.error(f"Error al actualizar información personal: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/experiencia-laboral', methods=['POST'])
@login_required
def create_experiencia_laboral():
    try:
        data = request.get_json()

        # Imprimir el JSON completo recibido
        print("=" * 60)
        print("📥 DATOS JSON RECIBIDOS EN /api/experiencia-laboral")
        print("=" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=" * 60)

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        # Extraer los datos del formulario de experiencia laboral
        puesto = data.get('puesto')
        empresa = data.get('empresa')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        trabajo_actual = data.get('trabajo_actual', False)
        ubicacion = data.get('ubicacion')
        descripcion = data.get('descripcion')
        tipo_empleo = data.get('tipo_empleo')  # tiempo_completo, medio_tiempo, freelance, contrato
        sector = data.get('sector')
        logros = data.get('logros', [])  # Lista de logros específicos

        print("📋 DATOS PROCESADOS:")
        print(f"  - Puesto: {puesto}")
        print(f"  - Empresa: {empresa}")
        print(f"  - Fecha Inicio: {fecha_inicio}")
        print(f"  - Fecha Fin: {fecha_fin}")
        print(f"  - Trabajo Actual: {trabajo_actual}")
        print(f"  - Ubicación: {ubicacion}")
        print(f"  - Descripción: {descripcion}")
        print(f"  - Tipo de Empleo: {tipo_empleo}")
        print(f"  - Sector: {sector}")
        print(f"  - Logros: {logros}")

        # Validaciones básicas
        if not puesto or not empresa or not fecha_inicio:
            return jsonify({'status': 'error', 'message': 'Puesto, empresa y fecha de inicio son campos obligatorios'}), 400

        # Validar que si no es trabajo actual, debe tener fecha de fin
        if not trabajo_actual and not fecha_fin:
            return jsonify({'status': 'error', 'message': 'Debe especificar fecha de fin o marcar como trabajo actual'}), 400

        # Aquí podrías agregar la lógica para guardar en la base de datos
        # Por ejemplo: current_user.add_work_experience(data)

        # Preparar datos de respuesta
        experiencia_data = {
            'puesto': puesto,
            'empresa': empresa,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin if not trabajo_actual else None,
            'trabajo_actual': trabajo_actual,
            'ubicacion': ubicacion,
            'descripcion': descripcion,
            'tipo_empleo': tipo_empleo,
            'sector': sector,
            'logros': logros,
            'periodo_formateado': f"{fecha_inicio} - {'Presente' if trabajo_actual else fecha_fin}"
        }

        return jsonify({
            'status': 'success', 
            'message': 'Experiencia laboral agregada exitosamente',
            'data': experiencia_data
        })

    except Exception as e:
        app.logger.error(f"Error al crear experiencia laboral: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/proyectos/gestion')
@login_required  
def proyectos_gestion():
    # Datos de ejemplo para los proyectos
    proyectos = [
        {
            'id': 1,
            'nombre': 'Transformación Digital Bancaria',
            'estado': 'En Desarrollo',
            'etapa': 'desarrollo',
            'tiempo_estimado': 960,
            'costos_estimados': 150000,
            'monto': 180000,
            'consultores_asignados': 5,
            'progreso': 65,
            'aliado_id': 'Banco Nacional',
            'fecha_inicio': '2024-01-15',
            'fecha_fin': '2024-07-15'
        },
        {
            'id': 2,
            'nombre': 'Sistema de Gestión Hospitalaria',
            'estado': 'Planificación',
            'etapa': 'planificacion',
            'tiempo_estimado': 1280,
            'costos_estimados': 200000,
            'monto': 250000,
            'consultores_asignados': 7,
            'progreso': 25,
            'aliado_id': 'Hospital Central',
            'fecha_inicio': '2024-02-01',
            'fecha_fin': '2024-10-01'
        },
        {
            'id': 3,
            'nombre': 'E-commerce para Retail',
            'estado': 'Testing',
            'etapa': 'testing',
            'tiempo_estimado': 640,
            'costos_estimados': 80000,
            'monto': 100000,
            'consultores_asignados': 3,
            'progreso': 85,
            'aliado_id': 'Retail Plus',
            'fecha_inicio': '2024-03-01',
            'fecha_fin': '2024-07-01'
        },
        {
            'id': 4,
            'nombre': 'Plataforma de Logística',
            'estado': 'Finalizado',
            'etapa': 'finalizado',
            'tiempo_estimado': 800,
            'costos_estimados': 120000,
            'monto': 140000,
            'consultores_asignados': 4,
            'progreso': 100,
            'aliado_id': 'LogiTech',
            'fecha_inicio': '2023-10-01',
            'fecha_fin': '2024-03-01'
        }
    ]

    return render_template('proyectos/gestion.html',
                         title='Gestión de Proyectos',
                         proyectos=proyectos,
                         config=app.config,
                         role=current_user.role)

@app.route('/api/idiomas', methods=['POST'])
def api_idiomas():
    """Endpoint para recibir e imprimir datos de idiomas"""
    try:
        data = request.get_json()
        print("=== DATOS DE IDIOMAS RECIBIDOS ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=====================================")

        return jsonify({
            'status': 'success',
            'message': 'Datos de idiomas recibidos correctamente',
            'data': data
        })
    except Exception as e:
        print(f"Error al procesar idiomas: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al procesar los datos: {str(e)}'
        }), 400

@app.route('/api/educacion', methods=['POST'])
def api_educacion():
    """Endpoint para recibir e imprimir datos de educación"""
    try:
        data = request.get_json()
        print("=== DATOS DE EDUCACIÓN RECIBIDOS ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=====================================")

        return jsonify({
            'status': 'success',
            'message': 'Datos de educación recibidos correctamente',
            'data': data
        })
    except Exception as e:
        print(f"Error al procesar educación: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al procesar los datos: {str(e)}'
        }), 400

@app.route('/api/certificaciones', methods=['POST'])
def api_certificaciones():
    try:
        data = request.get_json()
        print("=== DATOS DE CERTIFICACIONES RECIBIDOS ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=" * 45)

        # Aquí normalmente guardarías en la base de datos
        # Por ahora solo retornamos éxito
        return jsonify({"status": "success", "message": "Certificación guardada correctamente"})
    except Exception as e:
        print(f"Error en /api/certificaciones: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/proyectos-destacados', methods=['POST'])
def add_proyecto_destacado():
    try:
        data = request.get_json()
        print("📝 Datos del proyecto destacado recibidos:", json.dumps(data, indent=2, ensure_ascii=False))

        # Validar campos requeridos
        required_fields = ['titulo', 'fecha_inicio', 'descripcion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido'})

        return jsonify({'status': 'success', 'message': 'Proyecto destacado agregado correctamente'})

    except Exception as e:
        print(f"❌ Error al procesar proyecto destacado: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error interno del servidor'}), 500

@app.route('/api/habilidades-tecnicas', methods=['POST'])
def add_habilidad_tecnica():
    try:
        data = request.get_json()
        print("🔧 Datos de la habilidad técnica recibidos:", json.dumps(data, indent=2, ensure_ascii=False))

        # Validar campos requeridos
        required_fields = ['nombre', 'nivel', 'porcentaje']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido'})

        # Validar porcentaje
        porcentaje = data.get('porcentaje')
        if not isinstance(porcentaje, int) or porcentaje < 1 or porcentaje > 100:
            return jsonify({'status': 'error', 'message': 'El porcentaje debe ser un número entre 1 y 100'})

        return jsonify({'status': 'success', 'message': 'Habilidad técnica agregada correctamente'})

    except Exception as e:
        print(f"❌ Error al procesar habilidad técnica: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error interno del servidor'}), 500

@app.route('/api/idiomas', methods=['POST'])
def add_idioma():
    try:
        data = request.get_json()
        print("🌐 Datos del idioma recibidos:", json.dumps(data, indent=2, ensure_ascii=False))

        # Validar campos requeridos
        required_fields = ['idioma', 'nivel', 'porcentaje']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido'})

        # Validar porcentaje
        porcentaje = data.get('porcentaje')
        if not isinstance(porcentaje, int) or porcentaje < 1 or porcentaje > 100:
            return jsonify({'status': 'error', 'message': 'El porcentaje debe ser un número entre 1 y 100'})

        return jsonify({'status': 'success', 'message': 'Idioma agregado correctamente'})

    except Exception as e:
        print(f"❌ Error al procesar idioma: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error interno del servidor'}), 500