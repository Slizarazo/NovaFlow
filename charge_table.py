from config import workbench_db as mydb

regiones = [
    [1, "Norteamérica", "NA", "Incluye EE.UU., Canadá y territorios asociados", True],
    [2, "América Latina y el Caribe", "LATAM", "Desde México hasta Sudamérica y el Caribe", True],
    [3, "Europa Occidental", "EUW", "Incluye países como Francia, Alemania, España, etc.", True],
    [4, "Europa Oriental", "EUE", "Países del este europeo y el área del Báltico", True],
    [5, "África Septentrional", "NAF", "Países del norte de África, como Egipto, Marruecos", True],
    [6, "África Subsahariana", "SSAF", "África central, oriental, occidental y austral", True],
    [7, "Medio Oriente", "ME", "Península Arábiga, Irán, Israel, etc.", True],
    [8, "Asia Meridional", "SAS", "India, Pakistán, Bangladesh y vecinos", True],
    [9, "Sudeste Asiático", "SEA", "Incluye Indonesia, Vietnam, Filipinas, etc.", True],
    [10, "Asia Oriental", "EAS", "China, Japón, Corea del Sur, etc.", True],
    [11, "Asia Central", "CAS", "Kazajistán, Uzbekistán, Turkmenistán y vecinos", True],
    [12, "Oceanía", "OC", "Incluye Australia, Nueva Zelanda y el Pacífico Sur", True]
]

class Regiones:
    def __init__(self, nombre, codigo, descripcion, id_region, activo):
        self.nombre = nombre
        self.codigo = codigo
        self.descripcion = descripcion
        self.id_region = id_region
        self.activo = activo

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = 'INSERT INTO regiones (nombre, codigo, descripcion, id_region, activo) VALUES(%s, %s, %s, %s, %s)'
        values = (self.nombre, self.codigo, self.descripcion, self.id_region, self.activo)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

for r in regiones:
    new_region = Regiones(r[1], r[2], r[3], r[4], r[5])
    new_region.create()

subregiones = [
    [1, "Estados Unidos", "USA", "Estados Unidos continental y territorios", 1, True],
    [2, "Canadá", "CAN", "Incluye todas las provincias canadienses", 1, True],
    [3, "México y Centroamérica", "MEXCAM", "Desde México hasta Panamá", 2, True],
    [4, "Caribe", "CAR", "Islas del Caribe como Cuba, RD, PR, etc.", 2, True],
    [5, "Región Andina", "AND", "Colombia, Ecuador, Perú, Bolivia y Venezuela", 2, True],
    [6, "Cono Sur", "SUR", "Argentina, Chile, Uruguay y Paraguay", 2, True],
    [7, "Europa Occidental", "EUW", "Francia, Alemania, España, Italia y más", 3, True],
    [8, "Escandinavia", "SCAN", "Suecia, Noruega, Dinamarca, Finlandia", 3, True],
    [9, "Europa Oriental", "EUE", "Polonia, Ucrania, Rumanía, etc.", 4, True],
    [10, "Rusia y Cáucaso", "RUSCAU", "Rusia, Georgia, Armenia, Azerbaiyán", 4, True],
    [11, "África del Norte", "NAF", "Egipto, Marruecos, Argelia, Túnez", 5, True],
    [12, "África Occidental", "WAF", "Nigeria, Ghana, Senegal y vecinos", 6, True],
    [13, "África Central", "CAF", "Camerún, Congo, RCA y vecinos", 6, True],
    [14, "África Oriental", "EAF", "Etiopía, Kenia, Tanzania, etc.", 6, True],
    [15, "África Austral", "SAF", "Sudáfrica, Namibia, Botsuana", 6, True],
    [16, "Península Arábiga", "ARAB", "Arabia Saudita, EAU, Omán, etc.", 7, True],
    [17, "Irán y Asia Occidental", "WA", "Irán, Iraq, Siria, Líbano, etc.", 7, True],
    [18, "Asia Meridional", "SAS", "India, Pakistán, Bangladesh, Nepal", 8, True],
    [19, "Sudeste Asiático", "SEA", "Vietnam, Tailandia, Indonesia, etc.", 9, True],
    [20, "Asia Oriental", "EAS", "China, Japón, Corea del Sur", 10, True],
    [21, "Asia Central", "CAS", "Kazajistán, Uzbekistán, etc.", 11, True],
    [22, "Oceanía Insular", "OCINS", "Fiyi, Samoa, Islas Salomón", 12, True],
    [23, "Australia y Nueva Zelanda", "AUNZ", "Australia y Nueva Zelanda", 12, True]
]

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

for r in subregiones:
    new_region = Subregiones(r[1], r[2], r[3], r[4], r[5])
    new_region.create()

segmentacion = [
    [1, 'A', None],
    [2, 'B', None],
    [3, 'C', None],
]

class Segmentacion:

    def __init__(self, clasificacion, descripcion):
        self.claseificaicon = clasificacion
        self.descripcion = descripcion

    def create(self):
        conn = mydb('nova_flow')
        mycursor = conn.cursor()

        query = "INSERT INTO segmentacion (clasificacion, descripcion) VALUES(%s, %s);"
        values = (self.clasificaicon, self.descripcion)

        mycursor.execute(query, values)
        conn.commit()

        mycursor.close()
        conn.close()

for r in segmentacion:
    new_region = Segmentacion(r[1], r[2])
    new_region.create()

roles = [
    [1, 'Aliado'],
    [2, 'Gestor'],
    [3, 'Supervisor'],
    [4, 'Freelance'],
    [5, 'Empleado'],
]

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

for r in roles:
    new_region = Roles(r[1])
    new_region.create()

industrias = [
    [1, "Agricultura, silvicultura y pesca", "Sector Primario", "Sector Primario", "Sector Primario"],
    [2, "Explotación de minas y cantera", "Sector Primario", "Sector Primario", "Sector Primario"],
    [3, "Industrias manufactureras", "Sector Primario", "Sector Primario", "Sector Primario"],
    [4, "Suministro de electricidad, gas, vapor y airea acondicionado", "Sector Primario", "Sector Primario", "Sector Primario"],
    [5, "Suministro de agua; alcantarillado, gestión de desechos y actividades de saneamiento", "Sector Primario", "Sector Primario", "Sector Primario"],
    [6, "Construcción", "Sector Primario", "Sector Primario", "Sector Primario"],
    [8, "Comercio al por mayor y al por menor; reparación de vehiculos de motor y motocicletas", "Manufactura", "Sector Secundario", "Industrial"],
    [9, "Transporte y almacenamiento", "Manufactura", "Sector Secundario", "Industrial"],
    [10, "Quimica y farmacéutica", "Manufactura", "Sector Secundario", "Industrial"],
    [11, "Producción de metales", "Manufactura", "Sector Secundario", "Industrial"],
    [12, "Construcción", "Construcción", "Sector Secundario", "Industrial"],
    [13, "Energía eléctrica y gas", "Energía e infraestructura", "Sector Secundario", "Industrial"],
    [14, "Comercio al por mayor y menor", "Comercio", "Sector Terciario", "Servicios"],
    [15, "Transporte y logística", "Servicios", "Sector Terciario", "Servicios"],
    [16, "Hotelería y turismo", "Servicios", "Sector Terciario", "Servicios"],
    [17, "Tecnología de la información", "Tecnología", "Sector Terciario", "Servicios"],
    [18, "Servicios financieros y seguros", "Finanzas", "Sector Terciario", "Servicios"],
    [19, "Educación", "Servicios Sociales", "Sector Terciario", "Servicios"],
    [20, "Salud y asistencia social", "Servicios Sociales", "Sector Terciario", "Servicios"],
    [21, "Entretenimiento y medios", "Creativas y Medios", "Sector Terciario", "Servicios"],
    [22, "Actividades profesionales y técnicas", "Consultoria y Profesionales", "Sector Terciario", "Servicios"],
    [23, "Bienes raices e inmobiliaria", "Inmobiliaria", "Sector Terciario", "Servicios"],
    [24, "Organizaciones no gubernamentales", "Organizaciones sociales", "Sector Cuaternario", "Otros"],
    [25, "Administración pública", "Gobierno", "Sector Cuaternario", "Otros"],
    [26, "Actividades religiosas", "Sociedad Civil", "Sector Cuaternario", "Otros"],
    [27, "Investigación y desarrollo", "Ciencia y Tecnología", "Sector Cuaternario", "Otros"],
    [41, "Freelance o Multisector", "Freelance", "Multisector", "Otros"]
]

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

for r in industrias:
    new_region = Industrias(r[1], r[2], r[3], r[4])
    new_region.create()

















