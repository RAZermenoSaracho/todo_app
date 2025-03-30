# To Do App (Tkinter + PostgreSQL)

Aplicación de lista de tareas con interfaz gráfica construida en Python usando Tkinter y una base de datos PostgreSQL. Permite agregar, eliminar y marcar tareas como completadas.

---

## Características

- Interfaz sencilla e intuitiva con Tkinter
- Conexión a base de datos PostgreSQL
- Persistencia de datos
- Separación clara entre GUI, lógica y base de datos

---

## Requisitos

- Python 3.8 o superior
- PostgreSQL instalado y funcionando

---

## Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/tuusuario/todo_app.git
cd todo_app
```

2. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

3. **Configura la conexión a tu base de datos**

Copia el archivo de configuración de ejemplo:

```bash
cp config/config_example.json config/config.json
```

Edita `config/config.json` con los datos de acceso a tu base de datos PostgreSQL:

```json
{
  "DB_NAME": "todo_app_db",
  "DB_USER": "tu_usuario",
  "DB_PASSWORD": "tu_contraseña",
  "DB_HOST": "localhost",
  "DB_PORT": 5432
}
```

4. **Crea la base de datos en PostgreSQL** (opcional, el sistema puede crearla por ti).

---

## Inicialización del proyecto

Antes de ejecutar la aplicación por primera vez, asegúrate de que la base de datos y la tabla estén listas:

```bash
python __init__.py
```

Este script:
- Verifica si la base de datos existe y la crea si no está presente.
- Crea la tabla `tasks` en la base de datos si no existe.

---

## Ejecución

```bash
python main.py
```

Al iniciarse la aplicación, se conectará a la base de datos `todo_app_db` y mostrará la ventana principal.

---

## Estructura del proyecto

```
todo_app/
│
├── main.py                   # Punto de entrada
├── __init__.py               # Inicializador de base de datos y tabla
├── requirements.txt
├── config/
│   ├── config.json           # Archivo de configuración de conexión (privado)
│   └── config_example.json   # Archivo de ejemplo
├── db/
│   └── connection.py         # Conexión a PostgreSQL
├── models/
│   └── task.py               # Modelo de datos
├── gui/
│   └── app_window.py         # Interfaz gráfica
```

---

## Licencia

Este proyecto es de código abierto y puedes modificarlo libremente según tus necesidades.

---
