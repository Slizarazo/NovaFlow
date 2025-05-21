import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    APP_NAME = 'Sistema de Gestión de Aliados'
    
    # Navigation menus for each role
    NAVIGATION = {
        'gestor': [
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
        'aliado': [
            {'name': 'Dashboard', 'icon': 'home', 'url': '/dashboard'},
            {'name': 'Proyectos', 'icon': 'briefcase', 'url': '/proyectos'},
            {'name': 'Consultores', 'icon': 'user-check', 'url': '/consultores'}
        ],
        'supervisor': [
            {'name': 'Dashboard', 'icon': 'home', 'url': '/dashboard'},
            {'name': 'Proyectos', 'icon': 'briefcase', 'url': '/proyectos'},
            {'name': 'Aliados', 'icon': 'users', 'url': '/aliados'},
            {'name': 'Consultores', 'icon': 'user-check', 'url': '/consultores'}
        ],
        'consultor': [
            {'name': 'Dashboard', 'icon': 'home', 'url': '/dashboard'},
            {'name': 'Mis Proyectos', 'icon': 'briefcase', 'url': '/mis-proyectos'},
            {'name': 'Tareas', 'icon': 'check-square', 'url': '/tareas'}
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
