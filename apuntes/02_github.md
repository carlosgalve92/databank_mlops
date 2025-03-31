# GitHub

GitHub es una plataforma que permite a los desarrolladores almacenar, gestionar y compartir su código fuente de manera eficiente, al mismo tiempo que facilita la colaboración en proyectos de software mediante el uso de repositorios remotos.

## Comandos de git relacionados con Github

* Agregar repositorio remoto

    ```
    git remote add <nombre_remoto> <url_del_repositorio>
    ```
    El nombre más común de darle al repositorio remoto es origin.

* Subir cambios al remoto

    ```
    git push -u origin master
    ```

* Eliminar una rama remoto
    
    ```
    git push origin --delete <rama>
    ```

* Verificar cambios antes de descargar cambios

    ```
    git fetch origin
    ```
    Esto genera en local, ramas de seguimiento del remoto con nombres _origin/\<nombre de la rama\>_

* Llevar a cabo el merge

    ```
    git merge origin/<rama>
    ```

* LLevar a cabo el rebase

    ```
    git rebase origin/<rama>
    ```

* Usar al mismo tiempo fetch & merge o fetch & rebase

    * merge
    
    ```
    git pull origin <rama>
    ```
    
    * rebase

    ```
    git pull --rebase origin <rama>
    ```


## Actions (workflow)


## Apendice crear cuenta GitHub

[Tutorial para crear cuenta en GitHub](https://www.youtube.com/watch?v=h5cKAd94QNo&ab_channel=AISciences)

## Apendice usar conexión ssh (Windows)

Se genera clave ssh

```
ssh-keygen -t ed25519 -C "<correo>"
```

Agregar clave al agente ssh

* Evaluar que el agente está en ejecución:

    ```
    Get-Service -Name ssh-agent
    ```

    En caso no esté levantado será necesario levantar el servicio

    ```
    Start-Service ssh-agent
    ```

* Agregar llave

    ```
    ssh-add <C:\ruta\a\tu\clave\id_ed25519>
    ```

Compartir llave publica en GitHub
    
* Copiar llave publica

    ```
    Get-content ~/.ssh/id_ed25519.pub | clip
    ```

* Pegar llave pública en github (dentro de SSH Keys)

    ![alt text](..\images\ssh_keys_github.JPG)
