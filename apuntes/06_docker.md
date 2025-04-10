# Docker
Es una plataforma de código abierto que permite a los desarrolladores empaquetar aplicaciones y sus dependencias en contenedores, facilitando su despliegue y ejecución en cualquier entorno. Dentro de docker hay 2 componentes principales:

* Imágenes: modelo o plantilla hecha por capas con archivos del sistema con el diseño y configuraciones que sirve para crear instancias (contenedores)

* Contenedores: espacio que contiene todo lo necesario para la ejecución de aplicaciones, creados a patir de imágenes que pueden ser instanciados en cualquier servidor

    * Diferencias entre Contenedores y Máquinas Virtuales (MV):

        * Contenedores (Docker) son como tener varias apps independientes corriendo en la misma computadora, pero cada una con su propio ambiente cerrado.

            * Nivel de virtualización: A nivel de sistema operativo (SO).

            * Qué virtualiza: Solo las aplicaciones y sus dependencias, usando el mismo kernel del SO host.

            * Arranque: Muy rápido (segundos).

            * Peso: Ligero (comparten el mismo kernel, no requieren sistema operativo completo).

            * Uso típico: Microservicios, despliegue rápido, CI/CD, empaquetar apps.

            * Ventaja: Mayor densidad (puedes correr más contenedores en el mismo host que VMs), más eficiente en recursos.

        * MV son como tener varias computadoras físicas dentro de una sola.

            * Nivel de virtualización: A nivel de hardware.

            * Qué virtualiza: Un sistema operativo completo, incluyendo kernel, drivers, etc.

            * Arranque: Más lento (minutos).

            * Peso: Pesadas (cada VM necesita su propio SO).

            * Uso típico: Aislamiento completo, ejecutar diferentes sistemas operativos (por ejemplo, Windows en Linux).

            * Ventaja: Aislamiento completo del sistema (mejor para entornos más seguros o que requieran kernels distintos). 


## Comandos

* Listar contenedores

    ```
    docker ps
    ```

* Listar imágenes

    ```
    docker images
    ```

* Manegar redes

    ```
    docker network 
    ```

    * Crear redes

        ```
        docker network create <nombre red> --subnet <subnet> --ip-range <ip range>
        ```

    * Listar redes

        ```
        docker network ls
        ```

    * Eliminar redes

        ```
        docker network rm <red>
        ```

    * Conectar redes a contenedores

        ```
        docker network connect <contenedor>
        ```

    * Desconectar redes a contenedores

        ```
        docker network disconnect <contenedor>
        ```

* Manejar Volumenes

    ```
    docker volume
    ```

    * Crear un volume

        ```
        docker volume create <nombre_volume>
        ```
    
    * Listar redes

        ```
        docker network ls
        ```
    
    * Eliminar un volume

        ```
        docker volume rm <volume>
        ```

* Manejar contenedores

    ```
    docker container
    docker run
    ```

    * Crear contenedor

        ```
        docker container create --name <alias> --network <red a la que conectarlo> --volume <path_local:path_container:ro|rw> -p <puerto_local:puerto_container> <image>
        ```

    * Crear un contenedor y lanzarlo

        ```
        docker run <-itd> --name <alias> --network <red a la que conectarlo> --volume <path_local:path_container:ro|rw> -p <puerto_local:puerto_container> <image>
        ```

        Argumentos más usados:
        * ```-i``` (--interactive): Mantiene la entrada estándar (stdin) abierta para que puedas interactuar con el contenedor.
        * ```-t``` (--tty): Asocia una terminal virtual (TTY) al contenedor, proporcionando una interfaz de usuario más amigable y permitiendo que aplicaciones como bash o vim funcionen correctamente.
        * ```-d``` (--detach): Ejecuta el contenedor en segundo plano.
        * ```--name```: Poner allias a un contenedor.
        * ```--network```: Conecta el contenedor a una red específica.
        * ```-p``` (--publish): Mapea un puerto del contenedor al puerto de la máquina host.
        * ```-v``` (--volume): Mapea un directorio de la máquina host a un directorio del contenedor (volumen).
        * ```--volumes-from```: Conectar volume de otro container

        Ejemplo:
            ```
            docker run -i -t -d --name prueba_ubuntu -v C:/Users/34660/projects/mlops/data:/projects/mlops/data/ -p 8080:8080 --network prueba_red ubuntu
            ```

* Manejar image

    ```
    docker image
    ```

    * Eliminar imagen
        
        ```
        docker image rm
        ```
    
    * Crear imagen

        ```
        docker commmit <nombre_container> <nombre_imagen:TAG>
        ```

        Sin embargo, la forma más recomenada, sería mediante un dockerfile.

        
## Dockerfile
Otra opción para generar una imagen es a través de un _Dockerfile_. Para crear la imagen a partir del _Dockerfile_ es necesario ejecutar:

```
docker <buildx> build --ssh default --secret id=<id del secret>,src=<file> -t <nombre_imagen:tag> -f <ubicacion> 
```

* ```--ssh```: permite utilizar las claves ssh del local durante la construcción de la imagen. Para poder utilizarlo en powershell de Windows es necesario que el ssh-agent esté encendido, para lo cual es necesario ejecutar ```Start-Service ssh-agent``` y asegurarse que viene la clave. En caso no apareciera es necesario añadirla en el ssh-aggent ejecutando ```ssh-add ~/.ssh/<clave privada>```

* ```--secret```: per   mite pasar secretos al proceso de construcción de una manera segura, sin que estos secretos queden expuestos en la imagen resultante. Los secretos pueden ser proporcionados como archivos o como variables de entorno y estarán disponibles dentro de la construcción, pero no estarán presentes en la imagen final.

* Principales instrucciones _Dockerfile_

    * En la primera linea se indica la versión del build syntax del Dockerfile con un _syntax directive_ para usar características avanzadas:

        * ```# syntax=docker/dockerfile:1```: Activa sintaxis básica con soporte limitado. --> Por defecto si no se pone nada
        * ```# syntax=docker/dockerfile:1.2```: Soporta RUN --mount=type=cache, etc.
        * ```# syntax=docker/dockerfile:1.3```: Añade --mount=type=secret, SSH forwarding, etc.
        * ```# syntax=docker/dockerfile:1.4```: Soporte completo a COPY --from, target, secrets, cache, etc.
        * ```# syntax=docker/dockerfile:1.5```: Versión más moderna, mejora en manejo de features.
        * ```# syntax=docker/dockerfile:experimental```: Alias de versiones avanzadas, pero puede variar con el tiempo.
    
    * ```FROM <imagen:tag>``` -> Primera instrauccion, que indica la imagen de la que se parte.

    * ```LABEL <maintainer>``` -> Metadata

    * ```RUN <comando simple>``` -> Ejecución comando

    * ```ENV``` -> Variables de entorno

    * ```WORKDIR``` -> Se establece el directorio de trabajo

    * ```ADD``` -> Se copia informacion del host al contenedor, donde además puede descomprimir y soporta URLs

    * ```COPY``` -> Solo copia inforación del host al contenedor

    * ```EXPOSE``` -> Exponer un puerto en ese contenedor

    * ```CMD [<ejecutable>, <argumento 1>, <argumento N>]``` -> Se ejecuta cuando se inicializa el contenedor. Sin embargo si se pasan argumentos a la hora de crear el contenedor, se sobrescriben.
   
    * ```ENTYPOINT [<ejecutable>, <argumento 1>, <argumento N>]``` -> Se ejecuta cuando se inicializa el contenedor. Siempre se ejecutan independiente de se pasan o no argumentos a la hora de crear el contenedor.


## Apendice

### Instalación de docker en windows

[Tutorial instalar docker en windows](https://www.youtube.com/watch?v=ZyBBv1JmnWQ&ab_channel=CodeBear)

### Instalación de minikube con kubernetes en windows

[Tutorial instalar minikube con kubernets](https://www.youtube.com/watch?v=aweohAobrWA&ab_channel=TitasSarker)

### Kubernetes
Kubernetes es como un sistema operativo para tus contenedores (tipo Docker), que los maneja, los organiza y los mantiene vivos, sanos y disponibles.

Defines servicios y despliegues con ficheros yaml:
* deployment -> se encarga de crear y mantener tus pods (contenedores) actualizados, disponibles y replicados.
* service ->  expone tu aplicación para que pueda ser accedida desde fuera del clúster (o desde otros pods).

**Comandos**
* Iniciar una instancia local de Kubernetes en tu máquina utilizando Minikube
    ```
    minikube start
    ```

* Activar docker de minikube
    ```
    eval $(minikube -p minikube docker-env) # Bash
    & minikube -p minikube docker-env | Invoke-Expression # powershell
    ```

* Desactivar docker de minikube
    ```
    eval $(minikube -p minikube docker-env --unset) # Bash
    & minikube -p minikube docker-env --unset | Invoke-Expression # powershell
    ```

* Cargar imagen
    ```
    minikube -p minikube image load prueba_imagen
    ```

* Aplicar configuraciones kubernetes

    Deployment
    ```
    kubectl apply -f ./k8s/deployment.yaml
    kubectl get pods
    ```

    Service
    ```
    kubectl apply -f ./k8s/service.yaml
    ```

* Exponer y abrir en un navegador el servicio de Kubernetes. Minikube, en este caso, actúa como un entorno local para ejecutar Kubernetes.
    ```
    minikube service fastapi-service
    ```