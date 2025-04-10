# Arquitectura de Microservicos

La arquitectura de microservicios es un enfoque de diseño de software donde una aplicación se estructura como un conjunto de servicios pequeños, autónomos, y desplegables de forma independiente, que se comunican entre sí por medio de APIs o mensajes. Donde las principales características son:
* Cada microservicio es responsable de una funcionalidad específica.
* Cada servicio se puede actualizar sin afectar a los demás.
* Puedes usar diferentes lenguajes, bases de datos o herramientas en cada microservicio.
* Escalas solo los servicios que lo necesitan.
* Los servicios no dependen directamente entre sí.

A la hora de desarrollar una arquitectura de microservicios, los principales componenetes son:

* Microservicios
    * Python --> FastApi: es un framework web moderno, rápido y eficiente para construir APIs con Python 3.7+ basado en tipado estático (type hints) y estándares como OpenAPI y JSON Schema.
* API Gateway
* Service Discovery
* Mensajería
* Contenerización y orquestación (Configuración centralizada)
    * [Docker](./06_docker.md): Es una plataforma de código abierto que permite a los desarrolladores empaquetar aplicaciones y sus dependencias en contenedores, facilitando su despliegue y ejecución en cualquier entorno.
* Monitorización
* Seguridad
* Orquestación de workflows