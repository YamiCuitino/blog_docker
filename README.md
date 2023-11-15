# blog_docker
# Punto De Vista - Docker

Descripción corta del proyecto.

## Requisitos Previos

Asegúrate de tener instalados los siguientes requisitos antes de comenzar:

- Docker: [Instalación de Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Instalación de Docker Compose](https://docs.docker.com/compose/install/)

## Configuración del Proyecto

1. Clona el repositorio:

    git clone https://github.com/YamiCuitino/blog_docker
    cd blog_docker
   
3. Crea un archivo `.env` en el directorio raíz del proyecto y configura las variables de entorno necesarias. Puedes utilizar el archivo `.env.example` como referencia.

## Construcción y Ejecución

### Producción

1.	Construye y levanta la aplicación :

    docker-compose build
    docker-compose up
  	
   La aplicación estará disponible en [http://localhost:5005](http://localhost:5005).

3. Para frenar la aplicación , puedes usar:

    	docker-compose stop
   
 Para cancelarlo, puedes usar: 

Crtl + C

Para volver a levantarlo, puedes utilizar:

	docker-compose up –d  o  docker-compose restart


## Integrantes.

Alvarez Tomás, Bringas Delfina, Cuitiño Yamila
