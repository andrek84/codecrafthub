Casos de prueba para la API de CodeCraftHub
Se asume que la API está ejecutándose localmente en:

http://localhost:5000
Si utiliza otro puerto o servidor, sustituya la variable
BASE_URL
.

BASE_URL="http://localhost:5000"
Modelo de curso utilizado
{
  "id": "course-001",
  "name": "Python Fundamentals",
  "description": "Introduction to Python programming.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Valores válidos para
status
:

Not Started
In Progress
Completed
El campo
target_date
debe utilizar el formato:

YYYY-MM-DD
1. Comprobación de salud de la API
Solicitud
curl -i "$BASE_URL/api/health"
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "ok"
  }
}
2. Obtener todos los cursos
Solicitud
curl -i "$BASE_URL/api/courses"
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

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
Si no existen cursos, la respuesta puede ser:

{
  "success": true,
  "message": "Courses retrieved successfully",
  "data": []
}
3. Crear un curso correctamente
Carga útil JSON
{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-11-30",
  "status": "Not Started"
}
Solicitud
POST
curl -i -X POST "$BASE_URL/api/courses" \
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
Respuesta JSON:

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
El valor de
id
será generado por el servidor. Para los siguientes ejemplos se utilizará
course-002
.

4. Obtener un curso por su identificador
Solicitud
curl -i "$BASE_URL/api/courses/course-002"
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

{
  "success": true,
  "message": "Course retrieved successfully",
  "data": {
    "id": "course-002",
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs with Flask.",
    "target_date": "2026-11-30",
    "status": "Not Started"
  }
}
5. Actualizar un curso correctamente
Carga útil JSON para
PUT
El cuerpo de
PUT
debe incluir los campos editables completos del curso:

{
  "name": "Flask REST APIs - Updated",
  "description": "Build and maintain REST APIs using Flask.",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
Solicitud
PUT
curl -i -X PUT "$BASE_URL/api/courses/course-002" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs - Updated",
    "description": "Build and maintain REST APIs using Flask.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }'
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

{
  "success": true,
  "message": "Course updated successfully",
  "data": {
    "id": "course-002",
    "name": "Flask REST APIs - Updated",
    "description": "Build and maintain REST APIs using Flask.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }
}
El campo
id
debe conservarse y no debe modificarse mediante la carga útil.

6. Obtener estadísticas de cursos
Solicitud
curl -i "$BASE_URL/api/courses/stats"
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

{
  "success": true,
  "message": "Course statistics retrieved successfully",
  "data": {
    "total_courses": 2,
    "by_status": {
      "Not Started": 1,
      "In Progress": 1,
      "Completed": 0
    }
  }
}
La ruta específica de estadísticas es
/api/courses/stats
. Debe evaluarse antes que la ruta dinámica
/api/courses/<id>
para evitar que
stats
se interprete como un identificador.

7. Eliminar un curso
Solicitud
curl -i -X DELETE "$BASE_URL/api/courses/course-002"
Respuesta esperada
Código HTTP:

200 OK
Respuesta JSON:

{
  "success": true,
  "message": "Course deleted successfully",
  "data": {
    "id": "course-002"
  }
}
Después de esta operación, una consulta del mismo curso debe devolver
404 Not Found
.

Casos de error
8. Crear un curso sin campos requeridos
Los campos requeridos son:

name
target_date
status
En este ejemplo faltan
name
y
target_date
.

Si el requisito exacto del proyecto considera únicamente
name
como obligatorio, elimine
target_date
de esta validación. El caso se muestra siguiendo el modelo completo solicitado.

Solicitud
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Course without required fields",
    "status": "Not Started"
  }'
Respuesta esperada
Código HTTP:

400 Bad Request
Respuesta JSON:

{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "The name field is required",
    "The target_date field is required"
  ]
}
9. Crear un curso con
status
inválido
Solicitud
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "This course contains an invalid status.",
    "target_date": "2026-12-31",
    "status": "Pending"
  }'
Respuesta esperada
Código HTTP:

400 Bad Request
Respuesta JSON:

{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "The status must be one of: Not Started, In Progress, Completed"
  ]
}
10. Crear un curso con formato de fecha inválido
Solicitud
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "This course contains an invalid date.",
    "target_date": "31-12-2026",
    "status": "Not Started"
  }'
Respuesta esperada
Código HTTP:

400 Bad Request
Respuesta JSON:

{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "The target_date must use the YYYY-MM-DD format"
  ]
}
Otro ejemplo de fecha imposible
Aunque tenga la apariencia
YYYY-MM-DD
, esta fecha no es válida:

curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Impossible Date Course",
    "description": "This course contains an impossible date.",
    "target_date": "2026-02-30",
    "status": "Not Started"
  }'
Respuesta esperada:

400 Bad Request
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "The target_date is not a valid calendar date"
  ]
}
11. Actualizar un curso inexistente
Solicitud
curl -i -X PUT "$BASE_URL/api/courses/course-999999" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nonexistent Course",
    "description": "This course does not exist.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Respuesta esperada
Código HTTP:

404 Not Found
Respuesta JSON:

{
  "success": false,
  "message": "Course not found",
  "errors": [
    "No course exists with id course-999999"
  ]
}
12. Consultar un curso inexistente
Solicitud
curl -i "$BASE_URL/api/courses/course-999999"
Respuesta esperada
Código HTTP:

404 Not Found
Respuesta JSON:

{
  "success": false,
  "message": "Course not found",
  "errors": [
    "No course exists with id course-999999"
  ]
}
13. Eliminar un curso inexistente
Solicitud
curl -i -X DELETE "$BASE_URL/api/courses/course-999999"
Respuesta esperada
Código HTTP:

404 Not Found
Respuesta JSON:

{
  "success": false,
  "message": "Course not found",
  "errors": [
    "No course exists with id course-999999"
  ]
}
Resumen de códigos HTTP esperados
Operación	Éxito	Errores principales
GET /api/health
200
500
GET /api/courses
200
500
GET /api/courses/<id>
200
404
,
500
POST /api/courses
201
400
,
500
PUT /api/courses/<id>
200
400
,
404
,
500
DELETE /api/courses/<id>
200
404
,
500
GET /api/courses/stats
200
500
Secuencia recomendada para principiantes
Ejecute los comandos en este orden:

# 1. Definir la URL base
BASE_URL="http://localhost:5000"

# 2. Comprobar la API
curl -i "$BASE_URL/api/health"

# 3. Crear un curso
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs with Flask.",
    "target_date": "2026-11-30",
    "status": "Not Started"
  }'

# 4. Listar cursos
curl -i "$BASE_URL/api/courses"

# 5. Consultar estadísticas
curl -i "$BASE_URL/api/courses/stats"

# 6. Consultar, actualizar y eliminar el ID devuelto por el POST
curl -i "$BASE_URL/api/courses/course-002"