# UCSE-IW-2024

Sistema de gestión para consorcios de edificios desarrollado como trabajo práctico grupal para la materia **Ingeniería Web** de la **Universidad Católica de Santiago del Estero (UCSE)**, edición 2024.

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Módulos de la aplicación](#módulos-de-la-aplicación)
  - [usuarios](#usuarios)
  - [propiedades](#propiedades)
  - [comunicaciones](#comunicaciones)
  - [mensajería](#mensajería)
  - [servicios](#servicios)
  - [denuncias](#denuncias)
- [Endpoints de la API](#endpoints-de-la-api)
- [Requisitos previos](#requisitos-previos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Ejecución con Docker](#ejecución-con-docker)
- [Variables de entorno](#variables-de-entorno)
- [Inicialización de la base de datos](#inicialización-de-la-base-de-datos)
- [Documentación interactiva de la API](#documentación-interactiva-de-la-api)
- [Despliegue en producción](#despliegue-en-producción)

---

## Descripción general

La plataforma permite administrar de forma integral un consorcio de edificios de propiedad horizontal. Sus principales funcionalidades son:

- Registro y autenticación de residentes con roles diferenciados.
- Gestión de edificios y departamentos.
- Muro de comunicaciones comunitario (posteos, respuestas y eventos).
- Sistema de mensajería privada entre usuarios.
- Directorio de servicios y proveedores por edificio.
- Sistema de denuncias sobre contenido inapropiado.

---

## Tecnologías utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12 | Lenguaje principal |
| Django | 4.2.16 | Framework web |
| Django REST Framework | 3.14.0 | API REST |
| drf-spectacular | 0.27.2 | Documentación OpenAPI/Swagger |
| django-haystack + Whoosh | 3.2.1 / 2.7.4 | Motor de búsqueda de texto completo |
| django-storages + boto3 | 1.14.4 / 1.35.9 | Almacenamiento de archivos en AWS S3 |
| django-cors-headers | 4.4.0 | Gestión de CORS |
| django-filter | 24.3 | Filtrado de querysets |
| Whitenoise | 6.7.0 | Servicio de estáticos en producción |
| Gunicorn | 23.0.0 | Servidor WSGI de producción |
| SQLite | — | Base de datos (desarrollo / Docker) |
| PostgreSQL | — | Base de datos (producción en Render) |
| Docker | — | Contenedorización |

---

## Arquitectura del proyecto

```
UCSE-IW-2024/
├── Dockerfile                   # Imagen Docker de la aplicación
├── README.md
└── Backend/
    ├── manage.py
    ├── requirements.txt
    ├── initialize_db.py         # Carga inicial de datos de referencia
    ├── build.sh                 # Script de build para Render.com
    ├── run.sh                   # Script de arranque con Gunicorn
    ├── db.sqlite3               # Base de datos SQLite (desarrollo)
    ├── proyectoPrincipal/       # Configuración central de Django
    │   ├── settings.py
    │   └── urls.py
    ├── usuarios/                # Módulo de usuarios y autenticación
    ├── propiedades/             # Módulo de edificios
    ├── comunicaciones/          # Módulo de posteos y eventos
    ├── mensajeria/              # Módulo de chat privado
    ├── servicios/               # Módulo de proveedores de servicios
    ├── denuncias/               # Módulo de denuncias de contenido
    └── whoosh_index/            # Índice de búsqueda de texto completo
```

---

## Módulos de la aplicación

### usuarios

Gestiona el registro, autenticación y perfil de los usuarios del sistema.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `Rol` | Rol del usuario: `Administrador`, `Colaborador`, `Inquilino`, `Duenio` |
| `User` | Extiende `AbstractUser`. Campos: `email` (identificador), `nombre`, `apellido`, `rol`, `edificio`, `piso`, `numero`. El campo `username` fue reemplazado por `email`. |
| `PasswordResetToken` | Token UUID de un solo uso con expiración de 1 hora para restablecimiento de contraseña. |

**Permisos:**
- `IsOwnerUser`: permite la edición de perfil únicamente al propio usuario autenticado.

---

### propiedades

Gestiona los edificios registrados en el sistema.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `Edificio` | Representa un edificio con `nombre`, `direccion`, `numero` y `ciudad`. |

---

### comunicaciones

Gestiona el muro comunitario del edificio con posteos, respuestas y eventos.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `TipoPosteo` | Categoría del posteo: `Reclamo`, `Consulta`, `Aviso`. |
| `Posteo` | Publicación del muro con `titulo`, `descripcion`, `tipo_posteo`, `imagen` (almacenada en S3) y `fecha_creacion`. |
| `Respuesta` | Respuesta anidada a un `Posteo`. |
| `TipoEvento` | Categoría de evento: `Mantenimiento`, `Limpieza`, `Reformas`, `Reunion de Consorcio`. |
| `Evento` | Evento comunitario con `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin` y `tipo_evento`. Valida que `fecha_fin >= fecha_inicio`. |

El módulo integra **django-haystack** con motor **Whoosh** para búsqueda de texto completo sobre posteos.

---

### mensajería

Gestiona las conversaciones privadas entre usuarios.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `Conversacion` | Canal de chat entre dos o más `participantes` (M2M con `User`). Ordenada por `ultima_actualizacion`. |
| `Mensaje` | Mensaje dentro de una `Conversacion`. Campos: `remitente`, `contenido`, `fecha_envio`, `leido`. |

---

### servicios

Directorio de proveedores de servicios asociados a cada edificio.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `TipoServicio` | Especialidad del proveedor: `Plomeria`, `Gasista`, `Electricista`, `Tecnico en Refrigeracion`, `Cerrajero`, `Pintor`. |
| `Servicio` | Proveedor con `nombre_proveedor`, `telefono`, `tipo` y asociación al `Edificio`. Ordenado por `fecha_creacion` descendente. |

---

### denuncias

Permite a los usuarios reportar contenido inapropiado dentro de su mismo edificio.

**Modelos principales:**

| Modelo | Descripción |
|---|---|
| `Denuncia` | Denuncia realizada por un usuario sobre otro usuario, un posteo o un evento. |

**Tipos de denuncia:** `spam`, `inapropiado`, `ofensivo`, `acoso`.

**Estados posibles:** `pendiente` → `en_revision` → `resuelta` / `desestimada`.

**Validaciones:**
- Debe especificarse exactamente **un** elemento denunciado (usuario, posteo o evento).
- El denunciante y el contenido denunciado deben pertenecer al **mismo edificio**.

---

## Endpoints de la API

Todos los endpoints llevan el prefijo base del servidor (p. ej. `http://localhost:8000`).

### Autenticación (`/auth/`)

| Método | Ruta | Descripción | Autenticación |
|---|---|---|---|
| `POST` | `/auth/registro/` | Registrar nuevo usuario | No requerida |
| `POST` | `/auth/login/` | Iniciar sesión, devuelve token | No requerida |
| `POST` | `/auth/logout/` | Cerrar sesión, invalida token | Token |
| `POST` | `/auth/request-password-reset/` | Solicitar restablecimiento de contraseña | No requerida |
| `POST` | `/auth/reset-password/` | Confirmar nueva contraseña con token | No requerida |
| `GET` | `/auth/usuarios/` | Listar usuarios | No requerida |
| `GET/PUT/PATCH/DELETE` | `/auth/usuarios/{id}/` | CRUD sobre un usuario | Token (propio usuario) |

### Propiedades (`/propiedades/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET/POST` | `/propiedades/edificios/` | Listar / crear edificios |
| `GET/PUT/PATCH/DELETE` | `/propiedades/edificios/{id}/` | Detalle / editar / eliminar edificio |

### Comunicaciones (`/comunicaciones/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET/POST` | `/comunicaciones/posteos/` | Listar / crear posteos |
| `GET/PUT/PATCH/DELETE` | `/comunicaciones/posteos/{id}/` | Detalle / editar / eliminar posteo |
| `GET/POST` | `/comunicaciones/posteos/{id}/respuestas/` | Listar / crear respuestas |
| `GET/PUT/PATCH/DELETE` | `/comunicaciones/posteos/{id}/respuestas/{rid}/` | Detalle / editar / eliminar respuesta |
| `GET` | `/comunicaciones/tipos-posteo/` | Listar tipos de posteo |
| `GET/POST` | `/comunicaciones/eventos/` | Listar / crear eventos |
| `GET/PUT/PATCH/DELETE` | `/comunicaciones/eventos/{id}/` | Detalle / editar / eliminar evento |
| `GET` | `/comunicaciones/search/?q={texto}` | Búsqueda de texto completo en posteos |

### Mensajería (`/mensajeria/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET/POST` | `/mensajeria/conversaciones/` | Listar / crear conversaciones |
| `GET/PUT/PATCH/DELETE` | `/mensajeria/conversaciones/{id}/` | Detalle de conversación y mensajes |

### Servicios (`/servicios/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/servicios/tipos/` | Listar tipos de servicio |
| `GET/POST` | `/servicios/` | Listar / crear servicios del edificio |
| `GET/PUT/PATCH/DELETE` | `/servicios/{id}/` | Detalle / editar / eliminar servicio |

### Denuncias (`/denuncias/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET/POST` | `/denuncias/denuncias/` | Listar / crear denuncias |
| `GET/PUT/PATCH/DELETE` | `/denuncias/denuncias/{id}/` | Detalle / editar / eliminar denuncia |

---

## Requisitos previos

- Python 3.12+
- pip
- (Opcional) Docker y Docker Compose
- (Opcional) Cuenta de AWS S3 para almacenamiento de imágenes

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/NachoRossi46/UCSE-IW-2024.git
cd UCSE-IW-2024/Backend

# 2. Crear y activar entorno virtual
python -m venv entorno
# Windows
entorno\Scripts\activate
# Linux / macOS
source entorno/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo .env (ver sección Variables de entorno)

# 5. Aplicar migraciones
python manage.py migrate

# 6. Cargar datos iniciales de referencia
python initialize_db.py

# 7. Crear superusuario (opcional)
python manage.py createsuperuser

# 8. Construir el índice de búsqueda
python manage.py rebuild_index

# 9. Iniciar el servidor de desarrollo
python manage.py runserver
```

La API quedará disponible en `http://localhost:8000`.

---

## Ejecución con Docker

```bash
# Desde la raíz del repositorio
docker build -t ucse-iw-2024 .
docker run -p 8000:8000 -v ucse_data:/data ucse-iw-2024
```

- La base de datos SQLite se persiste en el volumen `/data`.
- Las migraciones se ejecutan automáticamente al arrancar el contenedor.
- El servidor escucha en `0.0.0.0:8000`.

---

## Variables de entorno

Crear un archivo `.env` dentro de `Backend/` con las siguientes variables:

```env
# Clave secreta de Django
SECRET_KEY=<clave_secreta_segura>

# Configuración de correo (Gmail SMTP)
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contrasena_de_aplicacion

# Configuración de AWS S3 (para almacenamiento de imágenes)
AWS_ACCESS_KEY_ID=<access_key>
AWS_SECRET_ACCESS_KEY=<secret_key>
AWS_STORAGE_BUCKET_NAME=<nombre_del_bucket>

# Solo en entorno Docker
DOCKER=True
```

> **Nota:** En producción sobre Render.com, las variables se configuran directamente en el panel del servicio. No incluir el archivo `.env` en el repositorio.

---

## Inicialización de la base de datos

El script `initialize_db.py` crea los datos de referencia necesarios para que la aplicación funcione correctamente:

| Entidad | Valores creados |
|---|---|
| `Rol` | Administrador, Colaborador, Inquilino, Duenio |
| `TipoPosteo` | Aviso, Consulta, Reclamo |
| `TipoEvento` | Mantenimiento, Limpieza, Reformas, Reunion de Consorcio |
| `TipoServicio` | Plomería, Gasista, Electricista, Técnico en Refrigeración, Cerrajero, Pintor |

```bash
python initialize_db.py
```

---

## Documentación interactiva de la API

El proyecto genera automáticamente la documentación OpenAPI mediante **drf-spectacular**.

| Interfaz | URL |
|---|---|
| Esquema OpenAPI (JSON/YAML) | `/api/schema/` |
| Swagger UI | `/api/docs/` |
| ReDoc | `/api/redoc/` |

La autenticación en Swagger UI se realiza mediante header `Authorization: Token <tu_token>`.

---

## Despliegue en producción

El proyecto está configurado para desplegarse en **[Render.com](https://render.com)** con base de datos **PostgreSQL**.

### Scripts de despliegue

- **`build.sh`**: instala dependencias, recopila archivos estáticos, aplica migraciones, inicializa la base de datos y reconstruye el índice de búsqueda.
- **`run.sh`**: inicia el servidor con **Gunicorn**.

### URLs de producción

| Servicio | URL |
|---|---|
| API (backend) | `https://ucse-iw-2024.onrender.com` |
| Frontend | `https://iw-front.vercel.app` |

### Consideraciones de producción

- `DEBUG = False` se activa automáticamente al detectar la variable de entorno `RENDER`.
- Los archivos estáticos son servidos por **Whitenoise**.
- Los archivos de media (imágenes) son almacenados en **AWS S3**.
- Se habilita `CSRF_TRUSTED_ORIGINS` para el dominio del frontend.
- El índice de búsqueda Whoosh se almacena en `/opt/render/project/src/whoosh_index`.
