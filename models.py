from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

# region MODELOS DE TESTEO

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

# region ORM

# region ACCESO DE USUARIOS

class UserAcces(UserMixin):

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
        return self.estado.lower() == 'activo'

    @staticmethod
    def check_password(password, contraseña_hash):
        return check_password_hash(contraseña_hash, password)

    @staticmethod
    def set_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def get_by_access(correo):
        user = Usuario.query.filter_by(correo=correo, estado=17).first()
        if user:
            return UserAcces(
                id=user.id,
                nombre=user.nombre,
                organizacion=user.rel_organizaciones.nombre if user.rel_organizaciones else None,
                sede=user.rel_sedes.nombre_sede if user.rel_sedes else None,
                correo=user.correo,
                contraseña=user.contrasena,
                rol=user.rel_roles.nombre if user.rel_roles else None,
                estado=user.rel_estados.nombre if user.rel_estados else None,
                ultimo_login=user.ultimo_login
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        user = Usuario.query.get(user_id)
        if not user:
            return None
        return UserAcces(
            id=user.id,
            nombre=user.nombre,
            organizacion=user.rel_organizaciones.nombre if user.rel_organizaciones else None,
            sede=user.rel_sedes.nombre_sede if user.rel_sedes else None,
            correo=user.correo,
            contraseña=user.contrasena,
            rol=user.rel_roles.nombre if user.rel_roles else None,
            estado=user.rel_estados.nombre if user.rel_estados else None,
            ultimo_login=user.ultimo_login
        )


# endregion

# region Usuario

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizaciones.id'))
    id_sede = db.Column(db.Integer, db.ForeignKey('sedes.id'))
    correo = db.Column(db.String, unique=True)
    contrasena = db.Column(db.String)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'))
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    ultimo_login = db.Column(db.DateTime)

    # Relaciones Directas
    rel_organizaciones = db.relationship('Organizacion', foreign_keys=[id_organizacion], back_populates="rel_usuario", lazy='joined')
    rel_sedes = db.relationship('Sede', foreign_keys=[id_sede], back_populates='rel_usuario', lazy='joined')
    rel_roles = db.relationship('Rol', foreign_keys=[id_rol], back_populates='rel_usuario', lazy='joined')
    rel_estados = db.relationship('Estado', foreign_keys=[estado], back_populates='rel_usuario', lazy='joined')

    # Relaciones Inversas
    rel_colaborador = db.relationship('Colaborador', back_populates='rel_usuarios', lazy='joined')
    rel_consultor = db.relationship('Consultor', back_populates='rel_usuarios', lazy='joined')
    rel_persona_cliente = db.relationship('PersonaCliente', back_populates='rel_usuarios', lazy='joined')
    rel_miembro_comunidad = db.relationship('MiembroComunidad', back_populates='rel_usuarios', lazy='joined')
    rel_caso_uso = db.relationship('CasoUso', back_populates='rel_usuarios', lazy='joined')
    rel_exp_laboral = db.relationship('ExpLaboral', back_populates='rel_usuarios', lazy='joined')
    rel_educacion = db.relationship('Educacion', back_populates='rel_usuarios', lazy='joined')
    rel_certificacion = db.relationship('Certificacion', back_populates='rel_usuarios', lazy='joined')
    rel_proyecto_destacado = db.relationship('ProyectoDestacado', back_populates='rel_usuarios', lazy='joined')
    rel_entregable = db.relationship('Entregable', back_populates='rel_usuarios', lazy='joined')
    
    actividades_actualizadas = db.relationship(
        'Actividad',
        back_populates='rel_usuario_actualiza',
        foreign_keys='Actividad.actualizado_por',
        lazy=True
    )

    actividades_asignadas = db.relationship(
        'Actividad',
        back_populates='rel_usuario_responsable',
        foreign_keys='Actividad.id_usuario_responsable',
        lazy=True
    )

    tareas_asignadas = db.relationship(
        'Tarea',
        back_populates='rel_usuario_responsable',
        foreign_keys='Tarea.id_usuario_responsable'
    )

    tareas_actualizadas = db.relationship(
        'Tarea',
        back_populates='actualizado_por_usuario',
        foreign_keys='Tarea.actualizado_por'
    )

    # --- Métodos de seguridad ---
    @staticmethod
    def check_password(password, contraseña_hash):
        return check_password_hash(contraseña_hash, password)

    @staticmethod
    def set_password_hash(password):
        return generate_password_hash(password)

    # --- Guardar usuario ---
    def save(self):
        self.contrasena = Usuario.set_password_hash(self.contrasena)
        db.session.add(self)
        db.session.commit()
        return self.id

    # --- Métodos funcionales ---
    def update_rol(self, nuevo_rol_id):
        self.id_rol = nuevo_rol_id
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_id_by_correo(correo):
        user = Usuario.query.filter_by(correo=correo, estado=17).first()
        return user if user else None

    @staticmethod
    def get_organizaciones():
        return (
            db.session.query(
                func.min(Usuario.id).label("id_usuario"),
                Organizacion.nombre.label("organizacion")
            )
            .join(Organizacion, Usuario.id_organizacion == Organizacion.id)
            .filter(Usuario.estado == 'activo')
            .group_by(Organizacion.nombre)
            .order_by(Organizacion.nombre.asc())
            .all()
        )

    @staticmethod
    def get_tbl_consultores():
        return (
            db.session.query(
                Usuario.id.label("id_usuario"),
                Usuario.nombre,
                Consultor.especialidad,
                Consultor.disponibilidad,
                func.round((Consultor.nivel_segun_usuario + Consultor.nivel_segun_gestor) / 2).label("nivel"),
                Consultor.ciudad,
                Consultor.tarifa_hora.label("tarifa")
            )
            .join(Consultor, Usuario.id == Consultor.id_usuario)
            .filter(Usuario.id_rol == 4)
            .all()
        )

# endregion

# region Organizacion

class Organizacion(db.Model):
    __tablename__ = 'organizaciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    id_industria = db.Column(db.Integer, db.ForeignKey('industrias.id'))
    fecha_registro = db.Column(Date)
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    contacto_principal = db.Column(db.String)
    tamaño = db.Column(db.String)
    empleados = db.Column(db.Integer)

    # Relación Directa
    rel_industrias = db.relationship('Industria', foreign_keys=[id_industria], back_populates='rel_organizacion', lazy='joined')
    rel_estados = db.relationship('Estado', foreign_keys=[estado], back_populates='rel_organizacion', lazy='joined')

    # Relación Inversa
    rel_usuario = db.relationship('Usuario', back_populates='rel_organizaciones', lazy='joined')
    rel_sede = db.relationship('Sede', back_populates='rel_organizaciones', lazy='joined')
    rel_colaborador = db.relationship('Colaborador', back_populates='rel_organizaciones', lazy='joined')
    rel_cuenta = db.relationship('Cuenta', back_populates='rel_organizaciones', lazy='joined')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all_activos():
        return Organizacion.query.filter_by(estado='activo').all()
    
    @staticmethod
    def get_table_orgs():
        # Alias para claridad
        sreg = aliased(Subregion)
        reg = aliased(Region)

        query = (
            db.session.query(
                Organizacion.nombre.label("Organización"),
                Industria.nombre.label("Industria"),
                Organizacion.estado.label("Estado"),
                func.concat(reg.nombre, " (", reg.codigo, ")").label("Región"),
                func.concat(sreg.nombre, " (", sreg.codigo, ")").label("Sub-Región"),
                Sede.pais.label("Pais"),
                Sede.nombre_sede.label("Sede"),
            )
            .outerjoin(Industria, Organizacion.id_industria == Industria.id)
            .outerjoin(Sede, Sede.id_organizacion == Organizacion.id)
            .outerjoin(sreg, Sede.subregion_id == sreg.id)
            .outerjoin(reg, sreg.id_region == reg.id)
        )

        return query.all()
    
# endregion

# region Sede

class Sede(db.Model):
    __tablename__ = 'sedes'

    id = db.Column(db.Integer, primary_key=True)
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizaciones.id'))
    nombre_sede = db.Column(db.String)
    subregion_id = db.Column(db.Integer, db.ForeignKey('subregiones.id'))
    direccion = db.Column(db.String)
    ciudad = db.Column(db.String)
    codigo_postal = db.Column(db.String)
    pais = db.Column(db.String)
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))

    # Relaciones Directas
    rel_organizaciones = db.relationship('Organizacion', back_populates='rel_sede')
    rel_subregiones = db.relationship('Subregion', back_populates='rel_sede')
    rel_estados = db.relationship('Estado', back_populates='rel_sede')

    # Relaciones Inversas
    rel_usuario = db.relationship('Usuario', back_populates='rel_sedes')
    rel_persona_cliente = db.relationship('PersonaCliente', back_populates='rel_sedes')
    rel_caso_uso = db.relationship('CasoUso', back_populates='rel_sedes')
    rel_comunidad_aliado = db.relationship('ComunidadAliado', back_populates='rel_sedes')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Sede.query.all()

    @staticmethod
    def get_orgs():
        query = text("""
            SELECT
                se.id,
                CONCAT(se.nombre_sede, " (", org.nombre, ")") AS nombre_completo
            FROM sedes se
            LEFT JOIN organizaciones org ON se.id_organizacion = org.id
        """)
        result = db.session.execute(query)
        return result.fetchall()
    
    @staticmethod
    def get_paises():
        query = text("""
            SELECT DISTINCT
                pais
            FROM sedes
        """)
        result = db.session.execute(query)
        return result.fetchall()

# endregion

# region SubRegion

class Subregion(db.Model):
    __tablename__ = 'subregiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    codigo = db.Column(db.String)
    descripcion = db.Column(db.Text)
    id_region = db.Column(db.Integer, db.ForeignKey('regiones.id'))
    activo = db.Column(db.Boolean)

    # Relaciones Directas
    rel_regiones = db.relationship('Region', back_populates='rel_subregion')

    # Relaciones Inversas
    rel_sede = db.relationship('Sede', back_populates='rel_subregiones')
    rel_cuenta = db.relationship('Cuenta', back_populates='rel_subregiones')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all_activos():
        return Subregion.query.filter_by(activo=True).all()

# endregion

# region Region

class Region(db.Model):
    __tablename__ = 'regiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    codigo = db.Column(db.String)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean)

    # Relaciones Inversas
    rel_subregion = db.relationship('Subregion', back_populates='rel_regiones')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all_activos():
        return Region.query.filter_by(activo=True).all()

# endregion

# region Colaborador

class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizaciones.id'), nullable=False)
    cargo = db.Column(db.String(255))
    rol_laboral = db.Column(db.String(255))

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_colaborador')
    rel_organizaciones = db.relationship('Organizacion', back_populates='rel_colaborador')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region Industria

class Industria(db.Model):
    __tablename__ = 'industrias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    grupo_general = db.Column(db.String(255))
    sector = db.Column(db.String(255))
    nota = db.Column(db.Text)

    # Relación Inversa
    rel_organizacion = db.relationship('Organizacion', back_populates='rel_industrias')
    rel_cuenta = db.relationship('Cuenta', back_populates='rel_industrias')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Industria.query.order_by(Industria.sector.asc()).all()

# endregion

# region Portafolio

class Portafolio(db.Model):
    __tablename__ = 'portafolio'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255))
    familia = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(255))
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    fecha_creacion = db.Column(db.Date, default=datetime.date.today)
    fecha_actualizacion = db.Column(db.Date, onupdate=datetime.date.today)

    # Relaciones Directas
    rel_estado = db.relationship('Estado', back_populates='rel_portafolios')
    rel_caso_uso = db.relationship('CasoUso', back_populates='rel_portafolios')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Portafolio.query.all()
    
# endregion

# region Consultor

class Consultor(db.Model):
    __tablename__ = 'consultores'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)

    especialidad = db.Column(db.String(255))
    disponibilidad = db.Column(db.String(100))
    nivel_segun_usuario = db.Column(db.String(100))
    nivel_segun_gestor = db.Column(db.String(100))
    fecha_incorporacion = db.Column(db.Date)
    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    pais = db.Column(db.String(100))
    tarifa_hora = db.Column(db.Float)
    resumen_perfil = db.Column(db.Text)
    celular = db.Column(db.String(50))
    linkedin = db.Column(db.String(255))

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_consultor')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_info(self, celular, linkedin, especialidad, nivel, direccion, ciudad, codigo_postal, pais, tarifa_hora, resumen):
        self.celular = celular
        self.linkedin = linkedin
        self.especialidad = especialidad
        self.nivel_segun_usuario = nivel
        self.direccion = direccion
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.pais = pais
        self.tarifa_hora = tarifa_hora
        self.resumen_perfil = resumen
        db.session.commit()

    @staticmethod
    def get_by_usuario_id(id_usuario):
        try:
            return Consultor.query.filter_by(id_usuario=id_usuario).one()
        except NoResultFound:
            return None

# endregion

# region comunidad

class Comunidad(db.Model):
    __tablename__ = 'comunidades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(100))

    # Relaciones Inversas
    rel_miembro_comunidad = db.relationship('MiembroComunidad', back_populates='rel_comunidades')
    rel_comunidad_aliado = db.relationship('ComunidadAliado', back_populates='rel_comunidades')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region PersonaCliente

class PersonaCliente(db.Model):
    __tablename__ = 'personas_cliente'

    id = db.Column(db.Integer, primary_key=True)
    id_sede = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    rol_en_cliente = db.Column(db.String(100))
    fecha_asignacion = db.Column(db.Date)

    # Relaciones Directas
    rel_sedes = db.relationship('Sede', back_populates='rel_persona_cliente')
    rel_usuarios = db.relationship('Usuario', back_populates='rel_persona_cliente')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_consultores_aliado(id_sede):
        from sqlalchemy.sql import text

        query = text("""
            SELECT 
                u.id AS id_usuario,
                u.nombre
            FROM personas_cliente pc
            JOIN usuarios u ON pc.id_usuario = u.id
            WHERE pc.id_sede = :id_sede

            UNION

            SELECT 
                u.id AS id_usuario,
                u.nombre
            FROM comunidad_aliado ca
            JOIN miembros_comunidad mc ON ca.id_comunidad = mc.id_comunidad
            JOIN usuarios u ON mc.id_usuario = u.id
            WHERE ca.id_sede = :id_sede
        """)

        result = db.session.execute(query, {'id_sede': id_sede})
        return result.fetchall()

# endregion

# region MiembroComunidad

class MiembroComunidad(db.Model):
    __tablename__ = 'miembros_comunidad'

    id = db.Column(db.Integer, primary_key=True)
    id_comunidad = db.Column(db.Integer, db.ForeignKey('comunidades.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    rol_en_comunidad = db.Column(db.String(100))
    fecha_union = db.Column(db.Date)

    # Relaciones Directas
    rel_comunidades = db.relationship('Comunidad', back_populates='rel_miembro_comunidad')
    rel_usuarios = db.relationship('Usuario', back_populates='rel_miembro_comunidad')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region ComunidadAliado

class ComunidadAliado(db.Model):
    __tablename__ = 'comunidad_aliado'

    id = db.Column(db.Integer, primary_key=True)
    id_sede = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    id_comunidad = db.Column(db.Integer, db.ForeignKey('comunidades.id'), nullable=False)
    fecha_asignacion = db.Column(db.Date)
    observaciones = db.Column(db.Text)

    # Relaciones Directas
    rel_sedes = db.relationship('Sede', back_populates='rel_comunidad_aliado')
    rel_comunidades = db.relationship('Comunidad', back_populates='rel_comunidad_aliado')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_asignaciones_estrategicas():
        query = text("""
            SELECT 
                s.nombre_sede AS nombre_organizacion,
                c.nombre AS nombre_comunidad,
                c.descripcion AS descripcion,
                u.nombre AS usuario,
                'Comunidad' AS tipo_asignacion,
                mc.rol_en_comunidad AS rol
            FROM comunidad_aliado ca
            JOIN sedes s ON ca.id = s.id
            JOIN comunidades c ON ca.id_comunidad = c.id
            JOIN miembros_comunidad mc ON ca.id_comunidad = mc.id_comunidad
            JOIN usuarios u ON mc.id_usuario = u.id

            UNION ALL

            SELECT 
                s.nombre_sede AS nombre_organizacion,
                NULL AS nombre_comunidad,
                NULL AS descripcion,
                u.nombre AS usuario,
                'Individual' AS tipo_asignacion,
                pc.rol_en_cliente AS rol
            FROM personas_cliente pc
            JOIN sedes s ON pc.id_sede = s.id
            JOIN usuarios u ON pc.id_usuario = u.id

            ORDER BY nombre_organizacion, tipo_asignacion, usuario;
        """)
        return db.session.execute(query).fetchall()

    @staticmethod
    def get_asignaciones_operativas():
        query = text("""
            SELECT 
                org.nombre_sede AS organizacion,
                us.nombre AS nombre_usuario,
                cli.nombre AS Cuenta,
                cu.caso_uso AS caso_uso,
                cu.estado AS estado
            FROM caso_uso cu
            LEFT JOIN sedes org ON cu.id_aliado = org.id
            LEFT JOIN usuarios us ON cu.id_usuario = us.id
            LEFT JOIN cuentas cli ON cu.id_cuenta = cli.id
        """)
        return db.session.execute(query).fetchall()

# endregion

# region CasoUso

class CasoUso(db.Model):
    __tablename__ = 'caso_uso'

    id = db.Column(db.Integer, primary_key=True)
    id_aliado = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    caso_uso = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    impacto = db.Column(db.String(255))
    puntuacion_impacto = db.Column(db.Integer)
    puntuacion_tecnica = db.Column(db.Integer)
    tags = db.Column(db.String(255))
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('portafolio.id'))
    fecha_inicio = db.Column(db.Date)
    fecha_cierre = db.Column(db.Date)
    monto_venta = db.Column(db.Float)
    costos_proyecto = db.Column(db.Float)
    margen_estimado_porcentaje = db.Column(db.Float)
    margen_estimado_bruto = db.Column(db.Float)
    feedback = db.Column(db.Text)

    # Relaciones Directas
    rel_sedes = db.relationship('Sede', back_populates='rel_caso_uso')
    rel_usuarios = db.relationship('Usuario', back_populates='rel_caso_uso')
    rel_cuentas = db.relationship('Cuenta', back_populates='rel_caso_uso')
    rel_estados = db.relationship('Estado', back_populates='rel_caso_uso')
    rel_portafolios = db.relationship('Portafolio', back_populates='rel_caso_uso')
    rel_estimacion = db.relationship('Estimacion', back_populates='rel_casos_uso')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_field(self, campo: str, valor):
        setattr(self, campo, valor)
        db.session.commit()

    # En tu modelo CasoUso
    def to_dict(self):
        return {
            'id': self.id,
            'id_aliado': self.id_aliado,
            'aliado': self.rel_sedes.nombre_sede if self.rel_sedes else None,
            'id_usuario': self.id_usuario,
            'usuario': self.rel_usuarios.nombre if self.rel_usuarios else None,
            'id_cuenta': self.id_cuenta,
            'cuenta': self.rel_cuentas.nombre if self.rel_cuentas else None,
            'caso_uso': self.caso_uso,
            'descripcion': self.descripcion,
            'impacto': self.impacto,
            'puntuacion_impacto': self.puntuacion_impacto,
            'puntuacion_tecnica': self.puntuacion_tecnica,
            'tags': self.tags,
            'estado': self.estado,
            'id_producto': self.id_producto,
            'producto': self.rel_portafolios.nombre if self.rel_portafolios else None,
            'fecha_inicio': self.fecha_inicio,
            'fecha_cierre': self.fecha_cierre,
            'monto_venta': self.monto_venta,
            'costos_proyecto': self.costos_proyecto,
            'margen_estimado_porcentaje': self.margen_estimado_porcentaje,
            'margen_estimado_bruto': self.margen_estimado_bruto,
            'feedback': self.feedback
        }

    @staticmethod
    def get_projects_to_sup(id_usuario):
        return CasoUso.query.filter_by(id_usuario=id_usuario).all()

    @staticmethod
    def get_by_id(id):
        return CasoUso.query.get(id)

# endregion

# region Cuenta

class Cuenta(db.Model):
    __tablename__ = 'cuentas'

    id = db.Column(db.Integer, primary_key=True)
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizaciones.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    industria = db.Column(db.Integer, db.ForeignKey('industrias.id'))
    subregion = db.Column(db.Integer, db.ForeignKey('subregiones.id'))
    fecha_alta = db.Column(db.Date)
    fecha_modificacion = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    codigo = db.Column(db.String(100))
    id_segmentacion = db.Column(db.Integer, db.ForeignKey('segmentacion.id'))
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))

    # Relaciones Directas
    rel_organizaciones = db.relationship('Organizacion', back_populates='rel_cuenta')
    rel_industrias = db.relationship('Industria', back_populates='rel_cuenta')
    rel_subregiones = db.relationship('Subregion', back_populates='rel_cuenta')
    rel_segmentaciones = db.relationship('Segmentacion', back_populates='rel_cuenta')
    rel_estados = db.relationship('Estado', back_populates='rel_cuenta')

    # Relaciones inversas
    rel_caso_uso = db.relationship('CasoUso', back_populates='rel_cuentas')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all_tbl():
        return (
            db.session.query(
                Cuenta.id,
                Cuenta.nombre,
                (Industria.nombre + " " + Industria.grupo_general).label("industria"),
                Cuenta.estado,
                func.count(CasoUso.id).label("proyectos_activos")
            )
            .outerjoin(Industria, Cuenta.industria == Industria.id)
            .outerjoin(CasoUso, Cuenta.id == CasoUso.id_cuenta)
            .group_by(Cuenta.id, Cuenta.nombre, Industria.nombre, Industria.grupo_general, Cuenta.estado)
            .all()
        )

    @staticmethod
    def get_cuentas_by_aliado(id_organizacion):
        return Cuenta.query.filter_by(id_organizacion=id_organizacion).all()

# endregion

# region Segmentacion

class Segmentacion(db.Model):
    __tablename__ = 'segmentacion'

    id = db.Column(db.Integer, primary_key=True)
    clasificacion = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

    # Relaciones inversas
    rel_cuenta = db.relationship('Cuenta', back_populates='rel_segmentaciones')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Segmentacion.query.all()

# endregion

# region Rol

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relación Inversa
    rel_usuario = db.relationship('Usuario', back_populates='rel_roles')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region ExpLaboral

class ExpLaboral(db.Model):
    __tablename__ = 'experiencia_laboral'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cargo = db.Column(db.String(255))
    empresa = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    ubicacion = db.Column(db.String(255))
    tipo_empleo = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    logros = db.Column(db.Text)

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_exp_laboral')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id_usuario(id_usuario):
        return ExpLaboral.query.filter_by(id_usuario=id_usuario).all()

# endregion

# region Educacion

class Educacion(db.Model):
    __tablename__ = 'educacion'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    institucion = db.Column(db.String(255))
    titulo = db.Column(db.String(255))
    area_estudio = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    descripcion = db.Column(db.Text)

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_educacion')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id_usuario(id_usuario):
        return Educacion.query.filter_by(id_usuario=id_usuario).all()

# endregion

# region Certificacion

class Certificacion(db.Model):
    __tablename__ = 'certificaciones'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(255))
    entidad = db.Column(db.String(255))
    fecha_obtencion = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    url_certificado = db.Column(db.String(255))
    id_credencial = db.Column(db.String(255))
    descripcion = db.Column(db.Text)

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_certificacion')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id_usuario(id_usuario):
        return Certificacion.query.filter_by(id_usuario=id_usuario).all()

# endregion

# region ProyectoDestacado

class ProyectoDestacado(db.Model):
    __tablename__ = 'proyectos_destacados'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    tecnologias_usadas = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    link_portafolio = db.Column(db.String(255))

    # Relaciones Directas
    rel_usuarios = db.relationship('Usuario', back_populates='rel_proyecto_destacado')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id_usuario(id_usuario):
        return ProyectoDestacado.query.filter_by(id_usuario=id_usuario).all()

# endregion

# region Estado

class Estado(db.Model):
    __tablename__ = 'estados'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    entidad = db.Column(db.String(100))

    # Relaciones Inversas
    rel_usuario = db.relationship('Usuario', back_populates='rel_estados')
    rel_organizacion = db.relationship('Organizacion', back_populates='rel_estados')
    rel_sede = db.relationship('Sede', back_populates='rel_estados')
    rel_portafolios = db.relationship('Portafolio', back_populates='rel_estado')
    rel_caso_uso = db.relationship('CasoUso', back_populates='rel_estados')
    rel_cuenta = db.relationship('Cuenta', back_populates='rel_estados')
    rel_entregable = db.relationship('Entregable', back_populates='rel_estados')
    rel_actividad = db.relationship('Actividad', back_populates='rel_estados')
    rel_tareas = db.relationship('Tarea', back_populates='rel_estado', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region Estimacion

class Estimacion(db.Model):
    __tablename__ = 'estimaciones'

    id = db.Column(db.Integer, primary_key=True)
    id_caso_uso = db.Column(db.Integer, db.ForeignKey('caso_uso.id'), nullable=False)
    nombre_caso_uso = db.Column(db.String(255), nullable=False)

    # Relaciones Directas
    rel_casos_uso = db.relationship('CasoUso', back_populates='rel_estimacion')

    # Relaciones Inversas
    rel_entregable = db.relationship('Entregable', back_populates='rel_estimaciones')
    rel_costo_recurso = db.relationship('CostoRecurso', back_populates='rel_estimaciones')
    rel_costo_freelance = db.relationship('CostoFreelance', back_populates='rel_estimaciones')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region Entregable

class Entregable(db.Model):
    __tablename__ = 'entregables'

    id = db.Column(db.Integer, primary_key=True)
    id_estimacion = db.Column(db.Integer, db.ForeignKey('estimaciones.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    criterios_aceptacion = db.Column(db.Text)
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    fecha_entrega_estimada = db.Column(db.Date)
    fecha_entregado = db.Column(db.Date)
    version = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    actualizado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # Relaciones Directas
    rel_estimaciones = db.relationship('Estimacion', back_populates='rel_entregable')
    rel_estados = db.relationship('Estado', back_populates='rel_entregable')
    rel_usuarios = db.relationship('Usuario', back_populates='rel_entregable')

    # Relaciones Inversas
    rel_actividad = db.relationship('Actividad', back_populates='rel_entregables')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region Actividad

class Actividad(db.Model):
    __tablename__ = 'actividades'

    id = db.Column(db.Integer, primary_key=True)
    id_entregable = db.Column(db.Integer, db.ForeignKey('entregables.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    fecha_inicio_estimada = db.Column(db.Date)
    fecha_fin_estimada = db.Column(db.Date)
    fecha_inicio_real = db.Column(db.Date)
    fecha_fin_real = db.Column(db.Date)
    id_usuario_responsable = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    prioridad = db.Column(db.String(50))
    orden = db.Column(db.Integer)
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    actualizado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # Relaciones Directas
    rel_entregables = db.relationship('Entregable', back_populates='rel_actividad')
    rel_estados = db.relationship('Estado', back_populates='rel_actividad')

    rel_usuario_responsable = db.relationship(
        'Usuario',
        back_populates='actividades_asignadas',
        foreign_keys=[id_usuario_responsable]
    )

    rel_usuario_actualiza = db.relationship(
        'Usuario',
        back_populates='actividades_actualizadas',
        foreign_keys=[actualizado_por]
    )
    
    tareas = db.relationship(
        'Tarea',
        back_populates='rel_actividad',
        lazy=True
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region Tarea

class Tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.Column(db.Integer, primary_key=True)
    id_actividad = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Integer, db.ForeignKey('estados.id'))
    id_usuario_responsable = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    duracion_optimista = db.Column(db.Float)
    duracion_mas_probable = db.Column(db.Float)
    duracion_pesimista = db.Column(db.Float)
    duracion_estimada = db.Column(db.Float)

    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    es_critica = db.Column(db.Boolean, default=False)
    orden = db.Column(db.Integer)
    observaciones = db.Column(db.Text)

    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    actualizado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # Relaciones Directas
    rel_actividad = db.relationship(
        'Actividad',
        back_populates='tareas',
        foreign_keys=[id_actividad]
    )
    rel_estado = db.relationship('Estado', back_populates='rel_tareas', lazy=True)

    rel_usuario_responsable = db.relationship(
        'Usuario',
        back_populates='tareas_asignadas',
        foreign_keys=[id_usuario_responsable]
    )

    actualizado_por_usuario = db.relationship(
        'Usuario',
        back_populates='tareas_actualizadas',
        foreign_keys=[actualizado_por]
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# region CostoRecurso

class CostoRecurso(db.Model):
    __tablename__ = 'costos_recursos'

    id = db.Column(db.Integer, primary_key=True)
    id_estimacion = db.Column(db.Integer, db.ForeignKey('estimaciones.id'), nullable=False)
    tipo = db.Column(db.String(100))              # Ej: 'humano', 'infraestructura', etc.
    concepto = db.Column(db.String(255))          # Ej: 'Backend Developer', 'Licencia', etc.
    periodicidad = db.Column(db.String(50))       # Ej: 'mensual', 'único', etc.
    divisa = db.Column(db.String(10))             # Ej: 'COP', 'USD', etc.
    cantidad = db.Column(db.Float)
    costo = db.Column(db.Float)                   # Valor unitario

    # Estimaciones Directas
    rel_estimaciones = db.relationship('Estimacion', back_populates='rel_costo_recurso')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion 

# region CostoFreelance

class CostoFreelance(db.Model):
    __tablename__ = 'costos_freelance'

    id = db.Column(db.Integer, primary_key=True)
    id_estimacion = db.Column(db.Integer, db.ForeignKey('estimaciones.id'), nullable=False)
    especialidad = db.Column(db.String(100))           # Ej: 'Data Scientist', 'UX Designer'
    nivel = db.Column(db.String(100))                  # Ej: 'Junior', 'Senior'
    costo_hora = db.Column(db.Float)                   # Valor por hora
    actividad = db.Column(db.String(255))              # Descripción breve de la tarea
    horas = db.Column(db.Float)                        # Total de horas estimadas

    # Relaciones Directas
    rel_estimaciones = db.relationship('Estimacion', back_populates='rel_costo_freelance')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

# endregion

# endregion

