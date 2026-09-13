# Casos de prueba — CodeCraftHub API

Comandos listos para copiar y pegar. Antes de empezar, asegúrate de que el servidor esté corriendo (`python app.py`) en **otra** ventana de terminal.

> **Windows / PowerShell:** usa `curl.exe` en lugar de `curl`, y escribe todo el comando **en una sola línea**.
> **Linux / Mac / Git Bash:** puedes usar `curl` normal.

La opción `-i` muestra los encabezados de la respuesta, incluido el código de estado HTTP.

---

## Prueba 1 — Crear un curso (POST) ✅

```
curl.exe -i -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Python Basics\",\"description\":\"Learn Python fundamentals\",\"target_date\":\"2026-12-31\",\"status\":\"Not Started\"}"
```

**Esperado: HTTP 201 Created**

```json
{
  "success": true,
  "message": "Curso creado correctamente",
  "data": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-09-13 11:16:36"
  }
}
```

---

## Prueba 2 — Crear un segundo curso (POST) ✅

```
curl.exe -i -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Flask REST APIs\",\"description\":\"Build APIs with Flask\",\"target_date\":\"2027-03-15\",\"status\":\"In Progress\"}"
```

**Esperado: HTTP 201 Created**, con `"id": 2`.

---

## Prueba 3 — Obtener todos los cursos (GET) ✅

```
curl.exe -i http://localhost:5000/api/courses
```

**Esperado: HTTP 200 OK**, con los dos cursos dentro del arreglo `data`.

---

## Prueba 4 — Obtener un curso específico (GET) ✅

```
curl.exe -i http://localhost:5000/api/courses/1
```

**Esperado: HTTP 200 OK**, con el curso de id 1.

---

## Prueba 5 — Actualizar un curso (PUT) ✅

```
curl.exe -i -X PUT http://localhost:5000/api/courses/1 -H "Content-Type: application/json" -d "{\"status\":\"In Progress\"}"
```

**Esperado: HTTP 200 OK**. El `status` cambia y aparece un campo nuevo `updated_at`.

---

## Prueba 6 — Estadísticas (GET) ✅

```
curl.exe -i http://localhost:5000/api/courses/stats
```

**Esperado: HTTP 200 OK**

```json
{
  "success": true,
  "message": "Estadisticas generadas correctamente",
  "data": {
    "total_courses": 2,
    "by_status": {
      "Not Started": 0,
      "In Progress": 2,
      "Completed": 0
    }
  }
}
```

---

## Prueba 7 — Campos obligatorios faltantes ❌

```
curl.exe -i -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Solo nombre\"}"
```

**Esperado: HTTP 400 Bad Request**, con tres errores: faltan `description`, `target_date` y `status`.

---

## Prueba 8 — Estado inválido ❌

```
curl.exe -i -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Curso X\",\"description\":\"Prueba\",\"target_date\":\"2026-01-01\",\"status\":\"Terminado\"}"
```

**Esperado: HTTP 400 Bad Request**. `"Terminado"` no está entre los valores permitidos.

---

## Prueba 9 — Formato de fecha inválido ❌

```
curl.exe -i -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Curso Y\",\"description\":\"Prueba\",\"target_date\":\"31/12/2026\",\"status\":\"Completed\"}"
```

**Esperado: HTTP 400 Bad Request**. La fecha debe ir en formato `YYYY-MM-DD`.

---

## Prueba 10 — Curso no encontrado (GET) ❌

```
curl.exe -i http://localhost:5000/api/courses/999
```

**Esperado: HTTP 404 Not Found**

```json
{
  "success": false,
  "message": "No existe un curso con id 999.",
  "errors": []
}
```

---

## Prueba 11 — Actualizar un curso inexistente (PUT) ❌

```
curl.exe -i -X PUT http://localhost:5000/api/courses/999 -H "Content-Type: application/json" -d "{\"status\":\"Completed\"}"
```

**Esperado: HTTP 404 Not Found**

---

## Prueba 12 — Verificar CORS ✅

```
curl.exe -i -H "Origin: http://localhost:3000" http://localhost:5000/api/courses
```

**Esperado: HTTP 200 OK**, y entre los encabezados debe aparecer la línea:

```
Access-Control-Allow-Origin: http://localhost:3000
```

Si esta línea no aparece, el panel web de la Parte 2 no podrá conectarse a la API.

---

## Prueba 13 — Eliminar un curso (DELETE) ✅

```
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
```

**Esperado: HTTP 200 OK**

```json
{
  "success": true,
  "message": "Curso eliminado correctamente",
  "data": { "id": 1 }
}
```

---

## Prueba 14 — Eliminar el mismo curso otra vez ❌

```
curl.exe -i -X DELETE http://localhost:5000/api/courses/1
```

**Esperado: HTTP 404 Not Found**, porque el curso ya no existe.

---

## Prueba 15 — Persistencia de los datos ✅

```
type courses.json
```

(en Linux o Mac: `cat courses.json`)

**Esperado:** el archivo contiene los cursos que quedaron después de las pruebas. Si detienes el servidor con `Ctrl + C` y lo vuelves a arrancar, los datos siguen ahí.

---

## Resumen de resultados

| # | Prueba | Código esperado | Resultado |
|---|---|---|---|
| 1 | Crear curso | 201 | ☐ |
| 2 | Crear segundo curso | 201 | ☐ |
| 3 | Listar cursos | 200 | ☐ |
| 4 | Obtener curso por id | 200 | ☐ |
| 5 | Actualizar curso | 200 | ☐ |
| 6 | Estadísticas | 200 | ☐ |
| 7 | Campos faltantes | 400 | ☐ |
| 8 | Estado inválido | 400 | ☐ |
| 9 | Fecha inválida | 400 | ☐ |
| 10 | Curso no encontrado | 404 | ☐ |
| 11 | Actualizar inexistente | 404 | ☐ |
| 12 | CORS habilitado | 200 + header | ☐ |
| 13 | Eliminar curso | 200 | ☐ |
| 14 | Eliminar repetido | 404 | ☐ |
| 15 | Persistencia | — | ☐ |
