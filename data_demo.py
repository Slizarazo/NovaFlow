"""
Archivo con datos de demostración para visualizar todas las gráficas y 
completar el ciclo de gestión del sistema de aliados y consultores.
"""

# Definición de modelos y datos ampliados para demostración

class DatosDemoCompleto:
    """
    Datos ampliados para todas las visualizaciones del sistema,
    siguiendo el ciclo de 5 etapas:
    1. Onboarding del Aliado
    2. Propuesta de Proyecto
    3. Ejecución
    4. Cierre
    5. Retención de Talento
    """

    # ETAPA 1: ONBOARDING - DATOS PARA DASHBOARD DE ALIADOS
    ALIADOS_EXTENDIDOS = [
        {
            'id': 1,
            'nombre': 'Aliado Tech',
            'region': 'Norte',
            'industria': 'Tecnología',
            'ventas_trimestre': 125000,
            'ventas_acumuladas': 450000,
            'fecha_registro': '2023-01-15',
            'estado': 'activo',
            'contacto_principal': 'María González',
            'email': 'maria.gonzalez@aliadotech.com',
            'telefono': '+52 55 1234 5678',
            'tamano': 'Grande',
            'empleados': 1200,
            'proyectos_activos': 3,
            'nivel_satisfaccion': 4.8,
            'direccion': {
                'calle': 'Av. Revolución 1520',
                'ciudad': 'Ciudad de México',
                'estado': 'CDMX',
                'cp': '01030',
                'pais': 'México'
            }
        },
        {
            'id': 2,
            'nombre': 'Financiera Global',
            'region': 'Centro',
            'industria': 'Finanzas',
            'ventas_trimestre': 98000,
            'ventas_acumuladas': 320000,
            'fecha_registro': '2023-02-10',
            'estado': 'activo',
            'contacto_principal': 'Juan Pérez',
            'email': 'juan.perez@financieraglobal.com',
            'telefono': '+52 55 8765 4321',
            'tamano': 'Mediana',
            'empleados': 450,
            'proyectos_activos': 1,
            'nivel_satisfaccion': 4.2,
            'direccion': {
                'calle': 'Paseo de la Reforma 222',
                'ciudad': 'Ciudad de México',
                'estado': 'CDMX',
                'cp': '06600',
                'pais': 'México'
            }
        },
        {
            'id': 3,
            'nombre': 'Industrias Este',
            'region': 'Este',
            'industria': 'Manufactura',
            'ventas_trimestre': 110000,
            'ventas_acumuladas': 390000,
            'fecha_registro': '2023-01-28',
            'estado': 'activo',
            'contacto_principal': 'Roberto Sánchez',
            'email': 'roberto.sanchez@industriaseste.com',
            'telefono': '+52 81 2345 6789',
            'tamano': 'Grande',
            'empleados': 850,
            'proyectos_activos': 2,
            'nivel_satisfaccion': 4.5,
            'direccion': {
                'calle': 'Av. Industrial 450',
                'ciudad': 'Monterrey',
                'estado': 'Nuevo León',
                'cp': '64000',
                'pais': 'México'
            }
        },
        {
            'id': 4,
            'nombre': 'Consultores Sur',
            'region': 'Sur',
            'industria': 'Consultoría',
            'ventas_trimestre': 85000,
            'ventas_acumuladas': 280000,
            'fecha_registro': '2023-03-05',
            'estado': 'activo',
            'contacto_principal': 'Laura Ramírez',
            'email': 'laura.ramirez@consultoressur.com',
            'telefono': '+52 99 8765 4321',
            'tamano': 'Pequeña',
            'empleados': 120,
            'proyectos_activos': 1,
            'nivel_satisfaccion': 4.7,
            'direccion': {
                'calle': 'Calle 60 Norte 150',
                'ciudad': 'Mérida',
                'estado': 'Yucatán',
                'cp': '97000',
                'pais': 'México'
            }
        },
        {
            'id': 5,
            'nombre': 'Servicios Oeste',
            'region': 'Oeste',
            'industria': 'Servicios',
            'ventas_trimestre': 102000,
            'ventas_acumuladas': 350000,
            'fecha_registro': '2023-02-18',
            'estado': 'activo',
            'contacto_principal': 'Carlos Mendoza',
            'email': 'carlos.mendoza@serviciosoeste.com',
            'telefono': '+52 33 1234 5678',
            'tamano': 'Mediana',
            'empleados': 320,
            'proyectos_activos': 2,
            'nivel_satisfaccion': 4.3,
            'direccion': {
                'calle': 'Av. López Mateos 1800',
                'ciudad': 'Guadalajara',
                'estado': 'Jalisco',
                'cp': '45050',
                'pais': 'México'
            }
        },
        {
            'id': 6,
            'nombre': 'Innovación Digital',
            'region': 'Norte',
            'industria': 'Tecnología',
            'ventas_trimestre': 115000,
            'ventas_acumuladas': 380000,
            'fecha_registro': '2023-03-20',
            'estado': 'activo',
            'contacto_principal': 'Andrea Torres',
            'email': 'andrea.torres@innovaciondigital.com',
            'telefono': '+52 55 9876 5432',
            'tamano': 'Mediana',
            'empleados': 280,
            'proyectos_activos': 1,
            'nivel_satisfaccion': 4.6,
            'direccion': {
                'calle': 'Insurgentes Sur 1000',
                'ciudad': 'Ciudad de México',
                'estado': 'CDMX',
                'cp': '03100',
                'pais': 'México'
            }
        },
        {
            'id': 7,
            'nombre': 'Logística Rápida',
            'region': 'Centro',
            'industria': 'Logística',
            'ventas_trimestre': 92000,
            'ventas_acumuladas': 310000,
            'fecha_registro': '2023-02-25',
            'estado': 'activo',
            'contacto_principal': 'Patricia Gutiérrez',
            'email': 'patricia.gutierrez@logisticarapida.com',
            'telefono': '+52 55 2345 6789',
            'tamano': 'Pequeña',
            'empleados': 150,
            'proyectos_activos': 1,
            'nivel_satisfaccion': 4.4,
            'direccion': {
                'calle': 'Periférico Sur 4690',
                'ciudad': 'Ciudad de México',
                'estado': 'CDMX',
                'cp': '14140',
                'pais': 'México'
            }
        },
        {
            'id': 8,
            'nombre': 'Construcciones Modernas',
            'region': 'Este',
            'industria': 'Construcción',
            'ventas_trimestre': 130000,
            'ventas_acumuladas': 420000,
            'fecha_registro': '2023-01-10',
            'estado': 'activo',
            'contacto_principal': 'Héctor Martínez',
            'email': 'hector.martinez@construccionesmodernas.com',
            'telefono': '+52 81 9876 5432',
            'tamano': 'Grande',
            'empleados': 950,
            'proyectos_activos': 2,
            'nivel_satisfaccion': 4.1,
            'direccion': {
                'calle': 'Constitución 800',
                'ciudad': 'Monterrey',
                'estado': 'Nuevo León',
                'cp': '64000',
                'pais': 'México'
            }
        }
    ]

    # ETAPA 2: PROPUESTA Y PLANIFICACIÓN - DATOS DE PROYECTOS
    PROYECTOS_EXTENDIDOS = [
        {
            'id': 1,
            'nombre': 'Transformación Digital',
            'aliado_id': 1,
            'etapa': 'ejecucion',
            'fecha_inicio': '2023-01-15',
            'fecha_fin': '2023-06-30',
            'monto': 85000,
            'consultores_asignados': 4,
            'descripcion': 'Implementación de estrategia de transformación digital completa, incluyendo migración a la nube, automatización de procesos y capacitación de personal.',
            'objetivos': [
                'Reducir costos operativos en un 25%',
                'Mejorar la eficiencia de procesos en un 30%',
                'Capacitar al 100% del personal en nuevas tecnologías'
            ],
            'hitos': [
                {'nombre': 'Inicio y planificación', 'fecha': '2023-01-15', 'completado': True},
                {'nombre': 'Análisis y diseño', 'fecha': '2023-02-20', 'completado': True},
                {'nombre': 'Implementación fase 1', 'fecha': '2023-04-10', 'completado': True},
                {'nombre': 'Implementación fase 2', 'fecha': '2023-05-25', 'completado': False},
                {'nombre': 'Cierre y evaluación', 'fecha': '2023-06-30', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Resistencia al cambio', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Plan de gestión del cambio'},
                {'nombre': 'Retrasos en implementación', 'impacto': 'Medio', 'probabilidad': 'Baja', 'mitigacion': 'Cronograma con buffers'}
            ],
            'presupuesto_desglosado': {
                'consultoria': 55000,
                'licencias': 15000,
                'capacitacion': 10000,
                'otros': 5000
            }
        },
        {
            'id': 2,
            'nombre': 'Optimización Procesos',
            'aliado_id': 2,
            'etapa': 'planificacion',
            'fecha_inicio': '2023-02-10',
            'fecha_fin': '2023-09-20',
            'monto': 72000,
            'consultores_asignados': 3,
            'descripcion': 'Revisión y rediseño de procesos financieros y administrativos para mejorar la eficiencia operativa y reducir costos.',
            'objetivos': [
                'Optimizar procesos administrativos reduciendo tiempos en un 30%',
                'Implementar automatización en al menos 5 procesos clave',
                'Reducir costos operativos en un 20%'
            ],
            'hitos': [
                {'nombre': 'Inicio del proyecto', 'fecha': '2023-02-10', 'completado': True},
                {'nombre': 'Diagnóstico y mapeo de procesos', 'fecha': '2023-03-25', 'completado': True},
                {'nombre': 'Diseño de nuevos procesos', 'fecha': '2023-05-15', 'completado': False},
                {'nombre': 'Implementación y pruebas', 'fecha': '2023-07-30', 'completado': False},
                {'nombre': 'Capacitación y cierre', 'fecha': '2023-09-20', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Falta de compromiso directivo', 'impacto': 'Alto', 'probabilidad': 'Baja', 'mitigacion': 'Involucrar a directivos clave'},
                {'nombre': 'Información incompleta', 'impacto': 'Medio', 'probabilidad': 'Media', 'mitigacion': 'Planificación detallada de recolección de datos'}
            ],
            'presupuesto_desglosado': {
                'consultoria': 48000,
                'software': 12000,
                'capacitacion': 8000,
                'otros': 4000
            }
        },
        {
            'id': 3,
            'nombre': 'Implementación ERP',
            'aliado_id': 3,
            'etapa': 'propuesta',
            'fecha_inicio': '2023-03-05',
            'fecha_fin': '2023-08-15',
            'monto': 95000,
            'consultores_asignados': 5,
            'descripcion': 'Implementación de sistema ERP para integrar todas las áreas del negocio, incluyendo producción, finanzas, RRHH, ventas y logística.',
            'objetivos': [
                'Integrar todos los procesos de negocio en un único sistema',
                'Mejorar la calidad y accesibilidad de la información para toma de decisiones',
                'Aumentar la productividad en un 25%'
            ],
            'hitos': [
                {'nombre': 'Inicio y análisis de requerimientos', 'fecha': '2023-03-05', 'completado': True},
                {'nombre': 'Selección de solución', 'fecha': '2023-04-10', 'completado': False},
                {'nombre': 'Configuración y adaptación', 'fecha': '2023-05-30', 'completado': False},
                {'nombre': 'Migración de datos', 'fecha': '2023-07-15', 'completado': False},
                {'nombre': 'Pruebas y capacitación', 'fecha': '2023-08-10', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Resistencia al cambio', 'impacto': 'Alto', 'probabilidad': 'Alta', 'mitigacion': 'Plan de gestión del cambio y comunicación'},
                {'nombre': 'Problemas de integración', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Pruebas exhaustivas de integración'}
            ],
            'presupuesto_desglosado': {
                'licencias': 30000,
                'consultoria': 45000,
                'infraestructura': 15000,
                'capacitacion': 5000
            }
        },
        {
            'id': 4,
            'nombre': 'Estrategia de Mercado',
            'aliado_id': 4,
            'etapa': 'cierre',
            'fecha_inicio': '2023-01-20',
            'fecha_fin': '2023-04-10',
            'monto': 45000,
            'consultores_asignados': 2,
            'descripcion': 'Desarrollo e implementación de estrategia de marketing digital y posicionamiento de mercado para nuevos servicios.',
            'objetivos': [
                'Aumentar el posicionamiento de marca en un 30%',
                'Incrementar tráfico web en un 50%',
                'Elevar las conversiones en un 25%'
            ],
            'hitos': [
                {'nombre': 'Análisis de mercado', 'fecha': '2023-01-25', 'completado': True},
                {'nombre': 'Desarrollo de estrategia', 'fecha': '2023-02-15', 'completado': True},
                {'nombre': 'Implementación de campañas', 'fecha': '2023-03-01', 'completado': True},
                {'nombre': 'Medición y ajustes', 'fecha': '2023-03-30', 'completado': True},
                {'nombre': 'Evaluación de resultados', 'fecha': '2023-04-10', 'completado': True}
            ],
            'riesgos': [
                {'nombre': 'Cambios en el mercado', 'impacto': 'Medio', 'probabilidad': 'Media', 'mitigacion': 'Monitoreo constante del entorno'},
                {'nombre': 'Bajo ROI inicial', 'impacto': 'Medio', 'probabilidad': 'Alta', 'mitigacion': 'Plan escalonado de inversión'}
            ],
            'presupuesto_desglosado': {
                'consultoria': 25000,
                'publicidad': 15000,
                'herramientas': 3000,
                'otros': 2000
            }
        },
        {
            'id': 5,
            'nombre': 'Mejora Continua',
            'aliado_id': 5,
            'etapa': 'post-evaluacion',
            'fecha_inicio': '2022-11-10',
            'fecha_fin': '2023-03-20',
            'monto': 65000,
            'consultores_asignados': 3,
            'descripcion': 'Implementación de metodología de mejora continua basada en Lean Six Sigma para optimizar procesos de servicio al cliente.',
            'objetivos': [
                'Reducir tiempo de resolución de incidencias en un 40%',
                'Mejorar la satisfacción del cliente en un 25%',
                'Formar equipo interno de mejora continua'
            ],
            'hitos': [
                {'nombre': 'Diagnóstico inicial', 'fecha': '2022-11-15', 'completado': True},
                {'nombre': 'Capacitación metodológica', 'fecha': '2022-12-10', 'completado': True},
                {'nombre': 'Implementación de mejoras', 'fecha': '2023-01-20', 'completado': True},
                {'nombre': 'Seguimiento y ajustes', 'fecha': '2023-02-25', 'completado': True},
                {'nombre': 'Evaluación de resultados', 'fecha': '2023-03-15', 'completado': True}
            ],
            'riesgos': [
                {'nombre': 'Falta de compromiso del equipo', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Plan de incentivos y reconocimiento'},
                {'nombre': 'Retorno a viejas prácticas', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Seguimiento periódico y refuerzo'}
            ],
            'presupuesto_desglosado': {
                'consultoria': 40000,
                'capacitacion': 15000,
                'herramientas': 7000,
                'otros': 3000
            }
        },
        {
            'id': 6,
            'nombre': 'Desarrollo Plataforma',
            'aliado_id': 1,
            'etapa': 'ejecucion',
            'fecha_inicio': '2023-02-05',
            'fecha_fin': '2023-07-15',
            'monto': 78000,
            'consultores_asignados': 4,
            'descripcion': 'Desarrollo de plataforma e-commerce con integración a sistemas existentes para expansión de canales de venta.',
            'objetivos': [
                'Lanzar nueva plataforma e-commerce en 4 meses',
                'Integrar con sistemas de inventario y CRM existentes',
                'Capacitar al equipo comercial en el uso de la plataforma'
            ],
            'hitos': [
                {'nombre': 'Definición de requerimientos', 'fecha': '2023-02-10', 'completado': True},
                {'nombre': 'Diseño de arquitectura', 'fecha': '2023-03-01', 'completado': True},
                {'nombre': 'Desarrollo de módulos core', 'fecha': '2023-04-15', 'completado': True},
                {'nombre': 'Integraciones y pruebas', 'fecha': '2023-06-01', 'completado': False},
                {'nombre': 'Despliegue y capacitación', 'fecha': '2023-07-10', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Problemas de integración con sistemas legacy', 'impacto': 'Alto', 'probabilidad': 'Alta', 'mitigacion': 'Análisis previo y pruebas de concepto'},
                {'nombre': 'Retrasos en desarrollo', 'impacto': 'Medio', 'probabilidad': 'Media', 'mitigacion': 'Metodología ágil y priorización clara'}
            ],
            'presupuesto_desglosado': {
                'desarrollo': 50000,
                'infraestructura': 10000,
                'licencias': 8000,
                'capacitacion': 10000
            }
        },
        {
            'id': 7,
            'nombre': 'Automatización',
            'aliado_id': 3,
            'etapa': 'ejecucion',
            'fecha_inicio': '2023-01-25',
            'fecha_fin': '2023-05-30',
            'monto': 53000,
            'consultores_asignados': 2,
            'descripcion': 'Implementación de automatización de procesos industriales mediante sistemas IoT y analítica de datos.',
            'objetivos': [
                'Reducir tiempos de producción en un 15%',
                'Implementar monitoreo en tiempo real de procesos críticos',
                'Reducir desperdicios en un 20%'
            ],
            'hitos': [
                {'nombre': 'Diagnóstico y selección de procesos', 'fecha': '2023-01-30', 'completado': True},
                {'nombre': 'Diseño de solución', 'fecha': '2023-02-28', 'completado': True},
                {'nombre': 'Implementación piloto', 'fecha': '2023-03-30', 'completado': True},
                {'nombre': 'Implementación completa', 'fecha': '2023-05-10', 'completado': False},
                {'nombre': 'Evaluación y ajustes', 'fecha': '2023-05-25', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Compatibilidad con equipos existentes', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Estudio previo de compatibilidad'},
                {'nombre': 'Seguridad de los sistemas', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Evaluación de seguridad y plan de mitigación'}
            ],
            'presupuesto_desglosado': {
                'hardware': 20000,
                'software': 15000,
                'consultoria': 15000,
                'capacitacion': 3000
            }
        },
        {
            'id': 8,
            'nombre': 'Programa de Innovación',
            'aliado_id': 6,
            'etapa': 'propuesta',
            'fecha_inicio': '2023-04-01',
            'fecha_fin': '2023-10-30',
            'monto': 68000,
            'consultores_asignados': 3,
            'descripcion': 'Implementación de programa de innovación corporativa con metodologías ágiles y design thinking.',
            'objetivos': [
                'Crear cultura de innovación en la organización',
                'Desarrollar al menos 3 proyectos innovadores',
                'Capacitar a 30 líderes en metodologías de innovación'
            ],
            'hitos': [
                {'nombre': 'Diagnóstico de innovación', 'fecha': '2023-04-10', 'completado': False},
                {'nombre': 'Diseño del programa', 'fecha': '2023-05-15', 'completado': False},
                {'nombre': 'Talleres de capacitación', 'fecha': '2023-06-30', 'completado': False},
                {'nombre': 'Desarrollo de proyectos', 'fecha': '2023-09-15', 'completado': False},
                {'nombre': 'Evaluación y presentación', 'fecha': '2023-10-25', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Falta de compromiso directivo', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Alineación con objetivos estratégicos'},
                {'nombre': 'Resistencia al cambio', 'impacto': 'Medio', 'probabilidad': 'Alta', 'mitigacion': 'Plan de gestión del cambio efectivo'}
            ],
            'presupuesto_desglosado': {
                'consultoria': 40000,
                'talleres': 15000,
                'materiales': 8000,
                'otros': 5000
            }
        },
        {
            'id': 9,
            'nombre': 'Gestión del Conocimiento',
            'aliado_id': 7,
            'etapa': 'planificacion',
            'fecha_inicio': '2023-03-15',
            'fecha_fin': '2023-08-30',
            'monto': 48000,
            'consultores_asignados': 2,
            'descripcion': 'Implementación de plataforma y metodología de gestión del conocimiento para preservar know-how y mejorar capacitación.',
            'objetivos': [
                'Implementar plataforma de gestión del conocimiento',
                'Documentar procesos críticos',
                'Reducir tiempo de onboarding en un 30%'
            ],
            'hitos': [
                {'nombre': 'Diagnóstico inicial', 'fecha': '2023-03-20', 'completado': True},
                {'nombre': 'Selección de plataforma', 'fecha': '2023-04-25', 'completado': False},
                {'nombre': 'Implementación técnica', 'fecha': '2023-06-10', 'completado': False},
                {'nombre': 'Carga de contenidos', 'fecha': '2023-07-20', 'completado': False},
                {'nombre': 'Capacitación y lanzamiento', 'fecha': '2023-08-25', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Falta de participación', 'impacto': 'Alto', 'probabilidad': 'Alta', 'mitigacion': 'Plan de incentivos y reconocimiento'},
                {'nombre': 'Calidad del contenido', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Proceso de revisión y validación'}
            ],
            'presupuesto_desglosado': {
                'plataforma': 20000,
                'consultoria': 18000,
                'capacitacion': 7000,
                'otros': 3000
            }
        },
        {
            'id': 10,
            'nombre': 'Expansión Infraestructura',
            'aliado_id': 8,
            'etapa': 'ejecucion',
            'fecha_inicio': '2023-02-20',
            'fecha_fin': '2023-09-10',
            'monto': 120000,
            'consultores_asignados': 5,
            'descripcion': 'Planificación y supervisión de expansión de infraestructura física y tecnológica para nuevas líneas de producción.',
            'objetivos': [
                'Ampliar capacidad productiva en un 40%',
                'Implementar nuevas tecnologías en líneas de producción',
                'Optimizar flujos logísticos internos'
            ],
            'hitos': [
                {'nombre': 'Planificación detallada', 'fecha': '2023-02-25', 'completado': True},
                {'nombre': 'Diseño y aprobación', 'fecha': '2023-03-30', 'completado': True},
                {'nombre': 'Contratación proveedores', 'fecha': '2023-04-15', 'completado': True},
                {'nombre': 'Implementación física', 'fecha': '2023-07-20', 'completado': False},
                {'nombre': 'Pruebas y puesta en marcha', 'fecha': '2023-09-05', 'completado': False}
            ],
            'riesgos': [
                {'nombre': 'Retrasos en entregas', 'impacto': 'Alto', 'probabilidad': 'Alta', 'mitigacion': 'Contratos con penalizaciones y múltiples proveedores'},
                {'nombre': 'Sobrecostos', 'impacto': 'Alto', 'probabilidad': 'Media', 'mitigacion': 'Reserva de contingencia y supervisión estricta'}
            ],
            'presupuesto_desglosado': {
                'infraestructura': 80000,
                'equipamiento': 25000,
                'consultoria': 10000,
                'otros': 5000
            }
        }
    ]

    # ETAPA 3: EJECUCIÓN - DATOS DE CONSULTORES Y EQUIPO
    CONSULTORES_EXTENDIDOS = [
        {
            'id': 1,
            'nombre': 'Ana Martínez',
            'especialidad': 'Tecnología',
            'proyectos_asignados': [1, 6],
            'disponibilidad': 30,
            'email': 'ana.martinez@consultores.com',
            'telefono': '+52 55 1234 5678',
            'nivel': 'Senior',
            'fecha_incorporacion': '2022-01-15',
            'habilidades': ['Cloud Computing', 'DevOps', 'Arquitectura de Software', 'Gestión de Proyectos'],
            'certificaciones': ['AWS Certified Solutions Architect', 'Scrum Master'],
            'evaluaciones': [
                {'fecha': '2022-06-15', 'calificacion': 4.8, 'comentarios': 'Excelente desempeño en proyectos de transformación digital'},
                {'fecha': '2022-12-15', 'calificacion': 4.7, 'comentarios': 'Gran capacidad de resolución de problemas complejos'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés', 'Francés'],
            'tarifa_hora': 75
        },
        {
            'id': 2,
            'nombre': 'Carlos Ruiz',
            'especialidad': 'Finanzas',
            'proyectos_asignados': [2],
            'disponibilidad': 70,
            'email': 'carlos.ruiz@consultores.com',
            'telefono': '+52 55 8765 4321',
            'nivel': 'Senior',
            'fecha_incorporacion': '2022-03-10',
            'habilidades': ['Análisis Financiero', 'Valoración de Empresas', 'Gestión de Riesgos', 'Planificación Estratégica'],
            'certificaciones': ['CFA', 'MBA en Finanzas'],
            'evaluaciones': [
                {'fecha': '2022-09-10', 'calificacion': 4.6, 'comentarios': 'Sólidos conocimientos financieros y gran capacidad analítica'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés'],
            'tarifa_hora': 70
        },
        {
            'id': 3,
            'nombre': 'Elena Gómez',
            'especialidad': 'Manufactura',
            'proyectos_asignados': [3, 7],
            'disponibilidad': 20,
            'email': 'elena.gomez@consultores.com',
            'telefono': '+52 81 2345 6789',
            'nivel': 'Senior',
            'fecha_incorporacion': '2021-11-05',
            'habilidades': ['Lean Manufacturing', 'Six Sigma', 'Automatización Industrial', 'Gestión de Cadena de Suministro'],
            'certificaciones': ['Six Sigma Black Belt', 'PMP'],
            'evaluaciones': [
                {'fecha': '2022-05-05', 'calificacion': 4.9, 'comentarios': 'Excelente implementación de metodologías Lean'},
                {'fecha': '2022-11-05', 'calificacion': 4.8, 'comentarios': 'Gran capacidad para optimizar procesos productivos'}
            ],
            'ubicacion': 'Monterrey',
            'idiomas': ['Español', 'Inglés', 'Alemán'],
            'tarifa_hora': 72
        },
        {
            'id': 4,
            'nombre': 'Javier Pérez',
            'especialidad': 'Marketing',
            'proyectos_asignados': [4],
            'disponibilidad': 60,
            'email': 'javier.perez@consultores.com',
            'telefono': '+52 55 9876 5432',
            'nivel': 'Semi-Senior',
            'fecha_incorporacion': '2022-05-20',
            'habilidades': ['Marketing Digital', 'SEO/SEM', 'Análisis de Datos', 'Estrategia de Contenidos'],
            'certificaciones': ['Google Analytics', 'HubSpot Inbound Marketing'],
            'evaluaciones': [
                {'fecha': '2022-11-20', 'calificacion': 4.5, 'comentarios': 'Excelente conocimiento de herramientas de marketing digital'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés'],
            'tarifa_hora': 65
        },
        {
            'id': 5,
            'nombre': 'María López',
            'especialidad': 'Operaciones',
            'proyectos_asignados': [5],
            'disponibilidad': 80,
            'email': 'maria.lopez@consultores.com',
            'telefono': '+52 33 1234 5678',
            'nivel': 'Senior',
            'fecha_incorporacion': '2021-08-15',
            'habilidades': ['Optimización de Procesos', 'Gestión de Proyectos', 'Análisis de Datos', 'Mejora Continua'],
            'certificaciones': ['PMP', 'ITIL', 'Lean Six Sigma Green Belt'],
            'evaluaciones': [
                {'fecha': '2022-02-15', 'calificacion': 4.7, 'comentarios': 'Gran capacidad para identificar oportunidades de mejora'},
                {'fecha': '2022-08-15', 'calificacion': 4.8, 'comentarios': 'Excelente liderazgo en proyectos de optimización'}
            ],
            'ubicacion': 'Guadalajara',
            'idiomas': ['Español', 'Inglés', 'Portugués'],
            'tarifa_hora': 70
        },
        {
            'id': 6,
            'nombre': 'Roberto Sánchez',
            'especialidad': 'Tecnología',
            'proyectos_asignados': [1, 6],
            'disponibilidad': 40,
            'email': 'roberto.sanchez@consultores.com',
            'telefono': '+52 55 2345 6789',
            'nivel': 'Senior',
            'fecha_incorporacion': '2021-10-10',
            'habilidades': ['Desarrollo de Software', 'Arquitectura Cloud', 'DevOps', 'Seguridad Informática'],
            'certificaciones': ['Azure Solutions Architect', 'CISSP'],
            'evaluaciones': [
                {'fecha': '2022-04-10', 'calificacion': 4.6, 'comentarios': 'Excelente conocimiento técnico y capacidad de implementación'},
                {'fecha': '2022-10-10', 'calificacion': 4.7, 'comentarios': 'Gran compromiso con los objetivos de los proyectos'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés'],
            'tarifa_hora': 73
        },
        {
            'id': 7,
            'nombre': 'Sofía Torres',
            'especialidad': 'Estrategia',
            'proyectos_asignados': [2, 4],
            'disponibilidad': 50,
            'email': 'sofia.torres@consultores.com',
            'telefono': '+52 55 8765 4321',
            'nivel': 'Senior',
            'fecha_incorporacion': '2022-02-01',
            'habilidades': ['Planificación Estratégica', 'Innovación', 'Análisis de Mercado', 'Transformación Organizacional'],
            'certificaciones': ['MBA', 'Design Thinking Certified'],
            'evaluaciones': [
                {'fecha': '2022-08-01', 'calificacion': 4.8, 'comentarios': 'Visión estratégica sobresaliente y gran capacidad analítica'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés', 'Italiano'],
            'tarifa_hora': 75
        },
        {
            'id': 8,
            'nombre': 'Daniel Ramírez',
            'especialidad': 'Desarrollo de Software',
            'proyectos_asignados': [6, 8],
            'disponibilidad': 35,
            'email': 'daniel.ramirez@consultores.com',
            'telefono': '+52 55 1234 5678',
            'nivel': 'Semi-Senior',
            'fecha_incorporacion': '2022-04-15',
            'habilidades': ['Desarrollo Full Stack', 'React', 'Node.js', 'Python', 'APIs'],
            'certificaciones': ['AWS Developer Associate', 'MongoDB Certified Developer'],
            'evaluaciones': [
                {'fecha': '2022-10-15', 'calificacion': 4.5, 'comentarios': 'Excelente capacidad técnica y rápido aprendizaje'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés'],
            'tarifa_hora': 65
        },
        {
            'id': 9,
            'nombre': 'Laura Herrera',
            'especialidad': 'UX/UI',
            'proyectos_asignados': [6, 9],
            'disponibilidad': 45,
            'email': 'laura.herrera@consultores.com',
            'telefono': '+52 55 9876 5432',
            'nivel': 'Senior',
            'fecha_incorporacion': '2022-01-20',
            'habilidades': ['Diseño UX', 'Investigación de Usuarios', 'Prototipado', 'Diseño de Interacción'],
            'certificaciones': ['Certified UX Professional', 'Adobe Certified Expert'],
            'evaluaciones': [
                {'fecha': '2022-07-20', 'calificacion': 4.7, 'comentarios': 'Gran capacidad para transformar requisitos en experiencias de usuario'},
                {'fecha': '2023-01-20', 'calificacion': 4.8, 'comentarios': 'Excelente colaboración con equipos técnicos'}
            ],
            'ubicacion': 'Ciudad de México',
            'idiomas': ['Español', 'Inglés', 'Francés'],
            'tarifa_hora': 70
        },
        {
            'id': 10,
            'nombre': 'Jorge Mendoza',
            'especialidad': 'Ingeniería Civil',
            'proyectos_asignados': [10],
            'disponibilidad': 30,
            'email': 'jorge.mendoza@consultores.com',
            'telefono': '+52 81 8765 4321',
            'nivel': 'Senior',
            'fecha_incorporacion': '2021-09-01',
            'habilidades': ['Diseño Estructural', 'Gestión de Proyectos de Construcción', 'BIM', 'Análisis de Costos'],
            'certificaciones': ['PMP', 'Certified BIM Professional'],
            'evaluaciones': [
                {'fecha': '2022-03-01', 'calificacion': 4.6, 'comentarios': 'Excelente capacidad técnica y de resolución de problemas'},
                {'fecha': '2022-09-01', 'calificacion': 4.7, 'comentarios': 'Gran habilidad para gestionar proyectos complejos'}
            ],
            'ubicacion': 'Monterrey',
            'idiomas': ['Español', 'Inglés'],
            'tarifa_hora': 72
        }
    ]

    # ETAPA 4: CIERRE - DATOS DE EVALUACIÓN Y RESULTADOS
    RESULTADOS_PROYECTOS = [
        {
            'proyecto_id': 4,  # Estrategia de Mercado (ya cerrado)
            'aliado_id': 4,
            'metricas_clave': [
                {'nombre': 'Aumento de posicionamiento', 'objetivo': '30%', 'logrado': '35%', 'estado': 'Superado'},
                {'nombre': 'Incremento de tráfico web', 'objetivo': '50%', 'logrado': '48%', 'estado': 'Casi logrado'},
                {'nombre': 'Aumento de conversiones', 'objetivo': '25%', 'logrado': '27%', 'estado': 'Superado'}
            ],
            'satisfaccion_cliente': 4.8,
            'lecciones_aprendidas': [
                'La segmentación de audiencia fue clave para el éxito de las campañas',
                'El análisis constante permitió ajustar estrategias a tiempo',
                'Involucrar al equipo del cliente desde el inicio mejoró la adopción'
            ],
            'desafios_enfrentados': [
                'Cambios en algoritmos de redes sociales',
                'Resistencia inicial a nuevas estrategias de marketing',
                'Tiempos ajustados para implementación completa'
            ],
            'recomendaciones_futuras': [
                'Mantener ciclos cortos de evaluación y ajuste',
                'Invertir en capacitación continua del equipo interno',
                'Explorar nuevos canales emergentes'
            ],
            'roi_estimado': '320%',
            'testimonios': [
                {
                    'autor': 'Laura Ramírez, Dir. Marketing',
                    'texto': 'La colaboración con el equipo consultor transformó completamente nuestra estrategia digital, con resultados que superaron nuestras expectativas.'
                },
                {
                    'autor': 'Miguel Fernández, CEO',
                    'texto': 'Vimos un impacto directo en nuestras métricas de negocio. La metodología fue clara y los resultados tangibles.'
                }
            ]
        },
        {
            'proyecto_id': 5,  # Mejora Continua (post-evaluación)
            'aliado_id': 5,
            'metricas_clave': [
                {'nombre': 'Reducción tiempo resolución', 'objetivo': '40%', 'logrado': '45%', 'estado': 'Superado'},
                {'nombre': 'Mejora satisfacción cliente', 'objetivo': '25%', 'logrado': '30%', 'estado': 'Superado'},
                {'nombre': 'Formación equipo interno', 'objetivo': '100%', 'logrado': '100%', 'estado': 'Logrado'}
            ],
            'satisfaccion_cliente': 4.9,
            'lecciones_aprendidas': [
                'El compromiso de la alta dirección fue fundamental',
                'La medición constante permitió correcciones tempranas',
                'La capacitación práctica tuvo mejor recepción que la teórica'
            ],
            'desafios_enfrentados': [
                'Resistencia inicial al cambio',
                'Dificultad para mantener el impulso inicial',
                'Compatibilidad con sistemas existentes'
            ],
            'recomendaciones_futuras': [
                'Establecer un programa de reconocimiento para mantener el impulso',
                'Implementar revisiones trimestrales de procesos',
                'Continuar con la capacitación avanzada del equipo interno'
            ],
            'roi_estimado': '280%',
            'testimonios': [
                {
                    'autor': 'Carlos Mendoza, Dir. Operaciones',
                    'texto': 'La metodología de mejora continua ha cambiado nuestra cultura organizacional. Vemos mejoras constantes y medibles.'
                },
                {
                    'autor': 'Ana Gutiérrez, Líder de Servicio',
                    'texto': 'Nunca habíamos logrado reducir los tiempos de respuesta de manera tan significativa. Los clientes lo notan y lo agradecen.'
                }
            ]
        }
    ]

    # ETAPA 5: RETENCIÓN DE TALENTO - MÉTRICAS DE COMUNIDAD Y DESARROLLO
    DESARROLLO_PROFESIONAL = {
        'programas_activos': [
            {
                'nombre': 'Certificación Avanzada en Cloud Computing',
                'participantes': 3,
                'estado': 'En curso',
                'inicio': '2023-01-15',
                'fin': '2023-06-30',
                'completado': '60%'
            },
            {
                'nombre': 'Programa de Liderazgo Consultivo',
                'participantes': 5,
                'estado': 'En curso',
                'inicio': '2023-02-10',
                'fin': '2023-05-15',
                'completado': '75%'
            },
            {
                'nombre': 'Especialización en Inteligencia Artificial para Negocios',
                'participantes': 4,
                'estado': 'Planificado',
                'inicio': '2023-05-01',
                'fin': '2023-09-30',
                'completado': '0%'
            }
        ],
        'mentoria': [
            {
                'mentor': 'Ana Martínez',
                'mentee': 'Daniel Ramírez',
                'area': 'Arquitectura Cloud',
                'inicio': '2023-01-01',
                'objetivos': ['Desarrollo de arquitecturas serverless', 'Optimización de costos en cloud']
            },
            {
                'mentor': 'Roberto Sánchez',
                'mentee': 'Jorge Mendoza',
                'area': 'Gestión de Proyectos Tecnológicos',
                'inicio': '2023-02-15',
                'objetivos': ['Metodologías ágiles en proyectos complejos', 'Gestión de stakeholders']
            }
        ],
        'recursos_aprendizaje': {
            'biblioteca_digital': 320,
            'cursos_online': 45,
            'webinars_mensuales': 4,
            'comunidades_practica': 6
        },
        'metricas_desarrollo': {
            'promedio_horas_formacion': 48,
            'tasa_certificacion': '72%',
            'indice_aplicacion_conocimientos': '78%',
            'satisfaccion_programas': 4.7
        }
    }

    METRICAS_COMUNIDAD = {
        'indice_satisfaccion': '92%',
        'tasa_retencion': '88%',
        'nps_consultores': 67,
        'engagement': '85%',
        'eventos_realizados': [
            {
                'nombre': 'Tech Conference 2023',
                'fecha': '2023-03-15',
                'participantes': 78,
                'satisfaccion': 4.8,
                'temas': ['Cloud Native', 'DevOps', 'IA', 'Blockchain']
            },
            {
                'nombre': 'Innovation Workshop',
                'fecha': '2023-02-22',
                'participantes': 35,
                'satisfaccion': 4.7,
                'temas': ['Design Thinking', 'Metodologías Ágiles', 'Innovación Disruptiva']
            },
            {
                'nombre': 'Estrategia Post-Pandemia',
                'fecha': '2023-01-18',
                'participantes': 42,
                'satisfaccion': 4.6,
                'temas': ['Transformación Digital', 'Nuevos Modelos de Negocio', 'Resiliencia Organizacional']
            }
        ],
        'programa_reconocimiento': {
            'consultores_reconocidos': 12,
            'categorias': ['Excelencia Técnica', 'Innovación', 'Satisfacción del Cliente', 'Mentoría'],
            'impacto_retencion': '+15%'
        },
        'bienestar': {
            'programa_beneficios': ['Horario Flexible', 'Teletrabajo', 'Días Personales', 'Seguro Médico Premium'],
            'balance_vida_trabajo': '87%',
            'participacion_actividades': '75%'
        }
    }

    # DATOS ADICIONALES PARA VISUALIZACIONES DE DASHBOARD
    DATOS_DASHBOARD_EXTENDIDOS = {
        'ubicaciones_operaciones': [
            {'nombre': 'Sede Central CDMX', 'lat': 19.4326, 'lng': -99.1332, 'proyectos': 5, 'consultores': 8},
            {'nombre': 'Oficina Monterrey', 'lat': 25.6866, 'lng': -100.3161, 'proyectos': 3, 'consultores': 5},
            {'nombre': 'Oficina Guadalajara', 'lat': 20.6597, 'lng': -103.3496, 'proyectos': 2, 'consultores': 4},
            {'nombre': 'Oficina Mérida', 'lat': 20.9674, 'lng': -89.5926, 'proyectos': 2, 'consultores': 3},
            {'nombre': 'Oficina Querétaro', 'lat': 20.5888, 'lng': -100.3899, 'proyectos': 1, 'consultores': 2},
            {'nombre': 'Oficina Tijuana', 'lat': 32.5027, 'lng': -117.0037, 'proyectos': 2, 'consultores': 3}
        ],
        'ventas_por_region': [
            {'region': 'Norte', 'ventas': 240000},
            {'region': 'Centro', 'ventas': 190000},
            {'region': 'Este', 'ventas': 160000},
            {'region': 'Sur', 'ventas': 85000},
            {'region': 'Oeste', 'ventas': 102000}
        ],
        'proyectos_por_etapa': [
            {'etapa': 'Propuesta', 'cantidad': 2, 'valor': 163000},
            {'etapa': 'Planificación', 'cantidad': 2, 'valor': 120000},
            {'etapa': 'Ejecución', 'cantidad': 4, 'valor': 331000},
            {'etapa': 'Cierre', 'cantidad': 1, 'valor': 45000},
            {'etapa': 'Post-evaluación', 'cantidad': 1, 'valor': 65000}
        ],
        'evaluaciones_consultores': {
            'promedio_general': 4.7,
            'dimensiones': [
                {'dimension': 'Conocimiento Técnico', 'calificacion': 4.8},
                {'dimension': 'Resolución de Problemas', 'calificacion': 4.7},
                {'dimension': 'Comunicación', 'calificacion': 4.6},
                {'dimension': 'Trabajo en Equipo', 'calificacion': 4.9},
                {'dimension': 'Entrega de Resultados', 'calificacion': 4.6}
            ],
            'evolucion_trimestral': [
                {'trimestre': 'Q1 2022', 'promedio': 4.4},
                {'trimestre': 'Q2 2022', 'promedio': 4.5},
                {'trimestre': 'Q3 2022', 'promedio': 4.6},
                {'trimestre': 'Q4 2022', 'promedio': 4.6},
                {'trimestre': 'Q1 2023', 'promedio': 4.7}
            ],
            'top_consultores': [
                {'nombre': 'Elena Gómez', 'calificacion': 4.9, 'proyectos': 2},
                {'nombre': 'María López', 'calificacion': 4.8, 'proyectos': 1},
                {'nombre': 'Ana Martínez', 'calificacion': 4.8, 'proyectos': 2},
                {'nombre': 'Sofía Torres', 'calificacion': 4.8, 'proyectos': 2},
                {'nombre': 'Roberto Sánchez', 'calificacion': 4.7, 'proyectos': 2}
            ],
            'factores_satisfaccion': [
                {'factor': 'Expertise técnico', 'impacto': 'Alto', 'valor': 85},
                {'factor': 'Comunicación', 'impacto': 'Alto', 'valor': 82},
                {'factor': 'Tiempo de respuesta', 'impacto': 'Medio', 'valor': 78},
                {'factor': 'Adaptabilidad', 'impacto': 'Alto', 'valor': 81},
                {'factor': 'Transferencia de conocimiento', 'impacto': 'Medio', 'valor': 75}
            ]
        },
        'tendencias_industria': [
            {'trimestre': 'Q1 2022', 'tecnologia': 100000, 'finanzas': 85000, 'manufactura': 90000, 'servicios': 75000},
            {'trimestre': 'Q2 2022', 'tecnologia': 120000, 'finanzas': 92000, 'manufactura': 95000, 'servicios': 82000},
            {'trimestre': 'Q3 2022', 'tecnologia': 115000, 'finanzas': 88000, 'manufactura': 100000, 'servicios': 87000},
            {'trimestre': 'Q4 2022', 'tecnologia': 130000, 'finanzas': 95000, 'manufactura': 105000, 'servicios': 90000},
            {'trimestre': 'Q1 2023', 'tecnologia': 140000, 'finanzas': 98000, 'manufactura': 110000, 'servicios': 95000}
        ],
        'pipeline_ventas': {
            'oportunidades_totales': 25,
            'valor_total': 1500000,
            'conversion_promedio': '22%',
            'etapas': [
                {'etapa': 'Contacto Inicial', 'oportunidades': 10, 'valor': 600000},
                {'etapa': 'Calificación', 'oportunidades': 6, 'valor': 350000},
                {'etapa': 'Propuesta', 'oportunidades': 5, 'valor': 300000},
                {'etapa': 'Negociación', 'oportunidades': 3, 'valor': 180000},
                {'etapa': 'Cierre', 'oportunidades': 1, 'valor': 70000}
            ],
            'tiempo_ciclo_promedio': 75  # días
        },
        'matriz_competencias': [
            {'competencia': 'Cloud Computing', 'nivel_actual': 4.5, 'demanda_mercado': 4.8, 'gap': 0.3, 'prioridad': 'Alta'},
            {'competencia': 'Data Science', 'nivel_actual': 3.8, 'demanda_mercado': 4.7, 'gap': 0.9, 'prioridad': 'Alta'},
            {'competencia': 'Cybersecurity', 'nivel_actual': 4.2, 'demanda_mercado': 4.6, 'gap': 0.4, 'prioridad': 'Media'},
            {'competencia': 'Agile Methods', 'nivel_actual': 4.6, 'demanda_mercado': 4.4, 'gap': -0.2, 'prioridad': 'Baja'},
            {'competencia': 'DevOps', 'nivel_actual': 4.0, 'demanda_mercado': 4.5, 'gap': 0.5, 'prioridad': 'Media'},
            {'competencia': 'Blockchain', 'nivel_actual': 3.2, 'demanda_mercado': 3.8, 'gap': 0.6, 'prioridad': 'Media'},
            {'competencia': 'UX/UI', 'nivel_actual': 4.3, 'demanda_mercado': 4.4, 'gap': 0.1, 'prioridad': 'Baja'}
        ]
    }





    