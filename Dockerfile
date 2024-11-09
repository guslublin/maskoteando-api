# Usar una imagen base de Python 3
FROM python:3.9

# Establecer el directorio de trabajo en la imagen
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Exponer el puerto (Django usa por defecto el puerto 8000)
EXPOSE 8000

# Comando para ejecutar migraciones y levantar el servidor
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
