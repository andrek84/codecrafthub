# Requisitos - CodeCraftHub

## 1. Requisitos funcionales

RF-01  La API debe permitir crear un curso mediante POST /api/courses.
RF-02  La API debe permitir consultar todos los cursos mediante GET /api/courses.
RF-03  La API debe permitir consultar un curso por su id mediante GET /api/courses/<id>.
RF-04  La API debe permitir actualizar un curso mediante PUT /api/courses/<id>.
RF-05  La API debe permitir eliminar un curso mediante DELETE /api/courses/<id>.
RF-06  La API debe ofrecer estadisticas mediante GET /api/courses/stats.
RF-07  El id de cada curso se genera automaticamente y comienza en 1.
RF-08  El sistema debe validar los campos obligatorios antes de crear o actualizar.
RF-09  El campo status solo acepta: Not Started, In Progress, Completed.
RF-10  El campo target_date debe tener el formato YYYY-MM-DD.
RF-11  Los cursos se persisten en el archivo local courses.json.
RF-12  Si courses.json no existe, el sistema lo crea automaticamente vacio.
RF-13  Los datos deben conservarse despues de reiniciar la aplicacion.
RF-14  Al actualizar un curso se registra su fecha de actualizacion (updated_at).
RF-15  Al eliminar un curso, este no debe aparecer en consultas posteriores.

## 2. Requisitos no funcionales

RNF-01  El backend se implementa en Python con el framework Flask.
RNF-02  No se utiliza base de datos; la persistencia es en archivo JSON.
RNF-03  No se requiere autenticacion ni gestion de usuarios.
RNF-04  Todas las respuestas se devuelven en formato JSON.
RNF-05  Las respuestas siguen una estructura uniforme en todos los endpoints.
RNF-06  Se utilizan codigos de estado HTTP adecuados (200, 201, 400, 404, 405, 500).
RNF-07  Los mensajes de error indican con claridad el campo y el motivo del fallo.
RNF-08  El archivo se almacena con codificacion UTF-8.
RNF-09  Se habilita CORS para permitir el consumo desde un panel web en el navegador.
RNF-10  El codigo incluye comentarios explicativos para principiantes.

## 3. Modelo de datos

Campo         Tipo     Obligatorio  Por defecto  Reglas
------------  -------  -----------  -----------  ------------------------------------------
id            entero   Generado     -            Autoincremental, comienza en 1
name          texto    Si           -            No puede estar vacio
description   texto    Si           -            No puede estar vacio
target_date   texto    Si           -            Formato YYYY-MM-DD
status        texto    Si           -            Not Started | In Progress | Completed
created_at    texto    Generado     Fecha actual  Se asigna al crear, no se modifica
updated_at    texto    Generado     -            Se actualiza en cada modificacion

Ejemplo de curso:

{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-09-13 06:26:54"
}

## 4. Endpoints

Metodo  Ruta                   Descripcion                    Exito  Errores
------  ---------------------  -----------------------------  -----  -------------
POST    /api/courses           Crea un curso nuevo            201    400, 500
GET     /api/courses           Lista todos los cursos         200    500
GET     /api/courses/<id>      Obtiene un curso por su id     200    404, 500
PUT     /api/courses/<id>      Actualiza un curso existente   200    400, 404, 500
DELETE  /api/courses/<id>      Elimina un curso               200    404, 500
GET     /api/courses/stats     Estadisticas del catalogo      200    500

## 5. Estructura de las respuestas

Exito:
{
  "success": true,
  "message": "Curso creado correctamente",
  "data": { }
}

Error:
{
  "success": false,
  "message": "Datos invalidos.",
  "errors": ["El campo 'name' es obligatorio y no puede estar vacio."]
}