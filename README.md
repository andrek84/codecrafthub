# CodeCraftHub

Plataforma de aprendizaje personalizada que permite a los desarrolladores llevar el control de los cursos que desean aprender.

Proyecto Final Parte 1 — Opción B (Python + Flask).

---

## 1. Visión general

CodeCraftHub es una API REST que funciona como un **rastreador personal de cursos**. Un desarrollador puede registrar los cursos que quiere estudiar, fijarles una fecha objetivo y actualizar su estado a medida que avanza.

Está construida con **Python** y el framework **Flask**. Los datos se guardan en un archivo de texto JSON local llamado `courses.json`, sin necesidad de base de datos ni sistema de autenticación.

---

## 2. Características

- API REST completa con las cuatro operaciones CRUD (crear, leer, actualizar, eliminar)
- Almacenamiento sencillo en archivo JSON, que se crea automáticamente al primer uso
- Identificadores numéricos generados automáticamente a partir del 1
- Validación de todos los campos obligatorios, del formato de fecha y de los estados permitidos
- Mensajes de error claros y códigos de estado HTTP correctos
- Respuestas JSON con una estructura uniforme en todos los endpoints
- CORS habilitado, para que un panel web pueda consumir la API desde el navegador
- Endpoint adicional de estadísticas

---

## 3. Requisitos previos

| Herramienta | Versión mínima | Cómo verificar |
|---|---|---|
| Python | 3.8 | `python --version` |
| pip | cualquiera | `pip --version` |
| curl | cualquiera | `curl.exe --version` |

---

## 4. Instalación

**Paso 1.** Crea la carpeta del proyecto y entra en ella:

```bash
mkdir codecrafthub
cd codecrafthub
```

**Paso 2.** Coloca dentro los archivos `app.py` y `requirements.txt`.

**Paso 3.** Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 5. Cómo ejecutar la aplicación

```bash
python app.py
```

Verás una salida similar a:

```
- CodeCraftHub API is starting...
- Data will be stored in: C:\...\codecrafthub\courses.json
- API will be available at: http://localhost:5000
```

La API queda disponible en `http://localhost:5000`. Para detener el servidor, presiona `Ctrl + C`.

> La ventana de terminal queda ocupada mientras el servidor está corriendo. Para hacer pruebas necesitas abrir **una segunda ventana**.

---

## 6. Modelo de datos

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | entero | Generado | Identificador único, empieza en 1 |
| `name` | texto | **Sí** | Nombre del curso |
| `description` | texto | **Sí** | Descripción del curso |
| `target_date` | texto | **Sí** | Fecha objetivo, formato `YYYY-MM-DD` |
| `status` | texto | **Sí** | `Not Started`, `In Progress` o `Completed` |
| `created_at` | texto | Generado | Fecha y hora de creación |
| `updated_at` | texto | Generado | Fecha y hora de la última modificación |

---

## 7. Formato de las respuestas

**Éxito:**

```json
{
  "success": true,
  "message": "Curso creado correctamente",
  "data": { }
}
```

**Error:**

```json
{
  "success": false,
  "message": "Datos invalidos.",
  "errors": ["El campo 'name' es obligatorio y no puede estar vacio."]
}
```

---

## 8. Endpoints de la API

| Método | Ruta | Descripción | Éxito | Errores |
|---|---|---|---|---|
| POST | `/api/courses` | Agrega un nuevo curso | 201 | 400, 500 |
| GET | `/api/courses` | Obtiene todos los cursos | 200 | 500 |
| GET | `/api/courses/<id>` | Obtiene un curso específico | 200 | 404, 500 |
| PUT | `/api/courses/<id>` | Actualiza un curso | 200 | 400, 404, 500 |
| DELETE | `/api/courses/<id>` | Elimina un curso | 200 | 404, 500 |
| GET | `/api/courses/stats` | Estadísticas del catálogo | 200 | 500 |

### Ejemplos

**Crear un curso**

```bash
curl -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Python Basics\",\"description\":\"Learn Python fundamentals\",\"target_date\":\"2026-12-31\",\"status\":\"Not Started\"}"
```

Respuesta `201 Created`:

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

**Obtener todos los cursos**

```bash
curl http://localhost:5000/api/courses
```

**Actualizar un curso**

```bash
curl -X PUT http://localhost:5000/api/courses/1 -H "Content-Type: application/json" -d "{\"status\":\"In Progress\"}"
```

**Eliminar un curso**

```bash
curl -X DELETE http://localhost:5000/api/courses/1
```

**Estadísticas**

```bash
curl http://localhost:5000/api/courses/stats
```

Respuesta `200 OK`:

```json
{
  "success": true,
  "message": "Estadisticas generadas correctamente",
  "data": {
    "total_courses": 2,
    "by_status": {
      "Not Started": 1,
      "In Progress": 1,
      "Completed": 0
    }
  }
}
```

---

## 9. Instrucciones de prueba

Con el servidor corriendo en una ventana, abre una segunda ventana de terminal y ejecuta las pruebas de la sección anterior. Verifica que:

- Crear un curso devuelve **201** y un `id` que empieza en 1
- Enviar datos incompletos devuelve **400** con la lista de errores
- Consultar un `id` inexistente devuelve **404**
- Actualizar devuelve **200** y agrega el campo `updated_at`
- Eliminar devuelve **200**, y **404** si se repite
- El archivo `courses.json` conserva los datos al reiniciar el servidor

---

## 10. Solución de problemas

| Problema | Causa | Solución |
|---|---|---|
| `Address already in use` | El puerto 5000 ya está ocupado | Cierra el servidor anterior, o cambia el puerto en la última línea de `app.py` |
| `ModuleNotFoundError: flask` | Faltan las dependencias | Ejecuta `pip install -r requirements.txt` |
| `curl: (7) Failed to connect` | El servidor no está corriendo | Vuelve a la primera ventana y ejecuta `python app.py` |
| HTTP 400 en todos los POST | Comillas mal escapadas | En Windows usa comillas dobles escapadas con `\"` dentro del `-d` |
| En PowerShell `curl` no responde bien | `curl` es un alias de otro comando | Usa `curl.exe` en lugar de `curl` |
| `courses.json` no aparece | Aún no se ha creado ningún curso | Se genera automáticamente al arrancar o con el primer POST |

---

## 11. Estructura del proyecto

```
codecrafthub/
├── app.py             # Aplicación Flask con todos los endpoints
├── courses.json       # Almacenamiento de datos (se crea automáticamente)
├── requirements.txt   # Dependencias del proyecto
├── requisitos.md      # Requisitos recopilados con GenAI
├── pruebas.md         # Casos de prueba con curl
└── README.md          # Este archivo
```

**Qué hace cada parte de `app.py`:**

1. **Configuración** — crea la aplicación Flask, activa CORS y define la ruta del archivo de datos
2. **Funciones auxiliares** — `load_courses()`, `save_courses()`, `get_next_id()` y `find_course()` manejan la lectura y escritura del JSON
3. **Respuestas uniformes** — `respuesta_ok()` y `respuesta_error()` garantizan el mismo formato en toda la API
4. **Validación** — `validar_curso()` revisa campos obligatorios, formato de fecha y estados permitidos
5. **Endpoints** — las seis rutas de la API
6. **Manejo de errores** — respuestas JSON para los errores 404, 405 y 500
7. **Arranque** — inicia el servidor en el puerto 5000

---

## Licencia

Proyecto académico con fines educativos.
