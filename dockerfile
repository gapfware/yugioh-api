# Usamos la imagen base oficial de Python 3.10
FROM python:3.10

# Configura el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia todo el contenido de tu aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará tu aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
