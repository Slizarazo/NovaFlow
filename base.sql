Table nova_flow.Organizaciones {
  id int [pk, increment]
  nombre varchar
  id_industria int
  fecha_registro date
  estado varchar
  contacto_principal varchar
  tamaño varchar
  empleados int
}

Table nova_flow.Sedes {
  id int [pk, increment]
  id_organizacion int
  nombre_sede varchar
  subregion varchar
  direccion varchar
  ciudad varchar
  codigo_postal varchar
  pais varchar
}

Table nova_flow.Subregiones {
  id int [pk, increment]
  nombre varchar
  codigo varchar
  descripcion text
  id_region int
  activo varchar
}

Table nova_flow.Regiones {
  id int [pk, increment]
  nombre varchar
  codigo varchar
  descripcion text
  id_region int
  activo varchar
}

Table nova_flow.Colaboradores {
  id int [pk, increment]
  id_usuario int
  id_organizacion int
  cargo varchar
  rol_laboral varchar
}

Table nova_flow.Industrias {
  id int [pk, increment]
  nombre varchar
  grupo_general varchar
  sector varchar
  nota text
}

Table nova_flow.Usuario {
  id int [pk, increment]
  nombre varchar
  id_organizacion int
  id_sede int
  correo varchar
  contrasena varchar
  id_rol int
  estado varchar
  ultimo_login date
}

Table nova_flow.Portafolio {
  id int [pk, increment]
  nombre varchar
  categoria varchar
  familia varchar
  descripcion text
  tipo varchar
  estado varchar
  fecha_creacion date
  fecha_actualizacion date
}

Table nova_flow.Consultores {
  id int [pk, increment]
  id_usuario int
  especialidad varchar
  disponibilidad int
  nivel_segun_usuario int
  nivel_segun_gestor int
  fecha_incorporacion date
  direccion varchar
  ciudad varchar
  codigo_postal varchar
  pais varchar
  tarifa_hora decimal
  resumen_perfil text
}

Table nova_flow.Comunidades {
  id int [pk, increment]
  nombre varchar
  descripcion text
  tipo varchar
}

Table nova_flow.Miembros_comunidad {
  id int [pk, increment]
  id_comunidad int
  id_usuario int
  rol_en_comunidad varchar
  fecha_union date
}

Table nova_flow.Personas_cliente {
  id int [pk, increment]
  id_sede int
  id_usuario int
  rol_en_cliente varchar
  fecha_asignacion date
}

Table nova_flow.Comunidad_aliado {
  id int [pk, increment]
  id_sede int
  id_comunidad int
  fecha_asignacion date
  observaciones text
}

Table nova_flow.Casos_uso {
  id int [pk, increment]
  id_aliado int
  id_usuario int
  id_cuenta int
  caso_uso varchar
  descripcion text
  impacto text
  puntuacion_impacto int
  puntuacion_tecnica int
  tags text
  estado varchar
  id_producto int
  fecha_inicio date
  fecha_cierre date
  monto_venta decimal
  costos_proyecto decimal
  margen_estimado_porcentaje decimal
  margen_estimado_bruto decimal
  feedback text
}

Table nova_flow.Cuentas {
  id int [pk, increment]
  id_organizacion int
  nombre varchar
  industria varchar
  subregion varchar
  fecha_alta date
  fecha_modificacion date
  fecha_baja date
  codigo varchar
  id_segmentacion int
  estado varchar
}

Table nova_flow.Segmentacion {
  id int [pk, increment]
  clasificacion varchar
  descripcion text
}

Table nova_flow.Roles {
  id int [pk, increment]
  nombre varchar
}
