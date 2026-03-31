# Nicolás Píriz - Eduvaluer Prueba Técnica

API REST de transferencias de futbol desarrollada con Django REST Framework y PostgreSQL.

## Requisitos previos

- [Docker](https://www.docker.com/) y Docker Compose instalados

## Correr el proyecto localmente

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd nicolas_piriz_eduvaluer_prueba_tecnica
```

2. Copiar el archivo de variables de entorno:

```bash
cp .env.example .env
```

3. Levantar los contenedores con Docker Compose:

```bash
docker-compose up --build
```

Esto levanta automáticamente:
- Una base de datos **PostgreSQL 16**
- La aplicación **Django** en el puerto `8000`
- Ejecuta las migraciones y carga datos de prueba (seed)

4. La API estará disponible en: `http://localhost:8000`

## Probar la API con Postman

El repositorio incluye el archivo `postman_collection.json` con todos los endpoints listos para probar.

Para importarlo:

1. Abrir **Postman**
2. Ir a **File > Import**
3. Seleccionar el archivo `postman_collection.json` de la raíz del proyecto
4. Los endpoints quedarán disponibles para ejecutar directamente

## Detener el proyecto

```bash
docker-compose down
```

Para eliminar también los datos de la base de datos:

```bash
docker-compose down -v
```
