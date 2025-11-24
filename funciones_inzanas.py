
# Funcion que verifica la matricula
def VerificacionMatricula(matricula: str) -> bool:
    
    # Verifica que la matricula exista, osea, que el usuario haya puesto algo
    if not matricula:
        return False
    
    # Cuenta el numero de caracteres y qeu empieze con A01 para verificar que se una matricula valida
    if matricula.startswith('A01'):
        contador = 0
        for so in matricula:
            contador = contador + 1
        if contador == 9:
            return True
        else:
            return False
    else:
        return False

# Extrae las preguntas de un archivo txt
def cargar_preguntas():
    
    # Una lista donde se guardaran la pregunats
    preguntas = []
    
    # Abre el archivo txt y lo declara como f
    with open("preguntas.txt", "r", encoding="utf-8") as f:
        
        # Una lista temporal para separar las preguntas, y opciones
        bloque = []
        
        # Extrae las preguntas y opciones con un for 
        for linea in f:
            
            #Elimina saltos de linea y cosas asi
            linea = linea.strip()
            
            # Esto Divide las preguntas y sus respectivas opciones tomando como referencia ---
            if linea == "---": 
                preguntas.append(bloque)
                bloque = []
            else:
                bloque.append(linea)
        
        # Para evitar que queden bloques pendientes
        if bloque:
            preguntas.append(bloque)
    return preguntas

# Funcion para establecer cual es la pregunta actual usando las variables de pregunta y el numero de pregunta del archivo main
def obtener_pregunta(preguntas, numero):

    # Verifica que el numero de pregunta este en el rango de valores del numero de preguntas existentes
    if numero < 1 or numero > len(preguntas):
        return None, None

    # Establece cual es la pregunta actual xd
    pregunta_actual = preguntas[numero - 1]
    
    # Establece qeu la pregunta es la linea una de nuestro bloque con la pregunta y opciones
    texto_pregunta = pregunta_actual[0]
    
    # Las lineas que siguen son opciones
    opciones = pregunta_actual[1:]
    
    # devuelve la pregunta y las opciones
    return texto_pregunta, opciones


# Funcion que guarda las respuestas del usuario
def guardar_respuesta(numero, respuesta):
    
    # Establece donde se guarda
    archivo = "estadisticas.txt"
    
    # Un diccionario para almacenar cuantas veces se contesto cada pregunta
    conteos = {}

    # Este try lo que hace es verificar las respuestas ya existentes en el archivo para incluirlas
    try:
        
        # Abre archivo
        with open(archivo, "r", encoding="utf-8") as f:
            
            # Procesa los datos para que tengaun un formato de pregunta = respuesta (o mas bien el numero de veces que se selecciono la opcion)
            for linea in f:
                linea = linea.strip()
                if "=" in linea:
                    clave, valor = linea.split("=")
                    conteos[clave] = int(valor)
    
    # Error por si el archivo no existe
    except FileNotFoundError:
       # Para ignorar el error
        pass

    # Establece el formato de Numero pregunta- respuesta del usuario
    clave = f"P{numero}_{respuesta}"

    # Si ya hay mas respuestas Las incrementa en lugar de poner un formato nuevo
    if clave in conteos:
        conteos[clave] += 1
    else:
        conteos[clave] = 1

    # Guarda todo y lo vuelve a poner en el archivo sobrescribiendolo 
    with open(archivo, "w", encoding="utf-8") as f:
        for clave, valor in conteos.items():
            f.write(f"{clave}={valor}\n")
