# Usa una imagen base de Python
FROM python:3.12-slim

# Configura la variable de entorno para la base de datos
ENV DATABASE_PATH=/data/db.sqlite3

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación
COPY . /app

RUN pip install --no-cache-dir setuptools
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crea el directorio para la base de datos
RUN mkdir -p /data

# Define el volumen para persistencia de datos
VOLUME ["/data"]

# Expone el puerto 8000
EXPOSE 8000

# Configura el comando de inicio del servidor y las migraciones
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
