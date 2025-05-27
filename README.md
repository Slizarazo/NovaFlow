
# NovaFlow - Sistema de Gestión de Aliados

## Descripción General

NovaFlow es un sistema web integral de gestión de aliados, proyectos y consultores desarrollado con Flask. El sistema permite la administración completa de relaciones comerciales, seguimiento de proyectos, gestión de recursos humanos freelance y análisis de rendimiento empresarial a través de dashboards interactivos.

## Características Principales

### 🔐 Sistema de Autenticación Multi-Rol
- **Gestor**: Administración general del sistema y supervisión de aliados
- **Aliado**: Gestión de proyectos, cuentas y análisis de crecimiento
- **Supervisor**: Coordinación de consultores y estimaciones de proyectos
- **Consultor**: Acceso a proyectos asignados y tareas

### 📊 Dashboards Especializados
- **Dashboard de Crecimiento**: Análisis de ventas, tendencias y KPIs de negocio
- **Dashboard de Desempeño**: Seguimiento de proyectos y consultores
- **Dashboard de Proyectos**: Gestión del ciclo de vida de proyectos
- **Dashboard de Productividad**: Métricas de eficiencia y recursos
- **Dashboard de Facturación**: Control financiero y flujo de caja
- **Dashboard de Riesgos**: Matriz de riesgos y alertas tempranas
- **Dashboard de Cuentas**: Segmentación y satisfacción de clientes
- **Dashboard de Comunidad**: Desarrollo profesional y métricas comunitarias

### 🎯 Gestión de Proyectos
- **Kanban Board**: Visualización de proyectos por estado (Oportunidad, Propuesta, Aprobado, Desarrollo, Testing, Cierre, Evaluación)
- **Calculadora de Tiempos**: Herramienta para estimación de recursos y costos
- **Seguimiento de Estimaciones**: Registro y aprobación de propuestas
- **Gestión de Estados**: Control completo del ciclo de vida del proyecto

### 👥 Administración de Recursos
- **Gestión de Usuarios**: Creación y administración de diferentes tipos de usuario
- **Red de Consultores**: Asignación y seguimiento de freelancers
- **Aliados Comerciales**: Gestión de relaciones y cuentas estratégicas
- **Asignaciones**: Coordinación de recursos por proyecto

### 📈 Análisis y Reportes
- **Gráficos Interactivos**: Visualizaciones con Plotly y Matplotlib
- **Mapas Geográficos**: Ubicaciones de operaciones con Folium
- **KPIs en Tiempo Real**: Métricas de ventas, rentabilidad y crecimiento
- **Análisis Predictivo**: Tendencias y proyecciones de negocio

## Tecnologías Utilizadas

### Backend
- **Flask 3.1.0**: Framework web principal
- **Flask-Login 0.6.3**: Gestión de autenticación y sesiones
- **Flask-SQLAlchemy 3.1.1**: ORM para base de datos
- **Flask-WTF 1.2.2**: Manejo de formularios y CSRF
- **Gunicorn 23.0.0**: Servidor WSGI para producción

### Visualización de Datos
- **Plotly 6.0.1**: Gráficos interactivos avanzados
- **Matplotlib 3.10.1**: Gráficos estáticos y análisis
- **Folium 0.19.5**: Mapas interactivos y geolocalización

### Procesamiento de Datos
- **Pandas 2.2.3**: Manipulación y análisis de datos
- **NumPy 2.2.5**: Computación numérica

### Frontend
- **HTML5/CSS3**: Estructura y estilos responsivos
- **JavaScript**: Interactividad y funcionalidades dinámicas
- **Bootstrap**: Framework CSS para diseño responsivo
- **Tema DEEPNOVA**: Diseño personalizado con esquema de colores corporativo

## Estructura del Proyecto

```
NovaFlow/
├── app.py                 # Configuración principal de Flask
├── main.py               # Punto de entrada de la aplicación
├── routes.py             # Definición de rutas y endpoints
├── models.py             # Modelos de datos y clases
├── config.py             # Configuración del sistema
├── graphs.py             # Generación de gráficos y visualizaciones
├── data_demo.py          # Datos de demostración extendidos
├── static/
│   ├── css/              # Hojas de estilo
│   ├── js/               # Scripts JavaScript
│   └── images/           # Recursos gráficos
├── templates/
│   ├── dashboard/        # Plantillas de dashboards
│   ├── proyectos/        # Gestión de proyectos
│   ├── aliados/          # Administración de aliados
│   ├── cuentas/          # Gestión de cuentas
│   └── layout.html       # Plantilla base
└── README.md
```

## Instalación y Configuración

### Requisitos Previos
- Python 3.11+
- Acceso a internet para dependencias externas

### Configuración en Replit
1. **Clonar o importar** el proyecto en Replit
2. **Instalar dependencias**: Se instalan automáticamente desde `pyproject.toml`
3. **Ejecutar aplicación**: Usar el botón "Run" o el comando `gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app`

### Variables de Entorno
```bash
SESSION_SECRET=tu-clave-secreta-aqui
```

## Uso del Sistema

### Credenciales de Acceso
- **Gestor**: `gestor1` / `password`
- **Aliado**: `aliado1` / `password`
- **Supervisor**: `supervisor1` / `password`
- **Consultor**: `consultor1` / `password`

### Funcionalidades por Rol

#### 👨‍💼 Gestor
- Supervisión general del sistema
- Gestión de usuarios y aliados
- Análisis de crecimiento y desempeño
- Administración de la comunidad de consultores

#### 🤝 Aliado
- Dashboard de crecimiento con KPIs personalizados
- Gestión completa de proyectos
- Análisis de productividad y facturación
- Control de riesgos y cuentas

#### 👨‍💻 Supervisor
- Coordinación de consultores y proyectos
- Calculadora de estimaciones de tiempo
- Gestión de propuestas y recursos
- Seguimiento de asignaciones

#### 🧑‍🎓 Consultor
- Acceso a proyectos asignados
- Seguimiento de tareas personales
- Dashboard personalizado

## API Endpoints

### Autenticación
- `GET /login` - Página de inicio de sesión
- `POST /login` - Procesamiento de credenciales
- `GET /logout` - Cerrar sesión

### Dashboards
- `GET /dashboard` - Dashboard principal según rol
- `GET /dashboard/growth` - Dashboard de crecimiento
- `GET /dashboard/performance` - Dashboard de desempeño
- `GET /dashboard/proyectos` - Dashboard de proyectos
- `GET /dashboard/productividad` - Dashboard de productividad
- `GET /dashboard/facturacion` - Dashboard de facturación
- `GET /dashboard/riesgos` - Dashboard de riesgos
- `GET /dashboard/cuentas` - Dashboard de cuentas
- `GET /dashboard/community` - Dashboard de comunidad

### Gestión de Proyectos
- `GET /proyectos/calculadora` - Calculadora de tiempos
- `GET /proyectos/estimaciones` - Lista de estimaciones
- `GET /proyectos/general` - Vista general de proyectos

### APIs REST
- `POST /api/usuarios` - Crear usuario
- `POST /api/proyectos` - Crear proyecto
- `POST /api/aliados` - Crear aliado
- `POST /api/asignaciones` - Crear asignación
- `POST /api/oportunidades` - Crear oportunidad
- `PUT /api/proyecto/<id>` - Actualizar proyecto

## Características Técnicas

### Seguridad
- Autenticación basada en sesiones con Flask-Login
- Protección CSRF en formularios
- Validación de roles y permisos por endpoint

### Rendimiento
- Datos en memoria para demostración rápida
- Carga lazy de gráficos complejos
- Optimización de consultas y renderizado

### Responsividad
- Diseño adaptable para dispositivos móviles
- Sidebar colapsible en pantallas pequeñas
- Componentes flexibles y escalables

### Extensibilidad
- Arquitectura modular y escalable
- Sistema de roles fácilmente extensible
- API REST preparada para integraciones

## Desarrollo y Contribución

### Estructura de Archivos Clave
- **routes.py**: Lógica de endpoints y controladores
- **models.py**: Definición de entidades y datos
- **graphs.py**: Generación de visualizaciones
- **config.py**: Configuración de navegación y roles
- **templates/**: Plantillas HTML organizadas por módulo

### Personalización
- **Temas**: Modificar `static/css/deepnova-theme.css`
- **Gráficos**: Extender funciones en `graphs.py`
- **Datos**: Actualizar `models.py` y `data_demo.py`
- **Navegación**: Configurar menús en `config.py`

## Despliegue

### Replit (Recomendado)
1. El proyecto está optimizado para Replit
2. Puerto configurado en 5000 para acceso web
3. Dependencias gestionadas automáticamente
4. Despliegue directo con el botón "Run"

### Producción
- Servidor: Gunicorn con configuración para alta concurrencia
- Base de datos: Preparado para PostgreSQL con psycopg2
- Escalabilidad: Arquitectura preparada para múltiples workers

## Licencia

Este proyecto es desarrollado como sistema empresarial propietario para la gestión de aliados y consultores.

## Soporte

Para soporte técnico o consultas sobre funcionalidades, contactar al equipo de desarrollo a través de los canales establecidos en la organización.

---

**NovaFlow** - Transformando la gestión de aliados y proyectos con tecnología innovadora.
