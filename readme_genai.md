CodeCraftHub
API REST sencilla para gestionar cursos de aprendizaje personalizados. El proyecto está construido con Python y Flask, y utiliza un archivo local llamado
courses.json
para almacenar la información, sin necesidad de una base de datos.

Este README está pensado para personas que están aprendiendo a trabajar con APIs REST por primera vez.

1. Visión general
CodeCraftHub permite crear, consultar, actualizar y eliminar cursos mediante una API REST.

Cada curso contiene los siguientes campos:

Campo	Descripción
id
Identificador único del curso. Lo genera la aplicación.
name
Nombre del curso.
description
Descripción del curso.
target_date
Fecha objetivo en formato
YYYY-MM-DD
.
status
Estado actual del curso.
Los valores permitidos para
status
son:

Not Started
In Progress
Completed
La aplicación almacena los cursos en un archivo JSON local:

courses.json
El archivo contiene una lista simple:

[
  {
    "id": "course-001",
    "name": "Python Fundamentals",
    "description": "Introduction to Python programming.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }
]
2. Características principales
API REST desarrollada con Flask.
Operaciones CRUD completas:
Crear cursos.
Consultar todos los cursos.
Consultar un curso por su identificador.
Actualizar cursos.
Eliminar cursos.
Persistencia en el archivo local
courses.json
.
Validación de:
Campos obligatorios.
Estados permitidos.
Formato de fechas.
Endpoint de comprobación de salud de la aplicación.
Endpoint de estadísticas de cursos.
Respuestas en formato JSON.
Uso de códigos de estado HTTP apropiados.
Estructura uniforme para respuestas exitosas y errores.
3. Requisitos previos
Antes de instalar el proyecto, asegúrate de tener instalado:

Python 3.9 o superior.
pip
, el gestor de paquetes de Python.
Git, opcional pero recomendado.
Una terminal:
Terminal de macOS o Linux.
PowerShell o CMD en Windows.
Puedes comprobar la versión de Python con:

python --version
En algunos sistemas puede ser necesario utilizar:

python3 --version
4. Instalación paso a paso
4.1 Clonar el repositorio
Si el proyecto está almacenado en Git:

git clone https://github.com/usuario/codecrafthub.git
cd codecrafthub
Si ya tienes los archivos del proyecto, simplemente abre una terminal dentro de la carpeta raíz.

4.2 Crear un entorno virtual
Un entorno virtual permite instalar las dependencias del proyecto sin afectar a otros proyectos de Python.

Windows
python -m venv venv
venv\Scripts\activate
Si utilizas PowerShell:

python -m venv venv
venv\Scripts\Activate.ps1
macOS o Linux
python3 -m venv venv
source venv/bin/activate
Cuando el entorno virtual esté activo, normalmente aparecerá
(venv)
al principio de la línea de comandos.

4.3 Instalar las dependencias
Si existe un archivo
requirements.txt
, ejecuta:

pip install -r requirements.txt
Si el archivo no existe, instala Flask manualmente:

pip install Flask
Para guardar las dependencias instaladas:

pip freeze > requirements.txt
Un archivo
requirements.txt
básico puede contener:

Flask
4.4 Crear el archivo de datos
El archivo
courses.json
debe encontrarse en la ubicación esperada por la aplicación.

Si todavía no existe, créalo con el siguiente contenido:

[]
Esto representa una lista vacía de cursos.

Si quieres comenzar con un curso de ejemplo:

[
  {
    "id": "course-001",
    "name": "Python Fundamentals",
    "description": "Introduction to Python programming.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }
]
Asegúrate de que el archivo contenga JSON válido.

5. Cómo ejecutar la aplicación
Opción A: ejecutar con
flask
Si el archivo principal se llama
app.py
:

Windows
flask --app app run --debug
macOS o Linux
FLASK_APP=app.py flask run --debug
La API estará disponible en:

http://127.0.0.1:5000
También puedes utilizar:

http://localhost:5000
Opción B: ejecutar directamente el archivo Python
Si
app.py
contiene un bloque de ejecución:

if __name__ == "__main__":
    app.run(debug=True)
puedes iniciar la aplicación con:

python app.py
En macOS o Linux:

python3 app.py
Detener la aplicación
Para detener el servidor, pulsa:

Ctrl + C
6. Formato de las respuestas
Respuesta exitosa
Las respuestas exitosas utilizan esta estructura:

{
  "success": true,
  "message": "Course retrieved successfully",
  "data": {}
}
Respuesta con error
Las respuestas de error utilizan esta estructura:

{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "The name field is required"
  ]
}
El campo
errors
contiene una lista de mensajes explicando el problema.

7. Documentación de la API
La URL base utilizada en los ejemplos es:

BASE_URL="http://localhost:5000"
En Windows PowerShell puedes definirla así:

$BASE_URL = "http://localhost:5000"
Los ejemplos siguientes utilizan
curl
, una herramienta de línea de comandos para realizar peticiones HTTP.

7.1 Comprobar el estado de la API
Endpoint
GET /api/health
Ejemplo
curl -i http://localhost:5000/api/health
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "ok"
  }
}
Este endpoint sirve para verificar que el servidor está funcionando.

7.2 Obtener todos los cursos
Endpoint
GET /api/courses
Ejemplo
curl -i http://localhost:5000/api/courses
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "Courses retrieved successfully",
  "data": [
    {
      "id": "course-001",
      "name": "Python Fundamentals",
      "description": "Introduction to Python programming.",
      "target_date": "2026-12-31",
      "status": "Not Started"
    }
  ]
}
Si no existen cursos:

{
  "success": true,
  "message": "Courses retrieved successfully",
  "data": []
}
7.3 Obtener un curso por ID
Endpoint
GET /api/courses/<id>
Sustituye
<id>
por el identificador real del curso.

Ejemplo
curl -i http://localhost:5000/api/courses/course-001
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "Course retrieved successfully",
  "data": {
    "id": "course-001",
    "name": "Python Fundamentals",
    "description": "Introduction to Python programming.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }
}
Si el curso no existe:

404 Not Found
{
  "success": false,
  "message": "Course not found",
  "errors": [
    "No course exists with id course-999"
  ]
}
7.4 Crear un curso
Endpoint
POST /api/courses
Campos de la solicitud
{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-11-30",
  "status": "Not Started"
}
El campo
id
no debe enviarse al crear un curso. La aplicación debe generarlo.

Ejemplo con
curl
curl -i -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs with Flask.",
    "target_date": "2026-11-30",
    "status": "Not Started"
  }'
Respuesta esperada
Código HTTP:

201 Created
Respuesta:

{
  "success": true,
  "message": "Course created successfully",
  "data": {
    "id": "course-002",
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs with Flask.",
    "target_date": "2026-11-30",
    "status": "Not Started"
  }
}
El valor exacto de
id
dependerá de la implementación.

7.5 Actualizar un curso
Endpoint
PUT /api/courses/<id>
Ejemplo de carga útil
{
  "name": "Flask REST APIs Updated",
  "description": "Build REST APIs using Flask.",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
Ejemplo con
curl
curl -i -X PUT http://localhost:5000/api/courses/course-002 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs Updated",
    "description": "Build REST APIs using Flask.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }'
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "Course updated successfully",
  "data": {
    "id": "course-002",
    "name": "Flask REST APIs Updated",
    "description": "Build REST APIs using Flask.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }
}
El campo
id
debe conservarse durante la actualización.

7.6 Eliminar un curso
Endpoint
DELETE /api/courses/<id>
Ejemplo
curl -i -X DELETE http://localhost:5000/api/courses/course-002
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "Course deleted successfully",
  "data": {
    "id": "course-002"
  }
}
Después de eliminar el curso, una consulta a:

GET /api/courses/course-002
debería devolver
404 Not Found
.

7.7 Obtener estadísticas
Endpoint
GET /api/courses/stats
Ejemplo
curl -i http://localhost:5000/api/courses/stats
Respuesta esperada
Código HTTP:

200 OK
Respuesta:

{
  "success": true,
  "message": "Course statistics retrieved successfully",
  "data": {
    "total_courses": 3,
    "by_status": {
      "Not Started": 1,
      "In Progress": 1,
      "Completed": 1
    }
  }
}
La ruta
/api/courses/stats
debe definirse antes de la ruta dinámica
/api/courses/<id>
. De lo contrario, Flask podría interpretar
stats
como si fuera el identificador de un curso.

8. Validaciones
Campo
name
Debe:

Estar presente en las solicitudes de creación y actualización.
Ser una cadena de texto.
No estar vacío.
Ejemplo incorrecto:

{
  "name": "",
  "description": "Example",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Campo
description
Debe ser una cadena de texto si se proporciona.

Ejemplo:

{
  "description": "Introduction to Flask."
}
Campo
target_date
Debe utilizar el formato:

YYYY-MM-DD
Ejemplos válidos:

2026-12-31
2027-01-15
2028-06-01
Ejemplos inválidos:

31-12-2026
12/31/2026
2026/12/31
2026-2-1
Campo
status
Solo se permiten estos valores:

Not Started
In Progress
Completed
Ejemplo válido:

{
  "status": "In Progress"
}
Ejemplo inválido:

{
  "status": "Pending"
}
9. Instrucciones de prueba
9.1 Prueba rápida manual
Con la aplicación ejecutándose, abre otra terminal y ejecuta:

curl -i http://localhost:5000/api/health
Después, crea un curso:

curl -i -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Fundamentals",
    "description": "Learn Python from the beginning.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Copia el
id
recibido en la respuesta.

Después consulta todos los cursos:

curl -i http://localhost:5000/api/courses
Consulta el curso individual:

curl -i http://localhost:5000/api/courses/ID_DEL_CURSO
Actualízalo:

curl -i -X PUT http://localhost:5000/api/courses/ID_DEL_CURSO \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Fundamentals Updated",
    "description": "Updated Python course.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }'
Consulta las estadísticas:

curl -i http://localhost:5000/api/courses/stats
Finalmente, elimínalo:

curl -i -X DELETE http://localhost:5000/api/courses/ID_DEL_CURSO
9.2 Pruebas de error
Crear un curso sin nombre
curl -i -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Course without a name.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Esperado:

400 Bad Request
Utilizar un estado inválido
curl -i -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "Example course.",
    "target_date": "2026-12-31",
    "status": "Pending"
  }'
Esperado:

400 Bad Request
Utilizar una fecha inválida
curl -i -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "Example course.",
    "target_date": "31-12-2026",
    "status": "Not Started"
  }'
Esperado:

400 Bad Request
Consultar un curso inexistente
curl -i http://localhost:5000/api/courses/course-does-not-exist
Esperado:

404 Not Found
10. Estructura del proyecto
Una estructura recomendada es:

codecrafthub/
│
├── app.py
├── courses.json
├── requirements.txt
├── README.md
│
└── .gitignore
Descripción de los archivos
app.py
Archivo principal de la aplicación Flask.

Normalmente contiene:

Creación de la aplicación Flask.
Definición de las rutas.
Lectura de
courses.json
.
Escritura de
courses.json
.
Validación de los datos recibidos.
Generación de respuestas JSON.
courses.json
Archivo de persistencia local.

Debe contener siempre una lista JSON:

[]
o:

[
  {
    "id": "course-001",
    "name": "Python Fundamentals",
    "description": "Introduction to Python.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }
]
No debe tener una propiedad contenedora como
courses
:

{
  "courses": []
}
La estructura esperada es directamente una lista.

requirements.txt
Contiene las dependencias de Python necesarias para ejecutar el proyecto.

Ejemplo:

Flask
README.md
Este archivo. Contiene las instrucciones de instalación, ejecución y uso de la API.

.gitignore
Indica qué archivos no deben subirse al control de versiones.

Ejemplo recomendado:

venv/
__pycache__/
*.pyc
.env
Si se desea conservar los datos de ejemplo de
courses.json
, no se debe incluir ese archivo en
.gitignore
.

11. Códigos HTTP utilizados
Código	Significado	Uso en CodeCraftHub
200
OK	Consulta, actualización, eliminación y estadísticas correctas.
201
Created	Curso creado correctamente.
400
Bad Request	Datos inválidos, campos faltantes o formato incorrecto.
404
Not Found	El curso solicitado no existe.
500
Internal Server Error	Error inesperado al ejecutar la aplicación o leer/escribir el archivo.
12. Solución de problemas comunes
12.1 Error:
python
no se reconoce como comando
En Windows puede aparecer:

'python' is not recognized as an internal or external command
Soluciones:

Instala Python desde python.org.
Durante la instalación, activa la opción Add Python to PATH.
Cierra y vuelve a abrir la terminal.
Comprueba la instalación:
python --version
En macOS o Linux prueba:

python3 --version
12.2 Error:
No module named flask
Esto significa que Flask no está instalado en el entorno actual.

Activa el entorno virtual:

# Windows
venv\Scripts\activate

# macOS o Linux
source venv/bin/activate
Después instala Flask:

pip install Flask
12.3 Error: el puerto 5000 ya está en uso
Puedes ejecutar Flask en otro puerto:

flask --app app run --debug --port 5001
Después utiliza:

curl http://localhost:5001/api/health
12.4 Error
404 Not Found
Comprueba:

Que la aplicación esté ejecutándose.
Que la URL esté escrita correctamente.
Que estés usando
/api/courses
y no
/courses
.
Que el identificador del curso exista.
Que la ruta de estadísticas sea
/api/courses/stats
.
12.5 Error
400 Bad Request
Comprueba:

Que el cuerpo sea JSON válido.
Que hayas añadido la cabecera:
Content-Type: application/json
Que el campo
name
esté presente.
Que
target_date
use el formato
YYYY-MM-DD
.
Que
status
sea uno de los valores permitidos.
12.6 Error al leer
courses.json
Comprueba que el archivo:

Exista.
Se encuentre en la ubicación esperada.
Contenga JSON válido.
Comience con
[
y termine con
]
.
No tenga comas adicionales.
Contenido válido:

[]
Contenido inválido:

[
  {
    "id": "course-001",
    "name": "Python"
  },
]
La coma después del último elemento no está permitida en JSON.

12.7 Los cambios no se guardan
Comprueba:

Que la aplicación tenga permisos de escritura sobre
courses.json
.
Que estés consultando el mismo archivo que utiliza la aplicación.
Que la solicitud haya devuelto un código de éxito.
Que
courses.json
no se esté sobrescribiendo manualmente mientras la aplicación está funcionando.
12.8 El endpoint
/api/courses/stats
devuelve curso no encontrado
La ruta de estadísticas debe registrarse antes de la ruta dinámica:

@app.route("/api/courses/stats", methods=["GET"])
def get_stats():
    pass

@app.route("/api/courses/<id>", methods=["GET"])
def get_course(id):
    pass
Si
/api/courses/<id>
se registra primero, el valor
stats
puede interpretarse como un
id
.

13. Resumen de endpoints
Método	Endpoint	Descripción	Éxito
GET
/api/health
Comprueba el estado de la API.	
200
GET
/api/courses
Obtiene todos los cursos.	
200
GET
/api/courses/<id>
Obtiene un curso por ID.	
200
POST
/api/courses
Crea un curso.	
201
PUT
/api/courses/<id>
Actualiza un curso.	
200
DELETE
/api/courses/<id>
Elimina un curso.	
200
GET
/api/courses/stats
Obtiene estadísticas de los cursos.	
200
Flujo básico de uso
1. Iniciar la aplicación Flask.
2. Comprobar /api/health.
3. Crear un curso con POST.
4. Consultar los cursos con GET.
5. Consultar un curso usando su id.
6. Actualizarlo con PUT.
7. Consultar las estadísticas.
8. Eliminarlo con DELETE.
Con estos pasos puedes ejecutar y probar CodeCraftHub incluso si es tu primer proyecto con una API REST.

28.35 seconds