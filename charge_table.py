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


