# Segundo parcial - Arq Web
Backend desarrollado para la materia Arquitectura Web
de la Facultad Politecnica de la
Universidad Nacional de Asunción

## Requisitos para correr el proyecto
- Docker
- Docker-compose

## Como correr el proyecto por primera vez

1. docker-compose build
2. docker-compose up -d django
3. docker-compose exec django python manage.py migrate
4. docker-compose stop
5. docker-compose up

## Servicios que corren

- Backend en django -> http://localhost:8000
- Flower (visualizar task periodicas) -> http://localhost:5555

## Documentación de los endpoints

- Swagger - OpenAPI -> http://localhost:8000/docs/
- Postman collection -> --TODO