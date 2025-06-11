import os
import mysql.connector
from sql_data import *

def workbench_db(table='nova_flow'):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database=table
    )

    return mydb

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    APP_NAME = 'Sistema de Gestión de Aliados'
    
    # Navigation menus for each role
    NAVIGATION = {
        'Gestor': [
            {'name': 'Dashboard', 'icon': 'home', 'url': '/dashboard', 
             'submenu': [
                 {'name': 'Crecimiento', 'url': '/dashboard/growth'},
                 {'name': 'Desempeño', 'url': '/dashboard/performance'},
                 {'name': 'Comunidad', 'url': '/dashboard/community'}
             ]},
            {'name': 'Aliados', 'icon': 'users', 'url': '/aliados',
             'submenu': [
                 {'name': 'Usuarios', 'url': '/aliados/usuarios'},
                 {'name': 'Cuentas', 'url': '/aliados/cuentas'},
                 {'name': 'Portafolio', 'url': '/aliados/portfolio'},
                 {'name': 'Asignaciones', 'url': '/aliados/asignaciones'}
             ]}
        ],
        'Aliado': [
            {'name': 'Dashboard de Crecimiento', 'icon': 'activity', 'url': '/dashboard/crecimiento', 'submenu': []},
            {'name': 'Dashboards', 'icon': 'activity', 'url': '/dashboard',
             'submenu': [
                 {'name': 'Crecimiento', 'url': '/dashboard/crecimiento'},
                 {'name': 'Proyectos', 'url': '/dashboard/proyectos'},
                 {'name': 'Cuentas', 'url': '/dashboard/cuentas'},
                 {'name': 'Productividad', 'url': '/dashboard/productividad'},
                 {'name': 'Facturación', 'url': '/dashboard/facturacion'},
                 {'name': 'Riesgos', 'url': '/dashboard/riesgos'}
             ]},
            {'name': 'Proyectos', 'icon': 'briefcase', 'url': '/proyectos',
             'submenu': [
                 {'name': 'General', 'url': '/proyectos/general'},
                 {'name': 'Oportunidades', 'url': '/proyectos/oportunidades'},
                 {'name': 'Propuestas', 'url': '/proyectos/propuestas'},
                 {'name': 'En Desarrollo', 'url': '/proyectos/desarrollo'},
                 {'name': 'Cerrados', 'url': '/proyectos/cerrados'}
             ]},
            {'name': 'Cuentas', 'icon': 'users', 'url': '/cuentas',
             'submenu': [
                 {'name': 'Info Clientes', 'url': '/cuentas/clientes'},
                 {'name': 'Usuarios', 'url': '/cuentas/usuarios'}
             ]}
        ],
        'Supervisor': [
            {'name': 'Dashboard', 'icon': 'home', 'url': '/dashboard'},
            {'name': 'Proyectos', 'icon': 'briefcase', 'url': '/proyectos',
             'submenu': [
                 {'name': 'Gestión de proyectos', 'url': '/proyectos/gestion'},
                 {'name': 'Calculadora', 'url': '/proyectos/calculadora'},
                 {'name': 'Proyectos', 'url': '/proyectos/lista'},
                 {'name': 'Planificación', 'url': '/proyectos/planificacion'},
                 {'name': 'Estimaciones', 'url': '/proyectos/estimaciones'}
             ]},
            {'name': 'Consultores', 'icon': 'user-check', 'url': '/consultores',
             'submenu': [
                 {'name': 'Propuestas', 'url': '/consultores/propuestas'},
                 {'name': 'Activos', 'url': '/consultores/activos'}
             ]}
        ],
        'Consultor': [
            {'name': 'Perfil', 'icon': 'user', 'url': '/consultor/perfil'},
            {'name': 'Mis Proyectos', 'icon': 'briefcase', 'url': '/mis-proyectos'},
            {'name': 'Actividades', 'icon': 'activity', 'url': '/actividades'},
            {'name': 'Propuestas', 'icon': 'file-text', 'url': '/propuestas'}
        ]
    }
    
    # Color scheme
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#3498db',
        'tertiary': '#e74c3c',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#3498db',
        'light': '#ecf0f1',
        'dark': '#2c3e50',
        'white': '#ffffff',
        'black': '#000000'
    }


