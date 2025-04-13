# DVC

Es un sistema de control de versiones open-source diseñado específicamente para gestionar grandes volúmenes de datos, modelos de Machine Learning y flujos de trabajo reproducibles. Actúa como una extensión de Git, permitiendo rastrear, versionar y compartir archivos de datos sin comprometer la eficiencia del repositorio.

## Comandos

* Inicializar un repositorio
    
    ```
    dvc init
    ```

    Esto genera:

    * Directorio _.dvc/_

        * Directorio _.dvc/tmp/_ donde se van guardando las diferentes versiones de los ficheros que se van añadiendo al repositorio.

        * Fichero _.dvc/[.gitignore](./../.dvc/.gitignore)_ que directorios que no deben subirse a git.

        * Fichero _.dvc/[config](./../.dvc/config)_ que contiene la configuración de dvc. Los datos sensibles van en el fichero de _.dvc/config.local_ que es ignorado en el _.dvc/[.gitignore](./../.dvc/.gitignore)_.

        
    * fichero [_.dvcignore_](.././.dvcignore) similar al [_.gitignore_](.././.gitignore), es decir, es un fichero donde se indican los directorios y los ficheros _dvc_ debería ignorar. 

    Tras inicializar el directorio, se aconseja hacer commit de los ficheros que pasan automáticamente al stage de git:
    
    * _.dvc/[.gitignore](./../.dvc/.gitignore)_
    
    * _.dvc/[config](./../.dvc/config)_ 

    * [_.dvcignore_](.././.dvcignore)


* Añadir archivos al control de versiones

    ```
    dvc add <archivo>
    ```

    Esto genera en la misma ruta de \<archivo\>

    * \<archivo\>.dvc en la misma ruta que guarda la referencia al dataset.
    
    * Fichero _.gitgnore_ que ignora el archivo que se ha añadido, con el objetivo de que git no suba información pesada.

    Tras añadir el \<archivo\>, te recomiendan trackear los cambios con _git_, para es necesario añadir a git: 
    * _\<archivo\>.dvc_ (```git add <archivvo>```)
    * _.gitignore_ (```git add <ruta_archivo>/.gitignore```)

    Y llevar a cabo el commit, y en el caso de estar usando un repositorio remoto, ejecutar el push.

    ```
    cz commit
    git push
    ```

* Eliminar archivos del control de versiones

    ```
    dvc remove <archivo>
    ```

* Estado de archivos que se encuentran referenciados dentro del control de versiones

    ```
    dvc status
    ```

* Configurar el repositorio remoto

    ```
    dvc remote add <nombre repositorio> <url del repositorio remoto>
    ```

    Generalmente al repositorio remoto se le pone como nombre _origin_

    Si adicional se quiere establecer este repositorio remoto como el de por defecto, se ejecuta:

    ```
    dvc remote default <nombre repositorio>
    ```
    
    * Configurar credenciales para acceder al repositorio

        ```
        dvc remote modify <nombre repositorio> --local access_key_id MI_ACCESS_KEY --local
        dvc remote modify <nombre repositorio> --local secret_access_key MI_SECRET_KEY --local
        ```


* Subir datos al repositorio remoto

    ```
    dvc push
    ```

* Descargar datos del repositorio remoto

    ```
    dvc pull
    ```

* Volver a una versión antigua de los datos

    Primero se cambia al commit de git donde estaban los datos con la versión antigua

    ```
    git checkout <id hash del commit>
    ```

    Si los datos están en remoto sería necesario ejecutar pull para descargar los datos de dicha versión

    ```
    dvc pull
    ```

    Y una vez descargados los datos, ejecutar:

    ```
    dvc checkout
    ```


* Sincronizar metadatos para verificar si han habido cambios en el repositorio remoto

    ```
    dvc fetch
    ```

* Correr experimento

    ```
    dvc exp run
    ```

* Aplicar experimento (para que sea efectivo el commit en git)

    ```
    dvc exp apply <nombre experimento>
    ```

* Mostrar experimentos

    ```
    dvc exp show
    ```

* Subir outputs al repositorio remoto y al repositorio git los metadatos

    ```
    dvc exp push origin --all
    ```

* Listar experimentos

    ```
    dvc exp list --all
    ```

* Descargar del repositorio remoto

    ```
    dvc exp pull origin --all
    ```


## Apendice instalar DVC (windows)

Seguir los pasos que vienen en su página [web oficial](https://dvc.org/doc/install/windows)