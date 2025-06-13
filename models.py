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

# region ORGANIZACIONES

class Organizaciones:

    def __init__(self, nombre, id_industria, fecha_registro, estado, contacto_principal, tamaño, empleados):
        self.nombre = nombre
        self.id_industria = id_industria
        self.fecha_registro = fecha_registro
        self.estado = estado
        self.contacto_principal = contacto_principal
        self.tamaño = tamaño
        self.empleados = empleados

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
        INSERT INTO organizaciones (
            nombre, id_industria, fecha_registro, estado, contacto_principal, tamaño, empleados
        ) VALUES(
            %s, %s, %s, %s, %s, %s, %s
        );
        """
        values = (
            self.nombre, self.id_industria, self.fecha_registro, self.estado, self.contacto_principal, self.tamaño, self.empleados
        )
        
        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid
        
        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM organizaciones WHERE estado = "activo";')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_table_orgs():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                org.nombre AS "Organización",
                ind.nombre AS "Industria",
                org.estado AS "Estado",
                CONCAT(reg.nombre, " (", reg.codigo, ")") AS "Región",
                CONCAT(sreg.nombre, " (", sreg.codigo, ")") AS "Sub-Región",
                sede.pais AS "Pais",
                sede.nombre_sede AS "Sede"
            FROM 
                nova_flow.organizaciones org
            LEFT JOIN nova_flow.industrias ind ON org.id_industria = ind.id_industria
            LEFT JOIN nova_flow.sedes sede ON sede.id_organizacion = org.id
            LEFT JOIN nova_flow.subregiones sreg ON sede.subregion = sreg.id
            LEFT JOIN nova_flow.regiones reg ON sreg.id_region = reg.id"""
        
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region SEDES

class Sedes:
    
    def __init__(self, id_organizacion, nombre_sede, subregion, direccion, ciudad, codigo_postal, pais):
        self.id_organizacion = id_organizacion
        self.nombre_sede = nombre_sede
        self.subregion = subregion
        self.direccion = direccion
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.pais = pais

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO sedes (id_organizacion, nombre_sede, subregion, direccion, ciudad, codigo_postal, pais) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_organizacion, self.nombre_sede, self.subregion, self.direccion, self.ciudad, self.codigo_postal, self.pais)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM sedes;')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data
    
    @staticmethod
    def get_orgs():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT
                se.id_sede,
                CONCAT(se.nombre_sede, " (", org.nombre, ")")
            FROM nova_flow.sedes se
            LEFT JOIN nova_flow.organizaciones org ON se.id_organizacion = org.id"""
        
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region SUBREGIONES

class Subregiones:

    def __init__(self, nombre, codigo, descripcion, id_region, activo):
        self.nombre = nombre
        self.codigo = codigo
        self.descripcion = descripcion
        self.id_region = id_region
        self.activo = activo

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = 'INSERT INTO subregiones (nombre, codigo, descripcion, id_region, activo) VALUES(%s, %s, %s, %s, %s)'
        values = (self.nombre, self.codigo, self.descripcion, self.id_region, self.activo)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM subregiones WHERE activo = "1";')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region REGIONES

class Regiones:

    def __init__(self, nombre, codigo, descripcion, activo):
        self.nombre = nombre
        self.codigo = codigo
        self.descripcion = descripcion
        self.activo = activo

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = 'INSERT INTO regiones (nombre, codigo, descripcion, activo) VALUES(%s, %s, %s, %s)'
        values = (self.nombre, self.codigo, self.descripcion, self.activo)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM regiones WHERE activo = "1"')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region COLABORADORES

class Colaboradores:

    def __init__(self, id_usuario, id_organizacion, cargo, rol_laboral):
        self.id_usuario = id_usuario
        self.id_organizacion = id_organizacion
        self.cargo = cargo
        self.rol_laboral = rol_laboral

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO colaboradores (id_usuario, id_organizacion, cargo, rol_laboral) VALUES(%s, %s, %s, %s);"
        values = (self.id_usuario, self.id_organizacion, self.cargo, self.rol_laboral)
        
        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region INDUSTRIAS

class Industrias:

    def __init__(self, nombre, grupo_general, sector, nota):
        self.nombre = nombre
        self.grupo_general = grupo_general
        self.sector = sector
        self.nota = nota

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO industrias (nombre, grupo_general, sector, nota) VALUES(%s, %s, %s, %s);"
        values = (self.nombre, self.grupo_general, self.sector, self.nota)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute("SELECT * FROM industrias ORDER BY sector ASC;")
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region ACCESO DE USUARIOS

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserAcces(UserMixin):

    @staticmethod
    def check_password(password, contraseña_hash):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado

        Args:
            password (str): contraseña del usuario

        Returns:
            byte: contraseña hasheada
        """
        return check_password_hash(contraseña_hash, password)
    
    @staticmethod
    def set_password_hash(password):
        """Establece una nueva contraseña hasheada

        Args:
            password (str): contraseña del usuario por defecto
        """
        return generate_password_hash(password)

    def __init__(self, id, nombre, organizacion, sede, correo, contraseña, rol, estado, ultimo_login):
        self.id = id
        self.nombre = nombre
        self.organizacion = organizacion
        self.sede = sede
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol
        self.estado = estado
        self.ultimo_login = ultimo_login

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return self.estado == 'activo'

    @staticmethod
    def get_by_access(user):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                us.id_usuario AS "id",
                us.nombre AS "nombre",
                org.nombre AS "organizacion",
                sede.nombre_sede AS "sede",
                us.correo AS "correo",
                us.contraseña AS "contraseña",
                rol.nombre AS "rol",
                us.estado,
                us.ultimo_login
            FROM 
                nova_flow.usuarios us
            LEFT JOIN 
                nova_flow.organizaciones org ON us.id_organizacion = org.id
            LEFT JOIN 
                nova_flow.sedes sede ON us.id_sede = sede.id_sede
            LEFT JOIN 
                nova_flow.roles rol ON us.id_rol = rol.id_rol
            WHERE
                us.correo = %s
            AND 
                us.estado = %s"""
        values = (user, "activo")

        mycursor.execute(query, values)
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data
    
    @staticmethod
    def get_access_by_id(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "SELECT * FROM usuarios WHERE id_usuario = %s;"        
        values = (int(id),)

        mycursor.execute(query, values)
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_by_id(user_id):
        row = UserAcces.get_access_by_id(user_id)

        if row[6] == 1:
            role = "Aliado"
        elif row[6] == 2:
            role = "Gestor"
        elif row[6] == 3:
            role = "Supervisor"
        elif row[6] == 4:
            role = "Freelance"
        elif row[6] == 5:
            role = "Empleado"

        if row:
            return UserAcces(
                id=row[0],
                nombre=row[1],
                organizacion=row[2],
                sede=row[3],
                correo=row[4],
                contraseña="No disponible",
                rol=role,
                estado=row[7],
                ultimo_login=row[8]
            )
        
        return None

# endregion

# region USUARIOS

class Usuario:

    @staticmethod
    def check_password(password, contraseña_hash):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado

        Args:
            password (str): contraseña del usuario

        Returns:
            byte: contraseña hasheada
        """
        return check_password_hash(contraseña_hash, password)
    
    @staticmethod
    def set_password_hash(password):
        """Establece una nueva contraseña hasheada

        Args:
            password (str): contraseña del usuario por defecto
        """
        return generate_password_hash(password)


    def __init__(self, nombre, id_organizacion, id_sede, correo, contraseña, id_rol, estado='activo', ultimo_login=None):
        self.nombre = nombre
        self.id_organizacion = id_organizacion
        self.id_sede = id_sede
        self.correo = correo
        self.contraseña = contraseña
        self.id_rol = id_rol
        self.estado = estado
        self.ultimo_login = ultimo_login

    def create(self):
        password = Usuario.set_password_hash(self.contraseña)
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
        INSERT INTO usuarios (
            nombre, id_organizacion, id_sede, correo, contraseña, id_rol, estado, ultimo_login
        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            self.nombre, self.id_organizacion, self.id_sede, self.correo, password,
            self.id_rol, self.estado, self.ultimo_login
        )

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    def update_rol(id, rol):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('UPDATE usuarios SET id_rol = '+str(rol)+' WHERE id_usuario = '+str(id)+';')
        conn.commit()

        mycursor.close()
        conn.close()

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
        mycursor = conn.cursor(dictionary=True)
        
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

    @staticmethod
    def get_table_users():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                u.id_usuario AS 'id',
                u.nombre AS 'Nombre',
                o.nombre AS 'Organización',
                s.nombre_sede AS 'Sede',
                u.correo AS "Usuario",
                r.nombre AS 'Rol',
                u.estado AS 'Estado'
            FROM nova_flow.usuarios u
            LEFT JOIN nova_flow.organizaciones o ON u.id_organizacion = o.id
            LEFT JOIN nova_flow.sedes s ON u.id_sede = s.id_sede
            LEFT JOIN nova_flow.roles r ON u.id_rol = r.id_rol;"""
        
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_tbl_consultores():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                us.id_usuario,
                us.nombre,
                con.especialidad,
                con.disponibilidad,
                ROUND((con.nivel_segun_usuario + con.nivel_segun_gestor) / 2),
                con.ciudad,
                con.tarifa_hora AS "tarifa"
            FROM nova_flow.usuarios us
            LEFT JOIN nova_flow.consultores con ON us.id_usuario = con.id_usuario
            WHERE us.id_rol = '4'"""
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data
   
# endregion

# region PORTAFOLIO

class Portafolio:
    
    def __init__(self, nombre, categoria, familia, descripcion, tipo, estado, fecha_creacion, fecha_actualizacion):
        self.nombre = nombre
        self.categoria = categoria
        self.familia = familia
        self.descripcion = descripcion
        self.tipo = tipo
        self.estado = estado
        self. fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion

    def create (self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO portafolio (nombre, categoria, familia, descripcion, tipo, estado, fecha_creacion, fecha_actualizacion) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.nombre, self.categoria, self.familia, self.descripcion, self.tipo, self.estado, self.fecha_creacion, self.fecha_actualizacion)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute("SELECT * FROM portafolio;")
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region CONSULTORES

class Consultores:
    
    def __init__(self, id_usuario, especialidad, disponibilidad, nivel_segun_usuario, nivel_segun_gestor, fecha_incorporacion, direccion, ciudad, codigo_postal, pais, tarifa_hora, resumen_perfil):
        self.id_usuario = id_usuario
        self.especialidad = especialidad
        self.disponibilidad = disponibilidad
        self.ns_usuario = nivel_segun_usuario
        self.ns_gestor = nivel_segun_gestor
        self.fecha_incorporacion = fecha_incorporacion
        self.direccion = direccion 
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.pais = pais
        self.tarifa_hora = tarifa_hora
        self.resumen_perfil = resumen_perfil

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO consultores (id_usuario, especialidad, disponibilidad, nivel_segun_usuario, nivel_segun_gestor, fecha_incorporacion, direccion, ciudad, codigo_postal ,pais, tarifa_hora, resumen_perfil) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_usuario, self.especialidad, self.disponibilidad, self.ns_usuario, self.ns_gestor, self.fecha_incorporacion, self.direccion, self.ciudad, self.codigo_postal, self.pais, self.tarifa_hora, self.resumen_perfil)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    def update(celular, linkedin, especialidad, nivel, direccion, ciudad, codigo_postal, pais, tarifa_hora, resumen, id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
        UPDATE consultores SET celular = %(celular)s, 
            linkedin = %(linkedin)s, 
            nivel_segun_usuario = %(nivel)s, 
            direccion = %(direccion)s, 
            ciudad = %(ciudad)s, 
            codigo_postal = %(codigo_postal)s, 
            pais = %(pais)s, 
            tarifa_hora = %(tarifa_hora)s, 
            resumen_perfil = %(resumen)s 
        WHERE id_usuario = %(id)s
        """
        values = {
            'celular': celular,
            'linkedin': linkedin,
            'especialidad': especialidad,
            'nivel': nivel,
            'direccion': direccion,
            'ciudad': ciudad,
            'codigo_postal': codigo_postal,
            'pais': pais,
            'tarifa_hora': tarifa_hora,
            'resumen': resumen,
            'id': id
        }

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_by_id(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        mycursor.execute('SELECT * FROM consultores WHERE id_usuario = '+str(id)+'')
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data

# endregion

# region COMUNIDADES

class Comunidades:
    
    def __init__(self, nombre, descripcion, tipo):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO comunidades (nombre, descripcion, tipo) VALUES(%s, %s, %s);"
        values = (self.nombre, self.descripcion, self.tipo)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM comunidades;')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region MIEMBROS COMUNIDAD

class Miembros_comunidad:
    
    def __init__(self, id_comunidad, id_usuario, rol_en_comunidad, fecha_union):
        self.id_comunidad = id_comunidad
        self.id_usuario = id_usuario
        self.rol_en_comunidad = rol_en_comunidad
        self.fecha_union = fecha_union

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO miembros_comunidad (id_comunidad, id_usuario, rol_en_comunidad, fecha_union) VALUES(%s, %s, %s, %s)"
        values = (self.id_comunidad, self.id_usuario, self.rol_en_comunidad, self.fecha_union)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region PERSONAS CLIENTE

class Personas_cliente:
    
    def __init__(self, id_sede, id_usuario, rol_en_cliente, fecha_asignacion):
        self.id_sede = id_sede
        self.id_usuario = id_usuario
        self.rol_en_cliente = rol_en_cliente
        self.fecha_asignacion = fecha_asignacion

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO personas_cliente (id_sede, id_usuario, rol_en_cliente, fecha_asignacion) VALUES(%s, %s, %s, %s);"
        values = (self.id_sede, self.id_usuario, self.rol_en_cliente, self.fecha_asignacion)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_consultores_aliado(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                u.id_usuario,
                u.nombre
            FROM personas_cliente pc
            JOIN usuarios u ON pc.id_usuario = u.id_usuario
            WHERE pc.id_sede = %(id_sede)s

            UNION

            SELECT 
                u.id_usuario,
                u.nombre
            FROM comunidad_aliado ca
            JOIN miembros_comunidad mc ON ca.id_comunidad = mc.id_comunidad
            JOIN usuarios u ON mc.id_usuario = u.id_usuario
            WHERE ca.id_sede = %(id_sede)s;
            """
        
        # Parámetros como diccionario
        params = {'id_sede': id}

        mycursor.execute(query, params)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region COMUNIDAD ALIADO

class Comunidad_aliado:
    
    def __init__(self, id_sede, id_comunidad, fecha_asignacion, observaciones):
        self.id_sede = id_sede
        self.id_comunidad = id_comunidad
        self.fecha_asignacion = fecha_asignacion
        self.observaciones = observaciones

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO comunidad_aliado (id_sede, id_comunidad, fecha_asignacion, observaciones) VALUES(%s, %s, %s, %s);"
        values = (self.id_sede, self.id_comunidad, self.fecha_asignacion, self.observaciones)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_asignaciones_estrategicas():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                s.nombre_sede AS nombre_organizacion,
                c.nombre AS nombre_comunidad,
                c.descripcion AS descripcion,
                u.nombre AS usuario,
                'Comunidad' AS tipo_asignacion,
                mc.rol_en_comunidad AS rol
            FROM nova_flow.comunidad_aliado ca
            JOIN nova_flow.sedes s ON ca.id_sede = s.id_sede
            JOIN nova_flow.comunidades c ON ca.id_comunidad = c.id
            JOIN nova_flow.miembros_comunidad mc ON ca.id_comunidad = mc.id_comunidad
            JOIN nova_flow.usuarios u ON mc.id_usuario = u.id_usuario

            UNION ALL

            SELECT 
                s.nombre_sede AS nombre_organizacion,
                NULL AS nombre_comunidad,
                NULL AS descripcion,
                u.nombre AS usuario,
                'Individual' AS tipo_asignacion,
                pc.rol_en_cliente AS rol
            FROM nova_flow.personas_cliente pc
            JOIN nova_flow.sedes s ON pc.id_sede = s.id_sede
            JOIN nova_flow.usuarios u ON pc.id_usuario = u.id_usuario

            ORDER BY nombre_organizacion, tipo_asignacion, usuario;
        """

        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_asignaciones_operativas():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                org.nombre_sede AS "organizacion",
                us.nombre AS "nombre_usuario",
                cli.nombre AS "Cuenta",
                cu.caso_uso AS "caso_uso",
                cu.estado AS "estado"
            FROM caso_uso cu
            LEFT JOIN sedes org ON cu.id_aliado = org.id_sede
            LEFT JOIN usuarios us ON cu.id_usuario = us.id_usuario
            LEFT JOIN cuentas cli ON cu.id_cuenta = cli.id
            """
        
        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region CASOS DE USO

class Casos_uso:

    def __init__(self, id_aliado, id_usuario, id_cuenta, caso_uso, descripcion, impacto, puntuacion_impacto, puntuacion_tecnica, tags, estado, id_producto, fecha_inicio, fecha_cierre, monto_venta, costos_proyecto, margen_estimado_porcentaje, margen_estimado_bruto, feedback):
        self.id_aliado = id_aliado
        self.id_usuario = id_usuario
        self.id_cuenta = id_cuenta
        self.caso_uso = caso_uso
        self.descripcion = descripcion
        self.impacto = impacto
        self.puntuacion_impacto = puntuacion_impacto
        self.puntuacion_tecnica = puntuacion_tecnica
        self.tags = tags
        self.estado = estado
        self.id_producto = id_producto
        self.fecha_inicio = fecha_inicio
        self.fecha_cierre = fecha_cierre
        self.monto_venta = monto_venta
        self.costos_proyecto = costos_proyecto
        self.margen_estimado_porcentaje = margen_estimado_porcentaje
        self.margen_estimado_bruto = margen_estimado_bruto
        self.feedback = feedback

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO caso_uso (id_aliado, id_usuario, id_cuenta, caso_uso, descripcion, impacto, puntuacion_impacto, puntuacion_tecnica, tags, estado, id_producto, fecha_inicio, fecha_cierre, monto_venta, costos_proyecto, margen_estimado_porcentaje, margen_estimado_bruto, feedback) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_aliado, self.id_usuario, self.id_cuenta, self.caso_uso, self.descripcion, self.impacto, self.puntuacion_impacto, self.puntuacion_tecnica, self.tags, self.estado, self.id_producto, self.fecha_inicio, self.fecha_cierre, self.monto_venta, self.costos_proyecto, self.margen_estimado_porcentaje, self.margen_estimado_bruto, self.feedback)
        
        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    def update(campo, valor, id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = f"UPDATE caso_uso SET {campo} = %s WHERE (id = %s);"
        values = (valor, id)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_projects(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                cu.id,
                us.nombre AS nombre_usuario,
                c.nombre AS nombre_cuenta,
                cu.caso_uso,
                cu.descripcion,
                cu.impacto,
                cu.puntuacion_impacto AS p_impacto,
                cu.puntuacion_tecnica AS p_tecnica,
                cu.tags,
                cu.estado,
                pr.nombre AS producto,
                cu.fecha_inicio,
                cu.fecha_cierre,
                cu.monto_venta,
                cu.costos_proyecto,
                cu.margen_estimado_porcentaje AS mep,
                cu.margen_estimado_bruto AS meb
            FROM nova_flow.caso_uso cu
            LEFT JOIN nova_flow.usuarios us ON cu.id_usuario = us.id_usuario
            LEFT JOIN nova_flow.cuentas c ON cu.id_cuenta = c.id
            LEFT JOIN nova_flow.portafolio pr ON cu.id_producto = pr.id
            WHERE cu.id_aliado = %(id)s
            """
        values = {'id': id}

        mycursor.execute(query, values)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_projects_to_sup(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM caso_uso WHERE id_usuario = '+str(id)+';')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_by_id(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM caso_uso WHERE id = '+str(id)+';')
        data = mycursor.fetchone()

        mycursor.close()
        conn.close()

        return data

# endregion

# region CUENTAS

class Cuentas:

    def __init__(self, id_organizacion, nombre, industria, subregion, fecha_alta, fecha_modificacion, fecha_baja, codigo, id_segmentacion, estado):
        self.id_organizacion = id_organizacion
        self.nombre = nombre
        self.industria = industria
        self.subregion = subregion
        self.fecha_alta = fecha_alta
        self.fecha_modificacion = fecha_modificacion
        self.fecha_baja = fecha_baja
        self.codigo = codigo
        self.id_segmentacion = id_segmentacion
        self.estado = estado

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO cuentas (id_organizacion, nombre, industria, subregion, fecha_alta, fecha_modificacion, fecha_baja, codigo, id_segmentacion, estado) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_organizacion, self.nombre, self.industria, self.subregion, self.fecha_alta, self.fecha_modificacion, self.fecha_baja, self.codigo, self.id_segmentacion, self.estado)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_all_tbl():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = """
            SELECT 
                cu.id,
                cu.nombre,
                CONCAT(ind.nombre, " ", ind.grupo_general) AS "industria",
                cu.estado,
                COUNT(pro.id_cuenta) AS "proyectos_activos"
            FROM nova_flow.cuentas cu
            LEFT JOIN nova_flow.industrias ind ON cu.industria = ind.id_industria
            LEFT JOIN nova_flow.caso_uso pro ON cu.id = pro.id_cuenta
            GROUP BY cu.id, cu.nombre, ind.nombre, ind.grupo_general, cu.estado;"""

        mycursor.execute(query)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

    @staticmethod
    def get_cuentas_by_aliado(aliado):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM cuentas WHERE id_organizacion = '+str(aliado)+';')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region SEGMENTACIONES

class Segmentacion:

    def __init__(self, clasificacion, descripcion):
        self.clasificacion = clasificacion
        self.descripcion = descripcion

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO segmentacion (clasificacion, descripcion) VALUES(%s, %s);"
        values = (self.clasificacion, self.descripcion)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        mycursor.execute('SELECT * FROM segmentacion;')
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region ROLES

class Roles:

    def __init__(self, nombre):
        self.nombre = nombre

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO roles (nombre) VALUES(%s);"
        values = (self.nombre,)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

# endregion

# region EXPERIENCIA LABORAL

class Exp_laboral:

    def __init__(self, id_usuario, cargo, empresa, descripcion, fecha_inicio, fecha_fin, ubicacion, tipo_empleo, sector, logros):
        self.id_usuario = id_usuario
        self.cargo = cargo
        self.empresa = empresa
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ubicacion = ubicacion
        self.tipo_empleo = tipo_empleo
        self.sector = sector
        self.logros = logros

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO experiencia_laboral (id_usuario, cargo, empresa, descripcion, fecha_inicio, fecha_fin, ubicacion, tipo_empleo, sector, logros) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_usuario, self.cargo, self.empresa, self.descripcion, self.fecha_inicio, self.fecha_fin, self.ubicacion, self.tipo_empleo, self.sector, self.logros)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    def get_by_id_usuario(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM experiencia_laboral WHERE id_usuario = %(id)s;"
        values = {'id': id}

        mycursor.execute(query, values)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region EDUCACIÓN

class Educacion:

    def __init__(self, id_usuario, institucion, titulo, area_estudio, fecha_inicio, fecha_fin, descripcion):
        self.id_usuario = id_usuario
        self.institucion = institucion
        self.titulo = titulo
        self.area_estudio = area_estudio
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.descripcion = descripcion

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        query = "INSERT INTO educacion (id_usuario, institucion, titulo, area_estudio, fecha_inicio, fecha_fin, descripcion) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_usuario, self.institucion, self.titulo, self.area_estudio, self.fecha_inicio, self.fecha_fin, self.descripcion)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_by_id_usuario(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM educacion WHERE id_usuario = %(id)s;"
        values = {'id': id}

        mycursor.execute(query, values)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# region CERTIFICACIONES

class Certificaciones:

    def __init__(self, id_usuario, nombre, entidad, fecha_obtencion, fecha_vencimiento, url_certificado, id_credencial, descripcion):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.entidad = entidad
        self.fecha_obtencion = fecha_obtencion
        self.fecha_vencimiento = fecha_vencimiento
        self.url_certificado = url_certificado
        self.id_credencial = id_credencial
        self.descripcion = descripcion

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO certificaciones (id_usuario, nombre, entidad, fecha_obtencion, fecha_vencimiento, url_certificado, id_credencial, descripcion) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_usuario, self.nombre, self.entidad, self.fecha_obtencion, self.fecha_vencimiento, self.url_certificado, self.id_credencial, self.descripcion)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
    @staticmethod
    def get_by_id_usuario(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM certificaciones WHERE id_usuario = %(id)s;"
        values = {'id': id}

        mycursor.execute(query, values)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data


# endregion

# region PROYECTOS DESTACADOS

class Proyectos_destacados:

    def __init__(self, id_usuario, nombre, descripcion, tecnologias_usadas, fecha_inicio, fecha_fin, link_portafolio):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.descripcion = descripcion
        self.tecnologias_usadas = tecnologias_usadas
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.link_portafolio = link_portafolio

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO proyectos_destacados (id_usuario, nombre, descripcion, tecnologias_usadas, fecha_inicio, fecha_fin, link_portafolio) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_usuario, self.nombre, self.descripcion, self.tecnologias_usadas, self.fecha_inicio, self.fecha_fin, self.link_portafolio)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

    @staticmethod
    def get_by_id_usuario(id):
        conn = mydb('nova_flow')
        mycursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM proyectos_destacados WHERE id_usuario = %(id)s;"
        values = {'id': id}

        mycursor.execute(query, values)
        data = mycursor.fetchall()

        mycursor.close()
        conn.close()

        return data

# endregion

# //////////////////////////////////////////////////
# //////////////////////////////////////////////////
# //////////////////////////////////////////////////
# ///////////////aun sin agregar////////////////////
# //////////////////////////////////////////////////
# //////////////////////////////////////////////////
# //////////////////////////////////////////////////

#  region ESTADOS

class Estados:

    def __init__(self, nombre, descripcion, entidad):
        self.nombre = nombre
        self.descripcion = descripcion
        self.entidad = entidad

# endregion

# region ESTIMACIONES

class Estimaciones:

    def __init__(self, id_caso_uso, nombre_caso_uso):
        self.id_caso_uso = id_caso_uso
        self.nombre_caso_uso = nombre_caso_uso

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO estimaciones (id_caso_uso, nombre_caso_uso) VALUES (%s, %s);"
        values = (self.id_caso_uso, self.nombre_caso_uso)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id
    
# endregion

# region ENTREGABLES

class Entregables:

    def __init__(self, id_estimacion, nombre, descripcion, criterios_aceptacion, estado, fecha_entrega_estimada, fecha_entregado, version, fecha_creacion, fecha_actualizacion, actualizado_por):
        self.id_estimacion = id_estimacion
        self.nombre = nombre
        self.descripcion = descripcion
        self.criterios_aceptacion = criterios_aceptacion
        self.estado = estado
        self.fecha_entrega_estimada = fecha_entrega_estimada
        self.fecha_entregado = fecha_entregado
        self.version = version
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.actualizado_por = actualizado_por

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO entregables (id_estimacion, nombre, descripcion, criterios_aceptacion, estado, fecha_entrega_estimada, fecha_entregado, version, fecha_creacion, fecha_actualizacion, actualizado_por) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_estimacion, self.nombre, self.descripcion, self.criterios_aceptacion, self.estado, self.fecha_entrega_estimada, self.fecha_entregado, self.version, self.fecha_creacion, self.fecha_actualizacion, self.actualizado_por)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region ACTIVIDADES

class Actividades:

    def __init__(self, id_entregable, nombre, descripcion, estado, fecha_inicio_estimada, fecha_fin_estimada, fecha_inicio_real, fecha_fin_real, id_usuario_responsable, prioridad, orden, observaciones, fecha_creacion, fecha_actualizacion, actualizado_por):
        self.id_entregable = id_entregable
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_inicio_estimada = fecha_inicio_estimada
        self.fecha_fin_estimada = fecha_fin_estimada
        self.fecha_inicio_real = fecha_inicio_real
        self.fecha_fin_real = fecha_fin_real
        self.id_usuario_responsable = id_usuario_responsable
        self.prioridad = prioridad
        self.orden = orden
        self.observaciones = observaciones
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.actualizado_por = actualizado_por

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO actividades (id_entregable, nombre, descripcion, estado, fecha_inicio_estimada, fecha_fin_estimada, fecha_inicio_real, fecha_fin_real, id_usuario_responsable, prioridad, orden, observaciones, fecha_creacion, fecha_actualizacion, actualizado_por) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_entregable, self.nombre, self.descripcion, self.estado, self.fecha_inicio_estimada, self.fecha_fin_estimada, self.fecha_inicio_real, self.fecha_fin_real, self.id_usuario_responsable, self.prioridad, self.orden, self.observaciones, self.fecha_creacion, self.fecha_actualizacion, self.actualizado_por)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region TAREAS

class Tareas:

    def __init__(self, id_actividad, nombre, descripcion, estado, id_usuario_responsable, duracion_optimista, duracion_mas_probable, duracion_pesimista, duracion_estimada, fecha_inicio, fecha_fin, es_critica, orden, observaciones, fecha_creacion, fecha_actualizacion, actualizado_por):
        self.id_actividad = id_actividad
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.id_usuario_responsable = id_usuario_responsable
        self.duracion_optimista = duracion_optimista
        self.duracion_mas_probable = duracion_mas_probable
        self.duracion_pesimista = duracion_pesimista
        self.duracion_estimada = duracion_estimada
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.es_critica = es_critica
        self.orden = orden
        self.observaciones = observaciones
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.actualizado_por = actualizado_por 

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO tareas (id_actividad, nombre, descripcion, estado, id_usuario_responsable, duracion_optimista, duracion_mas_probable, duracion_pesimista, duracion_estimada, fecha_inicio, fecha_fin, es_critica, orden, observaciones, fecha_creacion, fecha_actualizacion, actualizado_por) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_actividad, self.nombre, self.descripcion, self.estado, self.id_usuario_responsable, self.duracion_optimista, self.duracion_mas_probable, self.duracion_pesimista, self.duracion_estimada, self.fecha_inicio, self.fecha_fin, self.es_critica, self.orden, self.observaciones, self.fecha_creacion, self.fecha_actualizacion, self.actualizado_por)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region COSTOS RECURSOS

class Costos_recursos:

    def __init__(self, id_estimacion, tipo, concepto, periodicidad, divisa, cantidad, costo):
        self.id_estimacion = id_estimacion
        self.tipo = tipo 
        self.concepto = concepto
        self.periodicidad = periodicidad
        self.divisa = divisa
        self.cantidad = cantidad
        self.costo = costo

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO costos_recursos (id_estimacion, tipo, concepto, periodicidad, divisa, cantidad, costo) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_estimacion, self.tipo, self.concepto, self.periodicidad, self.divisa, self.cantidad, self.costo)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion

# region COSTOS FREELANCE

class Costos_freelance:

    def __init__(self, id_estimacion, especialidad, nivel, costo_hora, actividad, horas):
        self.id_estimacion = id_estimacion
        self.especialidad = especialidad
        self.nivel = nivel
        self.costo_hora = costo_hora
        self.actividad = actividad
        self.horas = horas

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO costos_freelance (id_estimacion, especialidad, nivel, costo_hora, actividad, horas) VALUES(%s, %s, %s, %s, %s, %s);"
        values = (self.id_estimacion, self.especialidad, self.nivel, self.costo_hora, self.actividad, self.horas)

        mycursor.execute(query, values)
        conn.commit()

        id = mycursor.lastrowid

        mycursor.close()
        conn.close()

        return id

# endregion
















