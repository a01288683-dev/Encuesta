# Se importa la libreria flask que sirve connectar el Backend con el Frontend y funciones 
# desde el archivo funiones inzanas
from flask import Flask, request, render_template, redirect, url_for
from funciones_inzanas import VerificacionMatricula, cargar_preguntas, obtener_pregunta, guardar_respuesta

# Crea el server
app = Flask(__name__)

# Carga las preguntas desde una funcion 
preguntas = cargar_preguntas()   

# El decorador de la primera pagina de la web y su respectiva funcion para cargar el archivo html
@app.route("/")
def main_page():
    return render_template("index.html")

# Decorador y funcion para la utilidad de enviar la matricula al backend y ejecutar la funcion que la verifica
@app.route("/guardar", methods=["POST"])
def guardar():
    
    #Obtiene la matricula del frontend
    matricula = request.form.get("matricula")

# Verifica (cargando una funcion) y recarga la pagina dependiendo de la verificacion
    if VerificacionMatricula(matricula):
        return redirect(url_for("page_preguntas"))
    else:
        return render_template("index.html", mensaje='Matricula invalida')

# Decorador y respectiva funcion para cargar una pagina intermedia
@app.route("/page_preguntas")
def page_preguntas():
    return render_template("page_preguntas.html")

# Decorador y funcion para redirigir la pagina si el usuario pulsa un boton de la pagina de arriba xd
@app.route('/redirigir', methods=['POST'])
def redirigir():
    return redirect(url_for('pagina_preguntas'))

# Decorador y funcion que carga la pagina de preguntas principal de la web
@app.route("/preguntas")
def pagina_preguntas():
    # Cuenta el numero de pregunta 
    numero = int(request.args.get("n", 1))  

    # Extrar preguntas y opciones con una funcion externa 
    texto, opciones = obtener_pregunta(preguntas, numero)

    # Detiene la carga de preguntas y termina la encuesta cuando se acaban las preguntas 
    if texto is None:
        return "¡Gracias por completar la encuesta!"

    # Envia el numero de pregunta, pregunta y opciones, para despues cargar la pagina
    return render_template("pregunta.html",
                           numero=numero,
                           texto=texto,
                           opciones=opciones)

# Decorador y respectiva funcion para la extraccion de las respuestas del usuario
@app.route("/respuesta", methods=["POST"])
def respuesta():
    
    # Pide y extrae el numero de pregunta y la respuesta del usuario
    numero = int(request.form["numero"])
    opcion = request.form["respuesta"]

    # Utiliza una funcion externa con las variables del numero de pregunta y la respuesta del usuario para guardarlas
    guardar_respuesta(numero, opcion)

    # Redirige al usuario segun la pregunta y el numero de respuestas
    siguiente = numero + 1
    return redirect(url_for("pagina_preguntas", n=siguiente))

# establece que este codigo es el main del server y que solo se va ejecutar este exceptuando las funciones importadas y tameplates
if __name__ == "__main__":
    # Modo debug
    app.run(debug=True)

