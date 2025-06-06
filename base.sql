CREATE TABLE nova_flow.`organizaciones` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `id_industria` int,
  `fecha_registro` date,
  `estado` varchar(255),
  `contacto_principal` varchar(255),
  `tamaño` varchar(255),
  `empleados` int
);

CREATE TABLE nova_flow.`sedes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_organizacion` int,
  `nombre_sede` varchar(255),
  `subregion` varchar(255),
  `direccion` varchar(255),
  `ciudad` varchar(255),
  `codigo_postal` varchar(255),
  `pais` varchar(255)
);

CREATE TABLE nova_flow.`subregiones` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `codigo` varchar(255),
  `descripcion` text,
  `id_region` int,
  `activo` varchar(255)
);

CREATE TABLE nova_flow.`regiones` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `codigo` varchar(255),
  `descripcion` text,
  `id_region` int,
  `activo` varchar(255)
);

CREATE TABLE nova_flow.`colaboradores` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_usuario` int,
  `id_organizacion` int,
  `cargo` varchar(255),
  `rol_laboral` varchar(255)
);

CREATE TABLE nova_flow.`industrias` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `grupo_general` varchar(255),
  `sector` varchar(255),
  `nota` text
);

CREATE TABLE nova_flow.`usuario` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `id_organizacion` int,
  `id_sede` int,
  `correo` varchar(255),
  `contrasena` varchar(255),
  `id_rol` int,
  `estado` varchar(255),
  `ultimo_login` date
);

CREATE TABLE nova_flow.`portafolio` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `categoria` varchar(255),
  `familia` varchar(255),
  `descripcion` text,
  `tipo` varchar(255),
  `estado` varchar(255),
  `fecha_creacion` date,
  `fecha_actualizacion` date
);

CREATE TABLE nova_flow.`consultores` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_usuario` int,
  `especialidad` varchar(255),
  `disponibilidad` int,
  `nivel_segun_usuario` int,
  `nivel_segun_gestor` int,
  `fecha_incorporacion` date,
  `direccion` varchar(255),
  `ciudad` varchar(255),
  `codigo_postal` varchar(255),
  `pais` varchar(255),
  `tarifa_hora` decimal,
  `resumen_perfil` text
);

CREATE TABLE nova_flow.`comunidades` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `descripcion` text,
  `tipo` varchar(255)
);

CREATE TABLE nova_flow.`miembros_comunidad` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_comunidad` int,
  `id_usuario` int,
  `rol_en_comunidad` varchar(255),
  `fecha_union` date
);

CREATE TABLE nova_flow.`personas_cliente` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_sede` int,
  `id_usuario` int,
  `rol_en_cliente` varchar(255),
  `fecha_asignacion` date
);

CREATE TABLE nova_flow.`comunidad_aliado` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_sede` int,
  `id_comunidad` int,
  `fecha_asignacion` date,
  `observaciones` text
);

CREATE TABLE nova_flow.`casos_uso` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_aliado` int,
  `id_usuario` int,
  `id_cuenta` int,
  `caso_uso` varchar(255),
  `descripcion` text,
  `impacto` text,
  `puntuacion_impacto` int,
  `puntuacion_tecnica` int,
  `tags` text,
  `estado` varchar(255),
  `id_producto` int,
  `fecha_inicio` date,
  `fecha_cierre` date,
  `monto_venta` decimal,
  `costos_proyecto` decimal,
  `margen_estimado_porcentaje` decimal,
  `margen_estimado_bruto` decimal,
  `feedback` text
);

CREATE TABLE nova_flow.`cuentas` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `id_organizacion` int,
  `nombre` varchar(255),
  `industria` varchar(255),
  `subregion` varchar(255),
  `fecha_alta` date,
  `fecha_modificacion` date,
  `fecha_baja` date,
  `codigo` varchar(255),
  `id_segmentacion` int,
  `estado` varchar(255)
);

CREATE TABLE nova_flow.`segmentacion` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `clasificacion` varchar(255),
  `descripcion` text
);

CREATE TABLE nova_flow.`roles` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255)
);
