# Applying changes to the original code to add routes for project management and details.
from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import current_user
from functools import reduce
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from controllers import *
from models import User, Aliado, Proyecto, Consultor, DatosDashboard
from models import Usuario, Organizaciones, Industrias, Colaboradores, Subregiones, Sedes, Regiones, Portafolio, Consultores, Comunidades, Miembros_comunidad, Comunidad_aliado, Personas_cliente, UserAcces, Cuentas, Segmentacion, Casos_uso, Exp_laboral, Educacion, Certificaciones, Proyectos_destacados, Estimaciones, Entregables, Actividades, Tareas, Costos_recursos, Costos_freelance
from config import Config
from graphs import *
from datetime import datetime, date
import logging, json

# region DATOS DEMOSTRACIÓN

try:
    from data_demo import DatosDemoCompleto
    USAR_DATOS_EXTENDIDOS = True
    app.logger.info("Datos de demostración extendidos cargados correctamente")
except ImportError:
    USAR_DATOS_EXTENDIDOS = False
    app.logger.warning(
        "No se pudieron cargar los datos de demostración extendidos")
    
# endregion

# region LOGEO

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, LoginManager

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.rol in roles:
                return f(*args, **kwargs)
            flash('Acceso denegado: no tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('login'))  # o redirigir a un 403
        return wrapper
    return decorator

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = UserAcces.get_by_access(username)
        
        if usuario and UserAcces.check_password(password, usuario[5]):
            user_acces = UserAcces(
                usuario[0],
                usuario[1],
                usuario[2],
                usuario[3],
                usuario[4],
                usuario[5],
                usuario[6],
                usuario[7],
                usuario[8]
            )

            login_user(user_acces)

            if current_user.rol == 'Freelance':
                return redirect(url_for('consultor_perfil'))
            if current_user.rol == "Gestor":
                next_page = request.args.get('next')
                return redirect(next_page or url_for('gestor_organizaciones'))
            if current_user.rol == "Supervisor":
                return redirect(url_for('supervisor_funnel'))
            else:
                return redirect(url_for('dashboard_growth'))
        else:
            flash('Usuario o contraseña inválidos', 'danger')

    return render_template('login.html',
                            title='Iniciar Sesión',
                            config=app.config,
                            rol=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# endregion

# region GESTOR

@app.route('/gestor/usuarios')
@login_required
@role_required('Gestor')
def aliados_usuarios():
    users = User.get_all_users() if hasattr(User, 'get_all_users') else []
    industrias = Industrias.get_all()
    regiones = Subregiones.get_all()
    sedes = Sedes.get_all()
    organizaciones = Organizaciones.get_all()
    tabla_usuarios = Usuario.get_table_users()
    return render_template('gestor/usuarios.html',
                         title='Gestión de Usuarios',
                         tabla_usuarios=tabla_usuarios,
                         industrias=industrias,
                         regiones=regiones,
                         sedes=sedes,
                         organizaciones=organizaciones,
                         users=users,
                         config=app.config,
                         rol=current_user.rol)

@app.route('/gestor/organizaciones')
@login_required
@role_required('Gestor')
def gestor_organizaciones():
    industrias = Industrias.get_all()
    regiones = Subregiones.get_all()
    organizaciones = Organizaciones.get_all()
    table_orgs = Organizaciones.get_table_orgs()
    regiones = Regiones.get_all()
    subregiones = Subregiones.get_all()
    return render_template('gestor/organizaciones.html',
                         title='Gestión de Aliados',
                         subregiones=subregiones,
                         table_orgs=table_orgs,
                         industrias=industrias,
                         regiones=regiones,
                         organizaciones=organizaciones,
                         config=app.config,
                         rol=current_user.rol)

@app.route('/gestor/portfolio')
@login_required
@role_required('Gestor')
def gestor_portfolio():
    portafolio = Portafolio.get_all()
    return render_template('gestor/portfolio.html',
                         title='Portafolio',
                         portafolio=portafolio,
                         config=app.config,
                         rol=current_user.rol)

@app.route('/gestor/asignaciones')
@login_required
@role_required('Gestor')
def gestor_asignaciones():
    consultores = Usuario.get_tbl_consultores()
    aliados = Sedes.get_orgs()
    comunidades = Comunidades.get_all()
    proyectos = {p.id: p for p in Proyecto.PROYECTOS}
    casos_uso_e = Comunidad_aliado.get_asignaciones_estrategicas()
    casos_uso_o = Comunidad_aliado.get_asignaciones_operativas()
    return render_template('gestor/asignaciones.html',
                         title='Asignaciones de Consultores',
                         casos_uso_e=casos_uso_e,
                         casos_uso_o=casos_uso_o,
                         consultores=consultores,
                         comunidades=comunidades,
                         aliados=aliados,
                         proyectos=proyectos,
                         config=app.config,
                         rol=current_user.rol)

# endregion

# region ALIADO

@app.route('/proyectos/general')
@login_required
@role_required('Aliado')
def proyectos_general():
    proyectos = Casos_uso.get_projects(current_user.sede)
    estados = {
        'oportunidad': [p for p in proyectos if str(p['estado']) == "1"],
        'propuesta': [p for p in proyectos if str(p['estado']) == "2"],
        'aprobado': [p for p in proyectos if str(p['estado']) == "3"],
        'desarrollo': [p for p in proyectos if str(p['estado']) == '4'],
        'testing': [p for p in proyectos if str(p['estado']) == '5'],
        'cierre': [p for p in proyectos if str(p['estado']) == '6'],
        'evaluacion': [p for p in proyectos if str(p['estado']) == '7'],
        'finalizados': [p for p in proyectos if str(p['estado']) == '8']
    }
    cuentas = Cuentas.get_cuentas_by_aliado(current_user.organizacion)
    consultores = Personas_cliente.get_consultores_aliado(current_user.sede)
    return render_template('aliados/general.html',
                         title='Gestión de Proyectos',
                         cuentas=cuentas,
                         proyectos=proyectos,
                         estados=estados,
                         consultores=consultores,
                         config=app.config,
                         rol=current_user.rol)

@app.route('/cuentas/clientes')
@login_required
def cuentas_clientes():
    industrias = Industrias.get_all()
    regiones = Subregiones.get_all()
    segmentacion = Segmentacion.get_all()
    cuentas = Cuentas.get_all_tbl()
    return render_template('aliados/clientes.html',
                         title='Gestión de Clientes',
                         cuentas=cuentas,
                         segmentacion=segmentacion,
                         industrias=industrias,
                         regiones=regiones,
                         config=app.config,
                         rol=current_user.rol)


# endregion

# region SUPERVISOR

@app.route('/supervisor/funnel')
@login_required
def supervisor_funnel():
    if current_user.rol == 'Supervisor':
        # Obtener proyectos y agrupar por estado
        proyectos = Casos_uso.get_projects_to_sup(current_user.id)
        estados = {
            'oportunidad': [p for p in proyectos if str(p[10]) == '1'],
            'propuesta': [p for p in proyectos if str(p[10]) == '2'],
            'aprobacion': [p for p in proyectos if str(p[10]) == '3'],
            'desarrollo': [p for p in proyectos if str(p[10]) == '4'],
            'testing': [p for p in proyectos if str(p[10]) == '5'],
            'cierre': [p for p in proyectos if str(p[10]) == '6'],
            'evaluacion': [p for p in proyectos if str(p[10]) == '7'],
            'finalizados': [p for p in proyectos if str(p[10]) == '8']
        }
        return render_template('supervisor/supervisor.html', 
                               title='Gestión de Proyectos', 
                               config=app.config,
                               proyectos=proyectos,
                               rol=current_user.rol, 
                               estados=estados)
    
    elif current_user.rol == 'Aliado':
        return render_template('dashboard/growth_overview.html', title='Dashboard de Crecimiento', config=app.config, rol=current_user.rol)
    return redirect(url_for('dashboard_growth'))

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
                         rol=current_user.rol)

@app.route('/proyectos/calculadora', methods=['GET'])
@login_required
def proyectos_calculadora():
    proyectos = Casos_uso.get_projects_to_sup(current_user.id)
    return render_template('supervisor/calculadora.html',
                         title='Calculadora de Tiempos',
                         proyectos=proyectos,
                         config=app.config,
                         rol=current_user.rol)


# endregion

# region CONSULTOR

@app.route('/consultor/perfil')
@login_required
def consultor_perfil():
    id = current_user.id

    usuario = Usuario.get_by_id(id)
    consultor = Consultores.get_by_id(id)
    exp_lab = Exp_laboral.get_by_id_usuario(id)
    educacion = Educacion.get_by_id_usuario(id)
    certificaciones = Certificaciones.get_by_id_usuario(id)
    pro_destacados = Proyectos_destacados.get_by_id_usuario(id)
    tecnologias = [{'id': x['id'], 'tecs':list_tecs(x['tecnologias_usadas'])} for x in pro_destacados]
    return render_template('consultor/perfil.html',
                         title='Perfil del Consultor',
                         certificaciones=certificaciones,
                         pro_destacados=pro_destacados,
                         educacion=educacion,
                         tecnologias=tecnologias,
                         usuario=usuario,
                         exp_lab=exp_lab,
                         consultor=consultor,
                         config=app.config,
                         rol=current_user.rol)

# endregion

# region CAMBIO DE ROL

@app.route('/cambio_rol')
@login_required
@role_required('Supervisor', 'Freelance')
def cambio_rol():
    try:
        role = current_user.rol
        
        if role == 'Freelance':
            Usuario.update_rol(current_user.id, 3)
            flash("Rol cambiado a Consultor.", "success")
            return redirect(url_for('supervisor_funnel'))

        elif role == 'Supervisor':
            Usuario.update_rol(current_user.id, 4)
            flash("Rol cambiado a Supervisor.", "success")
            return redirect(url_for('consultor_perfil'))

        else:
            flash("Rol actual no admite cambio automático.", "warning")
            return redirect(url_for('dashboard_growth'))

    except Exception as e:
        print(f"❌ Error al cambiar rol: {e}")
        flash("Ocurrió un error al intentar cambiar el rol.", "danger")
        return redirect(url_for('dashboard_growth'))

# endregion

# region Sin definir

@app.route('/cuentas/usuarios')
@login_required
def cuentas_usuarios():
    users = User.USERS
    return render_template('cuentas/usuarios.html',
                         title='Gestión de Usuarios',
                         users=users,
                         config=app.config,
                         rol=current_user.rol)

@app.route('/proyectos/estimaciones')
@login_required
def proyectos_estimaciones():
    # Datos de ejemplo para las estimaciones
    estimaciones = [
        {
            'id': 'EST-001',
            'aliado': 'Aliado Tech',
            'caso_uso': 'Sistema de Gestión de Inventarios para Retail',
            'fecha': '2024-01-15',
            'tipo': 'Desarrollo Completo',
            'horas_estimadas': 320,
            'tarifa_freelance': 45,
            'recursos': '3 Desarrolladores, 1 QA, 1 PM',
            'estado': 'Aprobada'
        },
        {
            'id': 'EST-002',
            'aliado': 'Financiera Global',
            'caso_uso': 'Plataforma de Pagos Móviles',
            'fecha': '2024-01-20',
            'tipo': 'MVP',
            'horas_estimadas': 480,
            'tarifa_freelance': 60,
            'recursos': '4 Desarrolladores, 1 Designer, 1 QA',
            'estado': 'En Revisión'
        },
        {
            'id': 'EST-003',
            'aliado': 'Industrias Este',
            'caso_uso': 'Dashboard de Analytics en Tiempo Real',
            'fecha': '2024-01-25',
            'tipo': 'Prototipo',
            'horas_estimadas': 160,
            'tarifa_freelance': 55,
            'recursos': '2 Desarrolladores Frontend, 1 Data Engineer',
            'estado': 'Pendiente'
        },
        {
            'id': 'EST-004',
            'aliado': 'Consultores Sur',
            'caso_uso': 'Sistema CRM Personalizado',
            'fecha': '2024-02-01',
            'tipo': 'Desarrollo Completo',
            'horas_estimadas': 600,
            'tarifa_freelance': 50,
            'recursos': '5 Desarrolladores, 2 QA, 1 PM, 1 Designer',
            'estado': 'Aprobada'
        },
        {
            'id': 'EST-005',
            'aliado': 'Servicios Oeste',
            'caso_uso': 'Migración a la Nube AWS',
            'fecha': '2024-02-05',
            'tipo': 'Consultoría',
            'horas_estimadas': 120,
            'tarifa_freelance': 75,
            'recursos': '2 Cloud Architects, 1 DevOps Engineer',
            'estado': 'Rechazada'
        },
        {
            'id': 'EST-006',
            'aliado': 'Aliado Tech',
            'caso_uso': 'App Móvil de E-commerce',
            'fecha': '2024-02-10',
            'tipo': 'MVP',
            'horas_estimadas': 280,
            'tarifa_freelance': 42,
            'recursos': '2 Desarrolladores Mobile, 1 Designer',
            'estado': 'En Revisión'
        }
    ]
    
    return render_template('proyectos/estimaciones.html',
                         title='Estimaciones de Proyectos',
                         estimaciones=estimaciones,
                         config=app.config,
                         rol=current_user.rol)

# endregion

# region Dashboards

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
                         rol=current_user.rol,
                         ingresos_vs_costos=generar_grafico_ingresos_vs_costos(datos_ingresos_costos),
                         crecimiento_yoy=generar_grafico_crecimiento_yoy(DatosDashboard.CRECIMIENTO_ANUAL),
                         clientes_nuevos_recurrentes=generar_grafico_clientes_nuevos_vs_recurrentes(datos_clientes),
                         rentabilidad=generar_grafico_rentabilidad(datos_rentabilidad))

@app.route('/dashboard/growth')
@login_required
def dashboard_growth():
    if current_user.rol == 'supervisor':
        return redirect(url_for('dashboard_growth'))

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
        rol=current_user.rol,
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
        rol=current_user.rol,
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
        rol=current_user.rol,
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
        rol=current_user.rol,
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
        rol=current_user.rol,
        facturacion_mensual=generar_grafico_facturacion(datos_facturacion),
        deudas_cobros=generar_grafico_deudas(datos_deudas),
        rentabilidad_proyecto=generar_grafico_rentabilidad_proyecto(datos_rentabilidad),
        flujo_caja=generar_grafico_flujo_caja(datos_flujo)
    )


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
        rol=current_user.rol,
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
        rol=current_user.rol,
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
        rol=current_user.rol,
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
        rol=current_user.rol,
        # Nuevos datos extendidos
        desarrollo_profesional=desarrollo_profesional,
        metricas_comunidad=metricas_comunidad,
        consultores_extendidos=consultores_extendidos,
        evaluaciones_consultores=evaluaciones_consultores,
        usar_datos_extendidos=USAR_DATOS_EXTENDIDOS)


# endregion

# region API

# region API GESTOR

@app.route('/api/usuarios', methods=['POST'])
@login_required
def create_user():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        fecha_actual = datetime.now()
        formato = fecha_actual.strftime('%Y-%m-%d')

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        tipo = data.get('tipo')
        print(f"Tipo de usuario: {tipo}")

        if tipo == 'gestor':
            nuevo_usuario = Usuario(data.get('nombre_completo'), data.get('organizacion'), data.get('sede'), data.get('correo'), 'password', 2, 'activo', None)
            nuevo_usuario.create()

        elif tipo == 'aliado':
            nuevo_usuario = Usuario(data.get('nombre_completo'), data.get('organizacion'), data.get('sede'), data.get('correo'), "password", 1, 'activo', None)
            nuevo_usuario.create()

        elif tipo == 'empleado':
            nuevo_usuario = Usuario(data.get('nombre_completo'), data.get('organizacion'), data.get('sede'), data.get('correo'), "password", 5, 'activo', None)
            id_usuario = nuevo_usuario.create()

            nuevo_colaborador = Colaboradores(id_usuario, data.get('organizacion'), data.get('cargo'), data.get('rol_laboral'))
            nuevo_colaborador.create()
        
        elif tipo == 'freelance':
            nuevo_usuario = Usuario(data.get('nombre_completo'), None, None, data.get('correo'), "password", 4, 'activo', None)
            id = nuevo_usuario.create()

            nuevo_consultor = Consultores(id, data.get('especialidad'), 90, data.get('freelanceNivel'), data.get('freelanceNivel'), formato, None, None, None, None, None, None)
            nuevo_consultor.create()

        return jsonify({'status': 'success', 'message': 'Usuario creado exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/organizaciones', methods=['POST'])
@login_required
def create_organizacion():
    try:
        data = request.get_json()
        print(data)
        # Validar campos mínimos requeridos
        # if not data.get('nombre'):
        #     return jsonify({'status': 'error', 'message': 'El nombre de la organización es requerido'}), 400

        fecha_actual = datetime.now()
        formato = fecha_actual.strftime('%Y-%m-%d')

        if data.get('tipo') == 'organizacion':
            # Crear organización
            nueva_organizacion = Organizaciones(
                data.get('nombre'),
                data.get('industria'),
                formato,
                data.get('estado'),
                data.get('contacto'),
                data.get('tamano'),
                data.get('empleados')
            )
            id_org = nueva_organizacion.create()

            # Crear sede principal
            nueva_sede = Sedes(
                id_org,
                data.get('nombreSede'),
                data.get('region'),
                data.get('direccion'),
                data.get('ciudad'),
                data.get('codigo_postal'),
                data.get('pais')
            )
            nueva_sede.create()

        elif data.get('tipo') == "sede":
            # Crear sede
            nueva_sede = Sedes(
                data.get('organizacion'),
                data.get('nombreSede'),
                data.get('region'),
                data.get('direccion'),
                data.get('ciudad'),
                data.get('codigo_postal'),
                data.get('pais')
            )
            nueva_sede.create()

        return jsonify({'status': 'success', 'message': 'Organización creada exitosamente'})

    except Exception as e:
        print('Error al crear la organización:', str(e))
        return jsonify({
            'status': 'error',
            'message': 'Hubo un error al procesar la solicitud',
            'details': str(e)
        }), 500

@app.route('/api/productos', methods=['POST'])
@login_required
def create_producto():
    try:
        fecha_actual = datetime.now()
        formato = fecha_actual.strftime('%Y-%m-%d')
        data = request.get_json()

        print('📥 Datos recibidos:', data)

        nuevo_producto = Portafolio(
            data.get('nombre'),
            data.get('categoria'),
            data.get('familia'),
            data.get('descripcion'),
            data.get('tipo'),
            data.get('estado'),
            formato,
            None  # fecha_actualizacion inicialmente nula
        )

        nuevo_producto.create()

        return jsonify({'status': 'success', 'message': 'Producto o servicio creado exitosamente'})
    
    except Exception as e:
        print('❌ Error al crear el producto:', str(e))
        return jsonify({'status': 'error', 'message': 'Error al crear el producto o servicio', 'details': str(e)}), 500

@app.route('/api/asignaciones', methods=['POST'])
@login_required
def create_asignacion():
    try:
        data = request.get_json()
        fecha_actual = datetime.now()
        formato = fecha_actual.strftime('%Y-%m-%d')
        print(f"Datos de asignación recibidos: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        tipo = data.get('tipo')

        if tipo == 'freelance':
            
            asignar_freelance = Personas_cliente(data.get('id_sede'), data.get('id_usuario'), data.get('rol_en_cliente'), formato)
            asignar_freelance.create()

        elif tipo == 'comunidad':
            
            nueva_asignacion = Comunidad_aliado(data.get('id_sede'), data.get('id_comunidad'), formato, None)
            nueva_asignacion.create()

        elif tipo == 'crear_comunidad':

            nueva_comunidad = Comunidades(data.get('nombre'), data.get('descripcion'), data.get('tipo_comunidad'))
            id = nueva_comunidad.create()
            miembros = data.get('miembros', [])

            for miembro in miembros:
                nuevo_miembro = Miembros_comunidad(id, miembro.get('usuario'), miembro.get('rol'), formato)
                nuevo_miembro.create()

        return jsonify({'status': 'success', 'message': 'Asignación creada exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear asignación: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# endregion

# region API ALIADO

@app.route('/api/oportunidades', methods=['POST'])
@login_required
def create_oportunidad():
    try:
        data = request.get_json()
        print(f"Datos de oportunidad recibidos: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        cuenta = data.get('cuenta')
        caso_uso = data.get('casoUso')
        descripcion = data.get('descripcion')
        impacto = data.get('impacto')
        usuario = data.get('idSupervisor')

        nuevo_caso_uso = Casos_uso(current_user.sede, usuario, cuenta, caso_uso, descripcion, impacto, None, None, None, 1, None, None, None, None, None, None, None, None)
        nuevo_caso_uso.create()

        print(f"Nueva oportunidad - Cuenta: {cuenta}, Caso de uso: {caso_uso}")
        print(f"Descripción: {descripcion}")
        print(f"Impacto: {impacto}")

        return jsonify({'status': 'success', 'message': 'Oportunidad creada exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear oportunidad: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
@login_required
def create_cliente():
    try:
        data = request.get_json()
        print(f"Datos recibidos para cliente: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        print(f"Datos del cliente: {data}")
        
        nueva_cuenta = Cuentas(current_user.organizacion, data.get('nombre'), data.get('industria'), data.get('region'), None, None, None, data.get('codigo'), data.get('sector'), 'activo')
        nueva_cuenta.create()

        return jsonify({'status': 'success', 'message': 'Cliente creado exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al crear cliente: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/nueva-oportunidad', methods=['POST'])
@login_required
@role_required('Supervisor')
def update_oportunidad():
    try:
        data = request.get_json()
        print(f"Datos de oportunidad recibidos: {data}")

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        proyecto_id = data.get('proyecto_id')
        campo = data.get('campo')
        valor = data.get('valor')

        if campo and valor and proyecto_id:
            Casos_uso.update(campo, valor, proyecto_id)
            return jsonify({'status': 'success', 'message': f'Campo {campo} actualizado'})
        else:
            return jsonify({'status': 'error', 'message': 'Faltan datos en la solicitud'}), 400

    except Exception as e:
        app.logger.error(f"Error al crear oportunidad: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cambio_estado_caso_uso', methods=['POST'])
@login_required
@role_required('Aliado', 'Supervisor')
def cambio_estado_caso_uso():
    try:
        # Obtener datos enviados desde el frontend
        data = request.get_json()
        id_caso = data['id']
        nuevo_estado = data['estado']

        # Consultar estado actual del caso de uso
        estado_actual = Casos_uso.get_by_id(id_caso)

        # Validación de rol: Aliado
        if current_user.rol == "Aliado":
            if estado_actual[10] == '2' and nuevo_estado == 'aprobado':
                Casos_uso.update('estado', '3', id_caso)
            elif estado_actual[10] == '3' and nuevo_estado == 'propuesta':
                Casos_uso.update('estado', '2', id_caso)
            else:
                return jsonify({'error': 'Transición no permitida para Aliado'}), 403

        # Validación de rol: Supervisor
        else:
            if estado_actual[10] == '1' and nuevo_estado == 'propuesta':
                Casos_uso.update('estado', '2', id_caso)
            elif estado_actual[10] == '2' and nuevo_estado == 'oportunidad':
                Casos_uso.update('estado', '1', id_caso)
            else:
                return jsonify({'error': 'Transición no permitida para Supervisor'}), 403

        # Respuesta exitosa
        return jsonify({
            'status': 'ok',
            'message': f'Caso de uso {id_caso} actualizado correctamente.'
        })

    except KeyError as e:
        return jsonify({'error': f'Falta un dato requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

# endregion

# region API SUPERVISOR

@app.route('/api/calculadora', methods=['POST'])
@login_required
@role_required('Supervisor')
def crear_estimacion():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400
        
        id_caso_uso = data.get('projectId')
        caso_uso = data.get('projectName')
        fecha_creacion = date.today()
        usuario = current_user.id

        # Creamos listas con lo que se insertaría en cada tabla
        entregables = []
        actividades = []
        tareas = []

        for ent in data["timeEstimates"]["entregables"]:
            entregables.append({
                "id": ent["id"],
                "id_proyecto": data["projectId"],
                "nombre": ent["name"]
            })
            for act in ent["actividades"]:
                actividades.append({
                    "id": act["id"],
                    "id_entregable": ent["id"],
                    "nombre": act["name"]
                })
                for task in act["tareas"]:
                    tareas.append({
                        "id": task["id"],
                        "id_actividad": act["id"],
                        "nombre": task["name"],
                        "optimista": task["optimistic"],
                        "mas_probable": task["mostLikely"],
                        "pesimista": task["pessimistic"]
                    })

        nueva_estimacion = Estimaciones(id_caso_uso, caso_uso)
        id_estimacion = nueva_estimacion.create()

        # Creación de entregables relacionados con la estimación
        for ent in entregables:
            nuevo_entregable = Entregables(id_estimacion, ent['nombre'], None, None, 9, None, None, 1, fecha_creacion, fecha_creacion, usuario)
            id_entregable = nuevo_entregable.create()

            # Creación de actividades relacionadas a cda entregable
            for act in actividades:
                if ent['id'] == act['id_entregable']:
                    nueva_actividad = Actividades(id_entregable, act['nombre'], None, 9, None, None, None, None, None, None, None, None, fecha_creacion, fecha_creacion, usuario)
                    id_actividad = nueva_actividad.create()

                    # Creación de tareas relacionadas a cada actividad
                    for tra in tareas:
                        if act['id'] == tra['id_actividad']:
                            optimista = tra['optimista']
                            mas_probable = tra['mas_probable']
                            pesimista = tra['pesimista']
                            estimada = (optimista + 4*mas_probable + pesimista) / 6

                            nueva_tarea = Tareas(id_actividad, tra['nombre'], None, 9, None, optimista, mas_probable, pesimista, estimada, None, None, None, None, None, fecha_creacion, fecha_creacion, usuario)

                            nueva_tarea.create()

        resources = data['costs']['resources']['items']
        freelance = data['costs']['freelance']['items']

        for rec in resources:
            nuevo_recurso = Costos_recursos(id_estimacion, rec['type'], rec['concept'], rec['periodicity'], rec['currency'], rec['quantity'], rec['cost'])
            nuevo_recurso.create()

        for fre in freelance:
            nuevo_freelance = Costos_freelance(id_estimacion, fre['specialty'], fre['level'], fre['rate'], fre['activity'], fre['hours'])
            nuevo_freelance.create()

        return jsonify({'status': 'success', 'message': 'Estimación guardada exitosamente'})

    except Exception as e:
        app.logger.error(f"Error al guardar estimación: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# endregion

# region API CONSULTOR

@app.route('/api/informacion-personal', methods=['POST'])
@login_required
def update_informacion_personal():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        # Extraer los datos del formulario
        userId = data.get('userId')
        telefono = data.get('telefono')
        linkedin = data.get('linkedin')
        especialidad = data.get('especialidad')
        nivel = data.get('nivel')
        direccion = data.get('direccion')
        ciudad = data.get('ciudad')
        codigo_postal = data.get('codigo_postal')
        pais = data.get('pais')
        tarifa_hora = data.get('tarifa_hora').replace("$", "").replace("USD", "").strip()
        resumen = data.get('resumen')

        Consultores.update(telefono, linkedin, especialidad, nivel, direccion, ciudad, codigo_postal, pais, tarifa_hora, resumen, userId)

        return jsonify({
            'status': 'success', 
            'message': 'Información personal actualizada exitosamente',
            'data': {
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

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        # Extraer los datos del formulario de experiencia laboral
        puesto = data.get('puesto')
        empresa = data.get('empresa')
        fecha_inicio = data.get('fecha_inicio')
        trabajo_actual = data.get('trabajo_actual', False)
        fecha_fin = data.get('fecha_fin', None)
        ubicacion = data.get('ubicacion')
        descripcion = data.get('descripcion')
        tipo_empleo = data.get('tipo_empleo')  # tiempo_completo, medio_tiempo, freelance, contrato
        sector = data.get('sector')
        logros = data.get('logros', None)  # Lista de logros específicos

        # Validaciones básicas
        if not puesto or not empresa or not fecha_inicio:
            return jsonify({'status': 'error', 'message': 'Puesto, empresa y fecha de inicio son campos obligatorios'}), 400

        # Validar que si no es trabajo actual, debe tener fecha de fin
        if not trabajo_actual and not fecha_fin:
            return jsonify({'status': 'error', 'message': 'Debe especificar fecha de fin o marcar como trabajo actual'}), 400

        nueva_experiencia = Exp_laboral(current_user.id, puesto, empresa, descripcion, fecha_inicio, fecha_fin, ubicacion, tipo_empleo, sector, logros)
        nueva_experiencia.create()

        return jsonify({
            'status': 'success', 
            'message': 'Experiencia laboral agregada exitosamente'
        })

    except Exception as e:
        app.logger.error(f"Error al crear experiencia laboral: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

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
        fecha_fin = data.get('fecha_fin') if data.get('fecha_fin') else None
        
        nueva_educacion = Educacion(current_user.id, data.get('institucion'), data.get('titulo'), data.get('area_estudio'), data.get('fecha_inicio'), fecha_fin, data.get('descripcion'))
        nueva_educacion.create()

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
        
        fecha_vencimiento = data.get('fecha_vencimiento') if data.get('fecha_vencimiento') else None

        nuevo_cert = Certificaciones(current_user.id, data.get('nombre'), data.get('organizacion'), data.get('fecha_obtencion'), fecha_vencimiento, data.get('url_verificacion'), data.get('credencial'), data.get('descripcion'))
        nuevo_cert.create()
        
        return jsonify({"status": "success", "message": "Certificación guardada correctamente"})
    except Exception as e:
        print(f"Error en /api/certificaciones: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/proyectos-destacados', methods=['POST'])
def add_proyecto_destacado():
    try:
        data = request.get_json()

        print(data)

        # Validar campos requeridos
        required_fields = ['titulo', 'fecha_inicio', 'descripcion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'El campo {field} es requerido'})

        nuevo_pd = Proyectos_destacados(current_user.id, data.get('titulo'), data.get('descripcion'), data.get('tecnologias'), data.get('fecha_inicio'), data.get('fecha_fin'), data.get('url_proyecto'))
        nuevo_pd.create()

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

# endregion

# region API SIN DEFINIR

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


# endregion

# endregion






















