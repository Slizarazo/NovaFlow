from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role  # 'gestor', 'aliado', 'supervisor', 'consultor'
    
    @classmethod
    def get_by_username(cls, username):
        for user in cls.USERS:
            if user.username == username:
                return user
        return None

class Aliado:
    def __init__(self, id, nombre, region, industria, ventas_trimestre, ventas_acumuladas):
        self.id = id
        self.nombre = nombre
        self.region = region
        self.industria = industria
        self.ventas_trimestre = ventas_trimestre
        self.ventas_acumuladas = ventas_acumuladas

class Proyecto:
    def __init__(self, id, nombre, aliado_id, etapa, fecha_inicio, fecha_fin, monto, consultores_asignados):
        self.id = id
        self.nombre = nombre
        self.aliado_id = aliado_id
        self.etapa = etapa  # 'propuesta', 'planificacion', 'ejecucion', 'cierre', 'post-evaluacion'
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.monto = monto
        self.consultores_asignados = consultores_asignados

class Consultor:
    def __init__(self, id, nombre, especialidad, proyectos_asignados, disponibilidad):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.proyectos_asignados = proyectos_asignados  # IDs de proyectos
        self.disponibilidad = disponibilidad  # porcentaje disponible

class DatosDashboard:
    # Mock data for dashboard visualizations
    UBICACIONES = [
        {'nombre': 'Oficina Norte', 'lat': 19.4326, 'lng': -99.1332, 'proyectos': 3, 'consultores': 5},
        {'nombre': 'Oficina Sur', 'lat': 19.3500, 'lng': -99.2000, 'proyectos': 2, 'consultores': 3},
        {'nombre': 'Oficina Este', 'lat': 19.4200, 'lng': -99.0700, 'proyectos': 1, 'consultores': 2},
        {'nombre': 'Oficina Oeste', 'lat': 19.4100, 'lng': -99.2100, 'proyectos': 2, 'consultores': 4},
        {'nombre': 'Oficina Central', 'lat': 19.4326, 'lng': -99.1332, 'proyectos': 4, 'consultores': 6}
    ]
    
    VENTAS_POR_PORTAFOLIO = [
        {'nombre': 'Transformación Digital', 'ventas': 245000},
        {'nombre': 'Consultoría de Procesos', 'ventas': 185000},
        {'nombre': 'Implementación Tecnológica', 'ventas': 210000},
        {'nombre': 'Estrategia y Mercado', 'ventas': 120000},
        {'nombre': 'Servicios Corporativos', 'ventas': 160000}
    ]
    
    DISTRIBUCION_INDUSTRIA = [
        {'industria': 'Tecnología', 'porcentaje': 35},
        {'industria': 'Finanzas', 'porcentaje': 25},
        {'industria': 'Manufactura', 'porcentaje': 20},
        {'industria': 'Servicios', 'porcentaje': 12},
        {'industria': 'Otros', 'porcentaje': 8}
    ]
    
    CRECIMIENTO_ANUAL = [
        {'mes': 'Ene', 'actual': 85000, 'anterior': 65000},
        {'mes': 'Feb', 'actual': 92000, 'anterior': 70000},
        {'mes': 'Mar', 'actual': 98000, 'anterior': 75000},
        {'mes': 'Abr', 'actual': 105000, 'anterior': 82000},
        {'mes': 'May', 'actual': 120000, 'anterior': 90000},
        {'mes': 'Jun', 'actual': 135000, 'anterior': 95000},
        {'mes': 'Jul', 'actual': 128000, 'anterior': 98000},
        {'mes': 'Ago', 'actual': 140000, 'anterior': 105000},
        {'mes': 'Sep', 'actual': 152000, 'anterior': 110000},
        {'mes': 'Oct', 'actual': 160000, 'anterior': 118000},
        {'mes': 'Nov', 'actual': 168000, 'anterior': 125000},
        {'mes': 'Dic', 'actual': 180000, 'anterior': 138000}
    ]
    
    FUNNEL_PROYECTOS = [
        {'etapa': 'Propuesta', 'cantidad': 15},
        {'etapa': 'Planificación', 'cantidad': 8},
        {'etapa': 'Ejecución', 'cantidad': 12},
        {'etapa': 'Cierre', 'cantidad': 6},
        {'etapa': 'Post-evaluación', 'cantidad': 4}
    ]
    
    ACTIVIDADES_PLANIFICADAS = [
        {'id': 1, 'actividad': 'Onboarding Aliados', 'inicio': '2023-01-01', 'fin': '2023-02-15'},
        {'id': 2, 'actividad': 'Propuestas', 'inicio': '2023-02-01', 'fin': '2023-03-15'},
        {'id': 3, 'actividad': 'Planificación', 'inicio': '2023-03-01', 'fin': '2023-04-15'},
        {'id': 4, 'actividad': 'Ejecución', 'inicio': '2023-04-01', 'fin': '2023-07-15'},
        {'id': 5, 'actividad': 'Monitoreo', 'inicio': '2023-04-15', 'fin': '2023-07-30'},
        {'id': 6, 'actividad': 'Cierre', 'inicio': '2023-07-15', 'fin': '2023-08-30'},
        {'id': 7, 'actividad': 'Evaluación', 'inicio': '2023-08-15', 'fin': '2023-09-30'},
        {'id': 8, 'actividad': 'Retención', 'inicio': '2023-09-15', 'fin': '2023-10-30'}
    ]

# Create instances after all classes are defined
User.USERS = [
    User(1, 'gestor1', 'gestor@example.com', 'password', 'gestor'),
    User(2, 'aliado1', 'aliado@example.com', 'password', 'aliado'),
    User(3, 'supervisor1', 'supervisor@example.com', 'password', 'supervisor'),
    User(4, 'consultor1', 'consultor@example.com', 'password', 'consultor')
]

Aliado.ALIADOS = [
    Aliado(1, 'Aliado Tech', 'Norte', 'Tecnología', 125000, 450000),
    Aliado(2, 'Financiera Global', 'Centro', 'Finanzas', 98000, 320000),
    Aliado(3, 'Industrias Este', 'Este', 'Manufactura', 110000, 390000),
    Aliado(4, 'Consultores Sur', 'Sur', 'Consultoría', 85000, 280000),
    Aliado(5, 'Servicios Oeste', 'Oeste', 'Servicios', 102000, 350000)
]

Proyecto.PROYECTOS = [
    # Oportunidad
    Proyecto(1, 'IA para Detección de Fraudes', 1, 'oportunidad', '2023-01-15', '2023-06-30', 85000, 4),
    Proyecto(2, 'Chatbot Inteligente', 2, 'oportunidad', '2023-02-10', '2023-09-20', 72000, 3),
    Proyecto(3, 'Optimización de Inventarios', 3, 'oportunidad', '2023-03-05', '2023-08-15', 95000, 5),
    
    # Propuesta
    Proyecto(4, 'Análisis Predictivo Cliente A', 4, 'propuesta', '2023-01-20', '2023-04-10', 45000, 2),
    Proyecto(5, 'Dashboard BI Cliente B', 5, 'propuesta', '2022-11-10', '2023-03-20', 65000, 3),
    Proyecto(6, 'Sistema de Recomendaciones', 1, 'propuesta', '2023-02-05', '2023-07-15', 78000, 4),
    
    # Aprobado
    Proyecto(7, 'Migración a la Nube', 2, 'aprobado', '2023-01-25', '2023-05-30', 53000, 2),
    Proyecto(8, 'App de Logística', 3, 'aprobado', '2023-03-10', '2023-08-20', 67000, 3),
    
    # Desarrollo
    Proyecto(9, 'Portal de Autoservicio', 1, 'desarrollo', '2023-01-15', '2023-06-30', 85000, 4),
    Proyecto(10, 'Sistema de Monitoreo', 2, 'desarrollo', '2023-02-10', '2023-09-20', 72000, 3),
    Proyecto(11, 'Plataforma E-learning', 3, 'desarrollo', '2023-03-05', '2023-08-15', 95000, 5),
    Proyecto(12, 'API de Integración', 4, 'desarrollo', '2023-01-20', '2023-04-10', 45000, 2),
    
    # Testing
    Proyecto(13, 'App Bancaria Mobile', 1, 'testing', '2022-11-10', '2023-03-20', 65000, 3),
    Proyecto(14, 'Sistema de Pagos', 2, 'testing', '2023-02-05', '2023-07-15', 78000, 4),
    
    # Cierre
    Proyecto(15, 'Sistema CRM Cliente C', 3, 'cierre', '2023-01-25', '2023-05-30', 53000, 2),
    Proyecto(16, 'App Mobile Cliente D', 4, 'cierre', '2023-03-10', '2023-08-20', 67000, 3),
    Proyecto(17, 'Dashboard Ejecutivo', 5, 'cierre', '2023-01-15', '2023-06-30', 85000, 4),
    
    # Evaluación
    Proyecto(18, 'Proyecto Analytics', 1, 'evaluacion', '2023-02-10', '2023-09-20', 72000, 3),
    Proyecto(19, 'Sistema de Reportes', 2, 'evaluacion', '2023-03-05', '2023-08-15', 95000, 5),
    
    # Finalizados
    Proyecto(20, 'Portal Corporativo', 3, 'finalizado', '2023-01-20', '2023-04-10', 45000, 2),
    Proyecto(21, 'Sistema de Facturación', 4, 'finalizado', '2022-11-10', '2023-03-20', 65000, 3),
    Proyecto(22, 'App de Ventas', 5, 'finalizado', '2023-02-05', '2023-07-15', 78000, 4),
    Proyecto(23, 'Plataforma de Marketing', 1, 'finalizado', '2023-01-25', '2023-05-30', 53000, 2),
    Proyecto(24, 'Sistema de Inventario', 2, 'finalizado', '2023-03-10', '2023-08-20', 67000, 3)
]

Consultor.CONSULTORES = [
    Consultor(1, 'Ana Martínez', 'Tecnología', [1, 6], 30),
    Consultor(2, 'Carlos Ruiz', 'Finanzas', [2], 70),
    Consultor(3, 'Elena Gómez', 'Manufactura', [3, 7], 20),
    Consultor(4, 'Javier Pérez', 'Marketing', [4], 60),
    Consultor(5, 'María López', 'Operaciones', [5], 80),
    Consultor(6, 'Roberto Sánchez', 'Tecnología', [1, 6], 40),
    Consultor(7, 'Sofía Torres', 'Estrategia', [2, 4], 50)
]
