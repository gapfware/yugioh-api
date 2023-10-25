## Yu-Gi-Oh! API

Desarrollo de una plataforma de juegos de cartas en línea que se centra en Yu-Gi-
Oh!. Se utilizó para el desarrollo FastAPI como framework y SQLAlchemy como ORM, así como también el patrón MVC para la construcción de las APIs REST


## Índice

- [Instalacion](#instalacion)
- [Descripcion](#descripcion)
- [Reglas](#reglas)


## Instalacion
1. Desde cero: 
### Crear entorno virtual
```
bash
python3 -m venv venv
```
### Activar entorno virtual
```
bash
source venv/bin/activate
```
### Instalar requerimientos
```
bash
pip install -r requirements.txt
```
### Crear base de datos 
Desde la terminal
```
mysql -u <tu_usuario> -p
```
```
CREATE DATABASE yugioh;
```

## Crear archivo .env en el directorio principal
```
DB_USER= your_db_user
DB_PASSWORD= db_password
DB_HOST= your_db_host
DB_PORT= db_port
DB_NAME=yugioh
```

## Ejecutar la aplicacion desde el directorio raiz
```
uvicorn app.main:app
```
## 2. Instalacion mediante docker

```
docker-compose up
```
Nota: Si en un principio no funciona, interrumpir la ejecucion y ejecutarlo nuevamente

## Descripcion

- API RESTful que permite a los usuarios crear, ver, actualizar y eliminar cartas de Yu-Gi-Oh!.

- API RESTful que permite ver, crear, actualizar y eliminar usuarios

- API RESTful que permite a los usuarios crear, ver y actualizar mazos de cartas de Yu-Gi-Oh!. Para crear un mazo es necesario previamente crear un usuario, ya que estos estan relacionados directamente

- Se podran asociar directamente cartas a los mazos, asi como eliminar cartas de los mazos.

## Reglas

- Para crear un mazo previamente se debe crear un usuario, ya que estaran asociados
- Cada mazo puede tener un maximo de 60 cartas
- Cada carta puede aparecer una sola vez por mazo
- Una vez creada una carta, no se le podra modificar su tipo
- Solo se pueden crear cartas de tipo: monster, spell y/o trap
- Solo las cartas de tipo monster tienen poder de ataque y poder de defensa
- Al insertar una imagen de una carta debera ser un link valido

## Persistencia de datos

Para el proyecto se utilizó MySQL como motor de base de datos
