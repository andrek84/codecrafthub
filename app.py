"""
=============================================================
 CodeCraftHub - API REST de seguimiento de cursos
 -------------------------------------------------------------
 Proyecto Final Parte 1 (Opcion B - Python + Flask)
 Permite a un desarrollador registrar los cursos que quiere
 aprender y llevar el control de su avance.
 Los datos se guardan en un archivo JSON local (sin base de datos).
=============================================================
"""

import json
import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

# -------------------------------------------------------------
# 1. CONFIGURACION DE LA APLICACION
# -------------------------------------------------------------
app = Flask(__name__)

# CORS permite que una pagina web abierta en el navegador
# pueda llamar a esta API. Es indispensable para la Parte 2.
CORS(app)

# Ruta del archivo donde se guardan los cursos.
# Se ubica siempre en la misma carpeta que este archivo app.py.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "courses.json")

# Unicos valores permitidos para el campo "status".
ESTADOS_VALIDOS = ["Not Started", "In Progress", "Completed"]


# -------------------------------------------------------------
# 2. FUNCIONES AUXILIARES DE ALMACENAMIENTO
# -------------------------------------------------------------
def load_courses():
    """Lee la lista de cursos desde courses.json.
    Si el archivo no existe, lo crea vacio automaticamente."""
    if not os.path.exists(DATA_FILE):
        save_courses([])
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        if not contenido:          # archivo vacio
            return []
        datos = json.loads(contenido)
        return datos if isinstance(datos, list) else []


def save_courses(courses):
    """Escribe la lista completa de cursos en courses.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as archivo:
        json.dump(courses, archivo, indent=2, ensure_ascii=False)


def get_next_id(courses):
    """Calcula el siguiente id. El primer curso siempre tendra id = 1."""
    if not courses:
        return 1
    return max(curso.get("id", 0) for curso in courses) + 1


def find_course(courses, course_id):
    """Busca un curso por su id. Devuelve (posicion, curso) o (None, None)."""
    for posicion, curso in enumerate(courses):
        if curso.get("id") == course_id:
            return posicion, curso
    return None, None


def timestamp():
    """Devuelve la fecha y hora actual como texto legible."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------------------------------------
# 3. RESPUESTAS CON FORMATO UNIFORME
# -------------------------------------------------------------
def respuesta_ok(data, mensaje="OK", codigo=200):
    return jsonify({"success": True, "message": mensaje, "data": data}), codigo


def respuesta_error(mensaje, codigo=400, errores=None):
    return jsonify({"success": False, "message": mensaje, "errors": errores or []}), codigo


# -------------------------------------------------------------
# 4. VALIDACION DE LOS DATOS QUE ENVIA EL CLIENTE
# -------------------------------------------------------------
def validar_curso(datos, es_actualizacion=False):
    """Revisa que los datos del curso sean correctos.
    Devuelve una lista de errores; si esta vacia, todo esta bien."""
    errores = []

    if not isinstance(datos, dict):
        return ["El cuerpo de la peticion debe ser un objeto JSON."]

    # --- name: obligatorio al crear ---
    if not es_actualizacion or "name" in datos:
        nombre = datos.get("name")
        if not isinstance(nombre, str) or not nombre.strip():
            errores.append("El campo 'name' es obligatorio y no puede estar vacio.")

    # --- description: obligatorio al crear ---
    if not es_actualizacion or "description" in datos:
        descripcion = datos.get("description")
        if not isinstance(descripcion, str) or not descripcion.strip():
            errores.append("El campo 'description' es obligatorio y no puede estar vacio.")

    # --- target_date: obligatorio al crear, formato YYYY-MM-DD ---
    if not es_actualizacion or "target_date" in datos:
        fecha = datos.get("target_date")
        if not isinstance(fecha, str) or not fecha.strip():
            errores.append("El campo 'target_date' es obligatorio (formato YYYY-MM-DD).")
        else:
            try:
                datetime.strptime(fecha.strip(), "%Y-%m-%d")
            except ValueError:
                errores.append("El campo 'target_date' debe tener el formato YYYY-MM-DD.")

    # --- status: obligatorio al crear, valor de la lista permitida ---
    if not es_actualizacion or "status" in datos:
        estado = datos.get("status")
        if estado not in ESTADOS_VALIDOS:
            errores.append(
                "El campo 'status' es obligatorio y debe ser uno de: "
                + ", ".join(ESTADOS_VALIDOS)
                + "."
            )

    return errores


# =============================================================
# 5. ENDPOINTS DE LA API
# =============================================================

# -------- GET /api/courses/stats --------
# IMPORTANTE: esta ruta se define ANTES de /api/courses/<id>.
# Si se definiera despues, Flask interpretaria "stats" como un id.
@app.route("/api/courses/stats", methods=["GET"])
def course_stats():
    """Devuelve estadisticas: total de cursos y conteo por estado."""
    try:
        cursos = load_courses()
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo leer el archivo de datos.", 500)

    conteo = {estado: 0 for estado in ESTADOS_VALIDOS}
    for curso in cursos:
        estado = curso.get("status")
        if estado in conteo:
            conteo[estado] += 1

    estadisticas = {"total_courses": len(cursos), "by_status": conteo}
    return respuesta_ok(estadisticas, "Estadisticas generadas correctamente")


# -------- GET /api/courses --------
@app.route("/api/courses", methods=["GET"])
def get_courses():
    """Devuelve todos los cursos registrados."""
    try:
        cursos = load_courses()
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo leer el archivo de datos.", 500)

    return respuesta_ok(cursos, f"Se encontraron {len(cursos)} curso(s)")


# -------- GET /api/courses/<id> --------
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Devuelve un curso especifico segun su id."""
    try:
        cursos = load_courses()
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo leer el archivo de datos.", 500)

    _, curso = find_course(cursos, course_id)
    if curso is None:
        return respuesta_error(f"No existe un curso con id {course_id}.", 404)

    return respuesta_ok(curso, "Curso encontrado")


# -------- POST /api/courses --------
@app.route("/api/courses", methods=["POST"])
def create_course():
    """Crea un curso nuevo."""
    datos = request.get_json(silent=True)
    if datos is None:
        return respuesta_error(
            "El cuerpo debe ser JSON valido con el encabezado "
            "Content-Type: application/json.", 400
        )

    errores = validar_curso(datos)
    if errores:
        return respuesta_error("Datos invalidos.", 400, errores)

    try:
        cursos = load_courses()
        nuevo_curso = {
            "id": get_next_id(cursos),
            "name": datos["name"].strip(),
            "description": datos["description"].strip(),
            "target_date": datos["target_date"].strip(),
            "status": datos["status"],
            "created_at": timestamp(),
        }
        cursos.append(nuevo_curso)
        save_courses(cursos)
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo guardar el archivo de datos.", 500)

    return respuesta_ok(nuevo_curso, "Curso creado correctamente", 201)


# -------- PUT /api/courses/<id> --------
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Actualiza un curso existente. Solo cambia los campos enviados."""
    datos = request.get_json(silent=True)
    if datos is None:
        return respuesta_error(
            "El cuerpo debe ser JSON valido con el encabezado "
            "Content-Type: application/json.", 400
        )

    errores = validar_curso(datos, es_actualizacion=True)
    if errores:
        return respuesta_error("Datos invalidos.", 400, errores)

    try:
        cursos = load_courses()
        posicion, curso = find_course(cursos, course_id)
        if curso is None:
            return respuesta_error(f"No existe un curso con id {course_id}.", 404)

        for campo in ["name", "description", "target_date", "status"]:
            if campo in datos:
                valor = datos[campo]
                curso[campo] = valor.strip() if isinstance(valor, str) else valor

        curso["updated_at"] = timestamp()
        cursos[posicion] = curso
        save_courses(cursos)
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo guardar el archivo de datos.", 500)

    return respuesta_ok(curso, "Curso actualizado correctamente")


# -------- DELETE /api/courses/<id> --------
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Elimina un curso segun su id."""
    try:
        cursos = load_courses()
        posicion, curso = find_course(cursos, course_id)
        if curso is None:
            return respuesta_error(f"No existe un curso con id {course_id}.", 404)

        cursos.pop(posicion)
        save_courses(cursos)
    except (OSError, json.JSONDecodeError):
        return respuesta_error("No se pudo guardar el archivo de datos.", 500)

    return respuesta_ok({"id": course_id}, "Curso eliminado correctamente")


# =============================================================
# 6. MANEJO GLOBAL DE ERRORES
# =============================================================
@app.errorhandler(404)
def ruta_no_encontrada(_error):
    return respuesta_error("Ruta no encontrada. Verifica la URL.", 404)


@app.errorhandler(405)
def metodo_no_permitido(_error):
    return respuesta_error("Metodo HTTP no permitido para esta ruta.", 405)


@app.errorhandler(500)
def error_interno(_error):
    return respuesta_error("Error interno del servidor.", 500)


# =============================================================
# 7. ARRANQUE DEL SERVIDOR
# =============================================================
if __name__ == "__main__":
    print("- CodeCraftHub API is starting...")
    print(f"- Data will be stored in: {DATA_FILE}")
    print("- API will be available at: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
