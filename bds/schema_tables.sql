
-- Crear schema si no existe
CREATE SCHEMA IF NOT EXISTS neuron;

-- Crear tablas
CREATE TABLE IF NOT EXISTS neuron.usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    id_organizacion INT,
    id_sede INT,
    correo VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255),
    id_rol INT,
    estado INT,
    ultimo_login DATETIME
);

CREATE TABLE IF NOT EXISTS neuron.organizaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    id_industria INT,
    fecha_registro DATE,
    estado INT,
    contacto_principal VARCHAR(255),
    tamaño VARCHAR(255),
    empleados INT
);

CREATE TABLE IF NOT EXISTS neuron.sedes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_organizacion INT,
    nombre_sede VARCHAR(255),
    subregion_id INT,
    direccion VARCHAR(255),
    ciudad VARCHAR(255),
    codigo_postal VARCHAR(255),
    pais VARCHAR(255),
    estado INT
);

CREATE TABLE IF NOT EXISTS neuron.subregiones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    codigo VARCHAR(255),
    descripcion TEXT,
    id_region INT,
    activo BOOLEAN
);

CREATE TABLE IF NOT EXISTS neuron.regiones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    codigo VARCHAR(255),
    descripcion TEXT,
    activo BOOLEAN
);

CREATE TABLE IF NOT EXISTS neuron.colaboradores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_organizacion INT,
    cargo VARCHAR(255),
    rol_laboral VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS neuron.industrias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    grupo_general VARCHAR(255),
    sector VARCHAR(255),
    nota TEXT
);

CREATE TABLE IF NOT EXISTS neuron.portafolio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    categoria VARCHAR(255),
    familia VARCHAR(255),
    descripcion TEXT,
    tipo VARCHAR(255),
    estado INT,
    fecha_creacion DATETIME,
    fecha_actualizacion DATETIME
);

CREATE TABLE IF NOT EXISTS neuron.consultores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    especialidad VARCHAR(255),
    disponibilidad VARCHAR(255),
    nivel_segun_usuario FLOAT,
    nivel_segun_gestor FLOAT,
    fecha_incorporacion DATE,
    direccion VARCHAR(255),
    ciudad VARCHAR(255),
    codigo_postal VARCHAR(255),
    pais VARCHAR(255),
    tarifa_hora FLOAT,
    resumen_perfil TEXT,
    celular VARCHAR(255),
    linkedin VARCHAR(255)
);

-- Tabla comunidades
CREATE TABLE IF NOT EXISTS neuron.comunidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    tipo VARCHAR(100)
);

-- Tabla personas_cliente
CREATE TABLE IF NOT EXISTS neuron.personas_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT,
    id_usuario INT,
    rol_en_cliente VARCHAR(255),
    fecha_asignacion DATE
);

-- Tabla miembros_comunidad
CREATE TABLE IF NOT EXISTS neuron.miembros_comunidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_comunidad INT,
    id_usuario INT,
    rol_en_comunidad VARCHAR(255),
    fecha_union DATE
);

-- Tabla comunidad_aliado
CREATE TABLE IF NOT EXISTS neuron.comunidad_aliado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT,
    id_comunidad INT,
    fecha_asignacion DATE,
    observaciones TEXT
);

-- Tabla caso_uso
CREATE TABLE IF NOT EXISTS neuron.caso_uso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aliado INT,
    id_usuario INT,
    id_cuenta INT,
    caso_uso VARCHAR(255),
    descripcion TEXT,
    impacto VARCHAR(255),
    puntuacion_impacto INT,
    puntuacion_tecnica INT,
    tags VARCHAR(255),
    estado INT,
    id_producto INT,
    fecha_inicio DATE,
    fecha_cierre DATE,
    monto_venta FLOAT,
    costos_proyecto FLOAT,
    margen_estimado_porcentaje FLOAT,
    margen_estimado_bruto FLOAT,
    feedback TEXT
);

-- Tabla cuentas
CREATE TABLE IF NOT EXISTS neuron.cuentas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_organizacion INT,
    nombre VARCHAR(255),
    industria INT,
    subregion INT,
    fecha_alta DATE,
    fecha_modificacion DATE,
    fecha_baja DATE,
    codigo VARCHAR(50),
    id_segmentacion INT,
    estado INT
);

-- Tabla segmentacion
CREATE TABLE IF NOT EXISTS neuron.segmentacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clasificacion VARCHAR(100),
    descripcion TEXT
);

-- Tabla roles
CREATE TABLE IF NOT EXISTS neuron.roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255)
);

-- Tabla experiencia_laboral
CREATE TABLE IF NOT EXISTS neuron.experiencia_laboral (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    cargo VARCHAR(255),
    empresa VARCHAR(255),
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    ubicacion VARCHAR(255),
    tipo_empleo VARCHAR(255),
    sector VARCHAR(255),
    logros TEXT
);

-- Tabla educacion
CREATE TABLE IF NOT EXISTS neuron.educacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    institucion VARCHAR(255),
    titulo VARCHAR(255),
    area_estudio VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion TEXT
);

-- Tabla certificaciones
CREATE TABLE IF NOT EXISTS neuron.certificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    nombre VARCHAR(255),
    entidad VARCHAR(255),
    fecha_obtencion DATE,
    fecha_vencimiento DATE,
    url_certificado VARCHAR(255),
    id_credencial VARCHAR(255),
    descripcion TEXT
);

-- Tabla proyectos_destacados
CREATE TABLE IF NOT EXISTS neuron.proyectos_destacados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    nombre VARCHAR(255),
    descripcion TEXT,
    tecnologias_usadas VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    link_portafolio VARCHAR(255)
);

-- Tabla estados
CREATE TABLE IF NOT EXISTS neuron.estados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    entidad VARCHAR(255)
);

-- Tabla estimaciones
CREATE TABLE IF NOT EXISTS neuron.estimaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_caso_uso INT,
    nombre_caso_uso VARCHAR(255)
);

-- Tabla entregables
CREATE TABLE IF NOT EXISTS neuron.entregables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_estimacion INT,
    nombre VARCHAR(255),
    descripcion TEXT,
    criterios_aceptacion TEXT,
    estado INT,
    fecha_entrega_estimada DATE,
    fecha_entregado DATE,
    version VARCHAR(50),
    fecha_creacion DATETIME,
    fecha_actualizacion DATETIME,
    actualizado_por INT
);

-- Tabla actividades
CREATE TABLE IF NOT EXISTS neuron.actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_entregable INT,
    nombre VARCHAR(255),
    descripcion TEXT,
    estado INT,
    fecha_inicio_estimada DATE,
    fecha_fin_estimada DATE,
    fecha_inicio_real DATE,
    fecha_fin_real DATE,
    id_usuario_responsable INT,
    prioridad VARCHAR(50),
    orden INT,
    observaciones TEXT,
    fecha_creacion DATETIME,
    fecha_actualizacion DATETIME,
    actualizado_por INT
);

-- Tabla tareas
CREATE TABLE IF NOT EXISTS neuron.tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_actividad INT,
    nombre VARCHAR(255),
    descripcion TEXT,
    estado INT,
    id_usuario_responsable INT,
    duracion_optimista FLOAT,
    duracion_mas_probable FLOAT,
    duracion_pesimista FLOAT,
    duracion_estimada FLOAT,
    fecha_inicio DATE,
    fecha_fin DATE,
    es_critica BOOLEAN,
    orden INT,
    observaciones TEXT,
    fecha_creacion DATETIME,
    fecha_actualizacion DATETIME,
    actualizado_por INT
);

-- Tabla costos_recursos
CREATE TABLE IF NOT EXISTS neuron.costos_recursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_estimacion INT,
    tipo VARCHAR(255),
    concepto VARCHAR(255),
    periodicidad VARCHAR(255),
    divisa VARCHAR(50),
    cantidad FLOAT,
    costo FLOAT
);

-- Tabla costos_freelance
CREATE TABLE IF NOT EXISTS neuron.costos_freelance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_estimacion INT,
    especialidad VARCHAR(255),
    nivel VARCHAR(255),
    costo_hora FLOAT,
    actividad VARCHAR(255),
    horas FLOAT
);

-- Llaves foráneas para esquema neuron

ALTER TABLE neuron.usuarios ADD CONSTRAINT fk_usuarios_organizacion FOREIGN KEY (id_organizacion) REFERENCES neuron.organizaciones(id);
ALTER TABLE neuron.usuarios ADD CONSTRAINT fk_usuarios_sede FOREIGN KEY (id_sede) REFERENCES neuron.sedes(id);
ALTER TABLE neuron.usuarios ADD CONSTRAINT fk_usuarios_rol FOREIGN KEY (id_rol) REFERENCES neuron.roles(id);
ALTER TABLE neuron.usuarios ADD CONSTRAINT fk_usuarios_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);

ALTER TABLE neuron.organizaciones ADD CONSTRAINT fk_organizaciones_industria FOREIGN KEY (id_industria) REFERENCES neuron.industrias(id);
ALTER TABLE neuron.organizaciones ADD CONSTRAINT fk_organizaciones_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);

ALTER TABLE neuron.sedes ADD CONSTRAINT fk_sedes_organizacion FOREIGN KEY (id_organizacion) REFERENCES neuron.organizaciones(id);
ALTER TABLE neuron.sedes ADD CONSTRAINT fk_sedes_subregion FOREIGN KEY (subregion_id) REFERENCES neuron.subregiones(id);
ALTER TABLE neuron.sedes ADD CONSTRAINT fk_sedes_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);

ALTER TABLE neuron.subregiones ADD CONSTRAINT fk_subregiones_region FOREIGN KEY (id_region) REFERENCES neuron.regiones(id);

ALTER TABLE neuron.colaboradores ADD CONSTRAINT fk_colaboradores_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.colaboradores ADD CONSTRAINT fk_colaboradores_organizacion FOREIGN KEY (id_organizacion) REFERENCES neuron.organizaciones(id);

ALTER TABLE neuron.portafolio ADD CONSTRAINT fk_portafolio_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);

ALTER TABLE neuron.consultores ADD CONSTRAINT fk_consultores_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.personas_cliente ADD CONSTRAINT fk_personas_cliente_sede FOREIGN KEY (id_sede) REFERENCES neuron.sedes(id);
ALTER TABLE neuron.personas_cliente ADD CONSTRAINT fk_personas_cliente_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.miembros_comunidad ADD CONSTRAINT fk_miembros_comunidad_comunidad FOREIGN KEY (id_comunidad) REFERENCES neuron.comunidades(id);
ALTER TABLE neuron.miembros_comunidad ADD CONSTRAINT fk_miembros_comunidad_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.comunidad_aliado ADD CONSTRAINT fk_comunidad_aliado_sede FOREIGN KEY (id_sede) REFERENCES neuron.sedes(id);
ALTER TABLE neuron.comunidad_aliado ADD CONSTRAINT fk_comunidad_aliado_comunidad FOREIGN KEY (id_comunidad) REFERENCES neuron.comunidades(id);

ALTER TABLE neuron.caso_uso ADD CONSTRAINT fk_caso_uso_aliado FOREIGN KEY (id_aliado) REFERENCES neuron.sedes(id);
ALTER TABLE neuron.caso_uso ADD CONSTRAINT fk_caso_uso_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.caso_uso ADD CONSTRAINT fk_caso_uso_cuenta FOREIGN KEY (id_cuenta) REFERENCES neuron.cuentas(id);
ALTER TABLE neuron.caso_uso ADD CONSTRAINT fk_caso_uso_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);
ALTER TABLE neuron.caso_uso ADD CONSTRAINT fk_caso_uso_producto FOREIGN KEY (id_producto) REFERENCES neuron.portafolio(id);

ALTER TABLE neuron.cuentas ADD CONSTRAINT fk_cuentas_organizacion FOREIGN KEY (id_organizacion) REFERENCES neuron.organizaciones(id);
ALTER TABLE neuron.cuentas ADD CONSTRAINT fk_cuentas_industria FOREIGN KEY (industria) REFERENCES neuron.industrias(id);
ALTER TABLE neuron.cuentas ADD CONSTRAINT fk_cuentas_subregion FOREIGN KEY (subregion) REFERENCES neuron.subregiones(id);
ALTER TABLE neuron.cuentas ADD CONSTRAINT fk_cuentas_segmentacion FOREIGN KEY (id_segmentacion) REFERENCES neuron.segmentacion(id);
ALTER TABLE neuron.cuentas ADD CONSTRAINT fk_cuentas_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);

ALTER TABLE neuron.experiencia_laboral ADD CONSTRAINT fk_experiencia_laboral_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.educacion ADD CONSTRAINT fk_educacion_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.certificaciones ADD CONSTRAINT fk_certificaciones_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.proyectos_destacados ADD CONSTRAINT fk_proyectos_destacados_usuario FOREIGN KEY (id_usuario) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.entregables ADD CONSTRAINT fk_entregables_estimacion FOREIGN KEY (id_estimacion) REFERENCES neuron.estimaciones(id);
ALTER TABLE neuron.entregables ADD CONSTRAINT fk_entregables_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);
ALTER TABLE neuron.entregables ADD CONSTRAINT fk_entregables_actualizado_por FOREIGN KEY (actualizado_por) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.estimaciones ADD CONSTRAINT fk_estimaciones_caso_uso FOREIGN KEY (id_caso_uso) REFERENCES neuron.caso_uso(id);

ALTER TABLE neuron.actividades ADD CONSTRAINT fk_actividades_entregable FOREIGN KEY (id_entregable) REFERENCES neuron.entregables(id);
ALTER TABLE neuron.actividades ADD CONSTRAINT fk_actividades_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);
ALTER TABLE neuron.actividades ADD CONSTRAINT fk_actividades_usuario_responsable FOREIGN KEY (id_usuario_responsable) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.actividades ADD CONSTRAINT fk_actividades_actualizado_por FOREIGN KEY (actualizado_por) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.tareas ADD CONSTRAINT fk_tareas_actividad FOREIGN KEY (id_actividad) REFERENCES neuron.actividades(id);
ALTER TABLE neuron.tareas ADD CONSTRAINT fk_tareas_estado FOREIGN KEY (estado) REFERENCES neuron.estados(id);
ALTER TABLE neuron.tareas ADD CONSTRAINT fk_tareas_usuario_responsable FOREIGN KEY (id_usuario_responsable) REFERENCES neuron.usuarios(id);
ALTER TABLE neuron.tareas ADD CONSTRAINT fk_tareas_actualizado_por FOREIGN KEY (actualizado_por) REFERENCES neuron.usuarios(id);

ALTER TABLE neuron.costos_recursos ADD CONSTRAINT fk_costos_recursos_estimacion FOREIGN KEY (id_estimacion) REFERENCES neuron.estimaciones(id);
ALTER TABLE neuron.costos_freelance ADD CONSTRAINT fk_costos_freelance_estimacion FOREIGN KEY (id_estimacion) REFERENCES neuron.estimaciones(id);

INSERT INTO neuron.estados (id, nombre, descripcion, entidad) VALUES
(1, 'Oportunidad', 'Inicio del ciclo: se identifica una necesidad o problema del negocio, Aqui se analiza si vale la pena desarrollar una solución', 'caso_uso'),
(2, 'Propuesta', 'Se plantea una solución al cliente o parte interesada. Se presentan objetivos, entregables y recursos necesarios (alcance preliminar)', 'caso_uso'),
(3, 'Aprobación', 'Las partes interesadas revisan la propuesta. si están de acuerdo con alcance, tiempos y costos, se da luz verde para iniciar formalmente el proyecto.', 'caso_uso'),
(4, 'En Desarrollo', 'Etapa de ejecución: se construyen los entregables del caso de uso (modelo, producto, sistema), con base en lo planteado.', 'caso_uso'),
(5, 'Testing', 'Validación de lo construido: Se hacen pruebas técnicas y/o funcionales con el cliente o equipo interno para asegurar calidad y cumplimiento del reqerimiento.', 'caso_uso'),
(6, 'Cierre', 'Se documenta lo realizado, se entregan los productos finales y se gestionan aspectos administrativos o contractuales (acta de cierre, manuales, transferencias).', 'caso_uso'),
(7, 'Evaluación', 'Se mide el impacto del caso de uso implementado. Se revisan aprendizajes, errores y valor generado. Puede incluir retroalimentación del cliente.', 'caso_uso'),
(8, 'Finalizados', 'Fin formal del caso de uso. El equipo se desasigna, se archiva la documentación y el caso se marca como completado en todos los sistemas.', 'caso_uso'),
(9, 'Planificado', 'El entregable está definido pero no ha iniciado su desarrollo', 'estimacion'),
(10, 'En desarrollo', 'El entregable está siendo construido, documentado o trabajado activamente.', 'estimacion'),
(11, 'En revisión', 'El entregable ha sido completado y está en evaluación por parte de stakeholders.', 'estimacion'),
(12, 'Ajustes requeridos', 'Se identificaron cambios tras la revisión inicial y debe ser ajustado.', 'estimacion'),
(13, 'Aprobado', 'El entregable ha sido validado formalmente y está listo para cierre.', 'estimacion'),
(14, 'Entregado', 'El entregable fue enviado al cliente interno o externo.', 'estimacion'),
(15, 'Cerrado', 'El entregable fue aceptado, documentado y archivado.', 'estimacion'),
(16, 'Cancelado', 'El entregable fue descartado o remplazado por decision del proyecto', 'estimacion'),
(17, 'Activo', 'Usuario con acceso completo autorizado al sistema.', 'usuario'),
(18, 'Inactivo', 'Usuario que fue registrado pero no tiene acceso temporalmente.', 'usuario'),
(19, 'Pendiente', 'Usuario recién creado que aún no ha completado el proceso de activación.', 'usuario'),
(20, 'Suspendido', 'Usuario cuyo acceso ha sido revocado por razones administrativas.', 'usuario'),
(21, 'Elimina', 'Usuario que fue dado de baja y ya no forma parte del sistema.', 'usuario'),
(22, 'Bloqueado', 'Usuario con acceso restringido por intentos fallidos de autenticación o incidentes.', 'usuario'),
(23, 'Verificado', 'Usuario que ha completado validaciones requeridas (correo, identidad, etc.).', 'usuario'),
(24, 'No Verificado', 'Usuario pendiente de verificación de datos clave.', 'usuario');

INSERT INTO neuron.roles (id, nombre) VALUES
(1, 'Aliado'),
(2, 'Gestor'),
(3, 'Supervisor'),
(4, 'Freelance'),
(5, 'Empleado');

INSERT INTO neuron.industrias (id, nombre, grupo_general, sector, nota) VALUES
(1, 'Agricultura, silvicultura y pesca', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(2, 'Explotación de minas y cantera', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(3, 'Industrias manufactureras', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(4, 'Suministro de electricidad, gas, vapor y airea acondicionado', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(5, 'Suministro de agua; alcantarillado, gestión de desechos y actividades de saneamiento', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(6, 'Construcción', 'Sector Primario', 'Sector Primario', 'Sector Primario'),
(8, 'Comercio al por mayor y al por menor; reparación de vehiculos de motor y motocicletas', 'Manufactura', 'Sector Secundario', 'Industrial'),
(9, 'Transporte y almacenamiento', 'Manufactura', 'Sector Secundario', 'Industrial'),
(10, 'Quimica y farmacéutica', 'Manufactura', 'Sector Secundario', 'Industrial'),
(11, 'Producción de metales', 'Manufactura', 'Sector Secundario', 'Industrial'),
(12, 'Construcción', 'Construcción', 'Sector Secundario', 'Industrial'),
(13, 'Energía eléctrica y gas', 'Energía e infraestructura', 'Sector Secundario', 'Industrial'),
(14, 'Comercio al por mayor y menor', 'Comercio', 'Sector Terciario', 'Servicios'),
(15, 'Transporte y logística', 'Servicios', 'Sector Terciario', 'Servicios'),
(16, 'Hotelería y turismo', 'Servicios', 'Sector Terciario', 'Servicios'),
(17, 'Tecnología de la información', 'Tecnología', 'Sector Terciario', 'Servicios'),
(18, 'Servicios financieros y seguros', 'Finanzas', 'Sector Terciario', 'Servicios'),
(19, 'Educación', 'Servicios Sociales', 'Sector Terciario', 'Servicios'),
(20, 'Salud y asistencia social', 'Servicios Sociales', 'Sector Terciario', 'Servicios'),
(21, 'Entretenimiento y medios', 'Creativas y Medios', 'Sector Terciario', 'Servicios'),
(22, 'Actividades profesionales y técnicas', 'Consultoria y Profesionales', 'Sector Terciario', 'Servicios'),
(23, 'Bienes raices e inmobiliaria', 'Inmobiliaria', 'Sector Terciario', 'Servicios'),
(24, 'Organizaciones no gubernamentales', 'Organizaciones sociales', 'Sector Cuaternario', 'Otros'),
(25, 'Administración pública', 'Gobierno', 'Sector Cuaternario', 'Otros'),
(26, 'Actividades religiosas', 'Sociedad Civil', 'Sector Cuaternario', 'Otros'),
(27, 'Investigación y desarrollo', 'Ciencia y Tecnología', 'Sector Cuaternario', 'Otros'),
(41, 'Freelance o Multisector', 'Freelance', 'Multisector', 'Otros');

INSERT INTO neuron.regiones (id, nombre, codigo, descripcion, activo) VALUES
(1, 'Norteamérica', 'NA', 'Incluye EE.UU., Canadá y territorios asociados', TRUE),
(2, 'América Latina y el Caribe', 'LATAM', 'Desde México hasta Sudamérica y el Caribe', TRUE),
(3, 'Europa Occidental', 'EUW', 'Incluye países como Francia, Alemania, España, etc.', TRUE),
(4, 'Europa Oriental', 'EUE', 'Países del este europeo y el área del Báltico', TRUE),
(5, 'África Septentrional', 'NAF', 'Países del norte de África, como Egipto, Marruecos', TRUE),
(6, 'África Subsahariana', 'SSAF', 'África central, oriental, occidental y austral', TRUE),
(7, 'Medio Oriente', 'ME', 'Península Arábiga, Irán, Israel, etc.', TRUE),
(8, 'Asia Meridional', 'SAS', 'India, Pakistán, Bangladesh y vecinos', TRUE),
(9, 'Sudeste Asiático', 'SEA', 'Incluye Indonesia, Vietnam, Filipinas, etc.', TRUE),
(10, 'Asia Oriental', 'EAS', 'China, Japón, Corea del Sur, etc.', TRUE),
(11, 'Asia Central', 'CAS', 'Kazajistán, Uzbekistán, Turkmenistán y vecinos', TRUE),
(12, 'Oceanía', 'OC', 'Incluye Australia, Nueva Zelanda y el Pacífico Sur', TRUE);

INSERT INTO neuron.subregiones (id, nombre, codigo, descripcion, id_region, activo) VALUES
(1, 'Estados Unidos', 'USA', 'Estados Unidos continental y territorios', 1, TRUE),
(2, 'Canadá', 'CAN', 'Incluye todas las provincias canadienses', 1, TRUE),
(3, 'México y Centroamérica', 'MEXCAM', 'Desde México hasta Panamá', 2, TRUE),
(4, 'Caribe', 'CAR', 'Islas del Caribe como Cuba, RD, PR, etc.', 2, TRUE),
(5, 'Región Andina', 'AND', 'Colombia, Ecuador, Perú, Bolivia y Venezuela', 2, TRUE),
(6, 'Cono Sur', 'SUR', 'Argentina, Chile, Uruguay y Paraguay', 2, TRUE),
(7, 'Europa Occidental', 'EUW', 'Francia, Alemania, España, Italia y más', 3, TRUE),
(8, 'Escandinavia', 'SCAN', 'Suecia, Noruega, Dinamarca, Finlandia', 3, TRUE),
(9, 'Europa Oriental', 'EUE', 'Polonia, Ucrania, Rumanía, etc.', 4, TRUE),
(10, 'Rusia y Cáucaso', 'RUSCAU', 'Rusia, Georgia, Armenia, Azerbaiyán', 4, TRUE),
(11, 'África del Norte', 'NAF', 'Egipto, Marruecos, Argelia, Túnez', 5, TRUE),
(12, 'África Occidental', 'WAF', 'Nigeria, Ghana, Senegal y vecinos', 6, TRUE),
(13, 'África Central', 'CAF', 'Camerún, Congo, RCA y vecinos', 6, TRUE),
(14, 'África Oriental', 'EAF', 'Etiopía, Kenia, Tanzania, etc.', 6, TRUE),
(15, 'África Austral', 'SAF', 'Sudáfrica, Namibia, Botsuana', 6, TRUE),
(16, 'Península Arábiga', 'ARAB', 'Arabia Saudita, EAU, Omán, etc.', 7, TRUE),
(17, 'Irán y Asia Occidental', 'WA', 'Irán, Iraq, Siria, Líbano, etc.', 7, TRUE),
(18, 'Asia Meridional', 'SAS', 'India, Pakistán, Bangladesh, Nepal', 8, TRUE),
(19, 'Sudeste Asiático', 'SEA', 'Vietnam, Tailandia, Indonesia, etc.', 9, TRUE),
(20, 'Asia Oriental', 'EAS', 'China, Japón, Corea del Sur', 10, TRUE),
(21, 'Asia Central', 'CAS', 'Kazajistán, Uzbekistán, etc.', 11, TRUE),
(22, 'Oceanía Insular', 'OCINS', 'Fiyi, Samoa, Islas Salomón', 12, TRUE),
(23, 'Australia y Nueva Zelanda', 'AUNZ', 'Australia y Nueva Zelanda', 12, TRUE);

INSERT INTO neuron.organizaciones (
  id, nombre, id_industria, fecha_registro, estado, contacto_principal, tamaño, empleados
) VALUES (
  1, 'DeepNova', 1, CURDATE(), 17, 'Carlos Ruiz', 'Mediana', 150
);

INSERT INTO neuron.sedes (
  id, id_organizacion, nombre_sede, subregion_id, direccion, ciudad, codigo_postal, pais, estado
) VALUES (
  1, 1, 'Sede Principal', 5, 'Calle 123', 'Bogotá', '110111', 'Colombia', 17
);

INSERT INTO neuron.usuarios (
  nombre,
  id_organizacion,
  id_sede,
  correo,
  contrasena,
  id_rol,
  estado,
  ultimo_login
) VALUES (
  'gestor1',
  1, -- organización existente
  1, -- sede existente
  'gestor1',
  "scrypt:32768:8:1$YZvX43qxe6GcHiT9$dc1ba21ef9172044c97bad8d39f921fd2224e116cbcfe1492338651c110fd07f0366f6bd56e0dd6a596f16e4122e61d595244a57b0d106f85a5f3f7da4858ef0",
  2, -- rol "Gestor"
  17, -- estado "Activo"
  NOW()
);

INSERT INTO neuron.usuarios (
  nombre,
  id_organizacion,
  id_sede,
  correo,
  contrasena,
  id_rol,
  estado,
  ultimo_login
) VALUES (
  'aliado1',
  1,
  1,
  'aliado1',
  "scrypt:32768:8:1$XyZp93LsKwEGrtY8$49cfe28b53c1a2c7d51e84a0a2b3956e57b8f13aacc0f4a47e8abebc0c6bb7a9be0c734b205bd1cbaef1c70b3b8deac1c57e7b02431c1731e0577a0f876adace",
  1,  -- Rol "Aliado"
  17, -- Estado "Activo"
  NOW()
);

INSERT INTO neuron.usuarios (
  nombre,
  id_organizacion,
  id_sede,
  correo,
  contrasena,
  id_rol,
  estado,
  ultimo_login
) VALUES (
  'consultor1',
  1,
  1,
  'consultor1',
  "scrypt:32768:8:1$PqR4mNxy7Ea9KXz1$8cc3bb6e2321fc0e4c6a776276c16f5f6e3d92035f1bd69f827c8f732eff71c4f239589bc2a705a5b13a7b3cbe6d3d41edc90e6b142182e52dd5f1a9e8c9f1b4",
  4,  -- Rol "Freelance"
  17, -- Estado "Activo"
  NOW()
);

SELECT id FROM neuron.usuarios WHERE correo = 'consultor1';

INSERT INTO neuron.consultores (
  id_usuario,
  especialidad,
  disponibilidad,
  nivel_segun_usuario,
  nivel_segun_gestor,
  fecha_incorporacion,
  direccion,
  ciudad,
  codigo_postal,
  pais,
  tarifa_hora,
  resumen_perfil,
  celular,
  linkedin
) VALUES (
  3,  -- ID del usuario Laura Méndez
  'Analítica de Datos',
  'Alta',
  75,
  70,
  CURRENT_DATE,
  'Calle 123 #45-67',
  'Bogotá',
  '110111',
  'Colombia',
  120000,
  'Especialista en inteligencia de negocios y modelos predictivos.',
  '+57 3001234567',
  'https://linkedin.com/in/lauramendez'
);

INSERT INTO neuron.proyectos_destacados (
  id_usuario,
  nombre,
  descripcion,
  tecnologias_usadas,
  fecha_inicio,
  fecha_fin,
  link_portafolio
) VALUES (
  3,
  'Modelo de predicción de ventas',
  'Desarrollé un modelo predictivo de ventas para una empresa retail usando Python y Prophet.',
  'Python, Prophet, Pandas, Power BI',
  '2023-03-01',
  '2023-07-30',
  'https://portafolio.laura.dev/prediccion-ventas'
);

INSERT INTO neuron.portafolio (
  nombre,
  categoria,
  familia,
  descripcion,
  tipo,
  estado,
  fecha_creacion,
  fecha_actualizacion
) VALUES (
  'Dashboard Ejecutivo de Ventas',
  'BI',
  'Dashboards',
  'Dashboard interactivo con visualización de KPIs de ventas por canal y producto.',
  'Producto Digital',
  17, -- Activo
  NOW(),
  NOW()
);

SELECT id FROM neuron.portafolio WHERE nombre = 'Dashboard Ejecutivo de Ventas';

INSERT INTO neuron.experiencia_laboral (
  id_usuario,
  cargo,
  empresa,
  descripcion,
  fecha_inicio,
  fecha_fin,
  ubicacion,
  tipo_empleo,
  sector,
  logros
) VALUES (
  3,
  'Analista de Datos',
  'DataCorp S.A.S.',
  'Responsable del análisis de datos operativos y financieros para apoyar decisiones estratégicas.',
  '2021-01-15',
  '2022-12-01',
  'Bogotá, Colombia',
  'Tiempo completo',
  'Tecnología',
  'Implementación de tableros en Power BI que redujeron el tiempo de reporte en 50%.'
);

INSERT INTO neuron.certificaciones (
  id_usuario,
  nombre,
  entidad,
  fecha_obtencion,
  fecha_vencimiento,
  url_certificado,
  id_credencial,
  descripcion
) VALUES (
  3,
  'Data Science Professional Certificate',
  'IBM',
  '2022-06-01',
  NULL,
  'https://www.credly.com/badges/laura-dspc',
  'DSPC-IBM-2022',
  'Certificación profesional en ciencia de datos con enfoque en Python, SQL y modelos estadísticos.'
);






