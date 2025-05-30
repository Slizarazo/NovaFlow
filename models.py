from flask_login import UserMixin
from config import workbench_db as mydb

# region modelos de testeo

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
 #endregion

# region ALIADOS
# temporalmente se le agrego la s (plural) para diferenciarlo de los modelos de testeo
class Organizaciones:
    def __init__(self, region, industria, fecha_registro, estado,
                 contacto_principal, tamaño, empleados, pais):
        self.region = region
        self.industria = industria
        self.fecha_registro = fecha_registro
        self.estado = estado
        self.contacto_principal = contacto_principal
        self.tamaño = tamaño
        self.empleados = empleados
        self.pais = pais

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
        INSERT INTO aliados (
            region, industria, fecha_registro, estado,
            contacto_principal, tamaño, empleados, pais
        ) VALUES(
            %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
        values = (
            self.region, self.industria, self.fecha_registro, self.estado,
            self.contacto_principal, self.tamaño, self.empleados, self.pais
        )
        
        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid
        
        mycursor.close()
        conn.close()

        return id
    
# endregion

# region COLABORADORES

class Colaborador:
    def __init__(self, id_usuario, id_organizacion, cargo, rol_laboral):
        self.id_usuario = id_usuario
        self.id_organizacion = id_organizacion
        self.cargo = cargo
        self.rol_laboral = rol_laboral

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO colaboradores (id_usuario, cargo, rol_laboral) VALUES(%s, %s, %s);"
        values = (self.id_usuario, self.cargo, self.rol_laboral)
        
        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_all(incluir_inactivos=False):
        if incluir_inactivos:
            query = "SELECT * FROM colaboradores ORDER BY id_colaboradores ASC;"
        else:
            query = "SELECT * FROM colaboradores WHERE estado = 'activo' ORDER BY id_colaboradores ASC;"
        # return ejecutar_sql(query, fetch='all')

    @staticmethod
    def get_by_id(id_colaboradores, incluir_inactivo=False):
        if incluir_inactivo:
            query = "SELECT * FROM colaboradores WHERE id_colaboradores = %s;"
        else:
            query = "SELECT * FROM colaboradores WHERE id_colaboradores = %s AND estado = 'activo';"
        # return ejecutar_sql(query, (id_colaboradores,), fetch='one')

    def update(self, id_colaboradores):
        query = """
        UPDATE colaboradores SET
            id_aliado = %s,
            cargo = %s,
            rol_laboral = %s,
            estado = %s
        WHERE id_colaboradores = %s;
        """
        values = (
            self.id_aliado, self.cargo, self.rol_laboral, self.estado, id_colaboradores
        )
        # ejecutar_sql(query, values)

    @staticmethod
    def delete(id_colaboradores):
        query = "UPDATE colaboradores SET estado = 'inactivo' WHERE id_colaboradores = %s;"
        # ejecutar_sql(query, (id_colaboradores,))

# endregion

# region INDUSTRIAS

class Industria:
    def __init__(self, nombre):
        self.nombre = nombre

    def create(self):
        query = "INSERT INTO industrias (nombre) VALUES (%s);"
        # ejecutar_sql(query, (self.nombre,))

    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "SELECT * FROM industrias ORDER BY sector ASC;"
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_by_id(id_industria):
        query = "SELECT * FROM industrias WHERE id_industria = %s;"
        # return ejecutar_sql(query, (id_industria,), fetch='one')

    def update(self, id_industria):
        query = "UPDATE industrias SET nombre = %s WHERE id_industria = %s;"
        # ejecutar_sql(query, (self.nombre, id_industria))

    @staticmethod
    def delete(id_industria):
        query = "DELETE FROM industrias WHERE id_industria = %s;"
        # ejecutar_sql(query, (id_industria,))

# endregion

# region USUARIOS
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado

        Args:
            password (str): contraseña del usuario

        Returns:
            byte: contraseña hasheada
        """
        return check_password_hash(self.contraseña_hash, password)
    
    def set_password_hash(password):
        """Establece una nueva contraseña hasheada

        Args:
            password (str): contraseña del usuario por defecto
        """
        return generate_password_hash(password)

    def __init__(self, nombre, organizacion, correo, contraseña_hash, id_rol, estado='activo', ultimo_login=None):
        self.nombre = nombre
        self.organizacion = organizacion
        self.correo = correo
        self.contraseña_hash = contraseña_hash
        self.id_rol = id_rol
        self.estado = estado
        self.ultimo_login = ultimo_login

    def create(self):
        password = Usuario.set_password_hash(self.contraseña_hash)
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
        INSERT INTO usuarios (
            nombre, organizacion, correo, contraseña_hash, id_rol, estado, ultimo_login
        ) VALUES(%s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            self.nombre, self.organizacion, self.correo, password,
            self.id_rol, self.estado, self.ultimo_login
        )

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_id_by_correo(correo):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()
        
        query = "SELECT id_usuario FROM usuarios WHERE correo = "+str(correo)+" AND estado = 'activo';"

        mycursor.execute(query)
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_by_id(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()
        
        query = "SELECT * FROM usuarios WHERE id_usuario = "+str(id)+";"

        mycursor.execute(query)
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_organizaciones():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """SELECT MIN(id_usuario) AS id_usuario, organizacion
                    FROM usuarios
                    WHERE estado = 'activo'
                    GROUP BY organizacion
                    ORDER BY organizacion ASC;"""

        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    def update(self, id_usuario):
        query = """
        UPDATE usuarios SET
            nombre = %s,
            correo = %s,
            contraseña_hash = %s,
            id_rol = %s,
            estado = %s,
            ultimo_login = %s
        WHERE id_usuario = %s;
        """
        values = (
            self.nombre, self.correo, self.contraseña_hash,
            self.id_rol, self.estado, self.ultimo_login, id_usuario
        )
        # ejecutar_sql(query, values)

    @staticmethod
    def delete(id_usuario):
        query = "UPDATE usuarios SET estado = 'inactivo' WHERE id_usuario = %s;"
        # ejecutar_sql(query, id_usuario)

# endregion





