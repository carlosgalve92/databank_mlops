# Git flow
El Git Flow en un sistema de Machine Learning (ML) sigue una estructura similar a la de un desarrollo de software tradicional, pero con algunas particularidades debido a la naturaleza de los modelos de ML, los experimentos y los datos. A continuación, se describo un flujo de MLOps en producción:

## A nivel de Ramas

1. **Ramas principales**


    **master / main**: Contiene la última versión estable del sistema de ML en producción.

    **develop**: Contiene el código en desarrollo que será integrado en master tras pruebas y validaciones.

2. **Ramas auxiliares**

    **Feature (feature/nombre-feature)**: Para desarrollar nuevas funcionalidades o mejorar el código. Se crean desde develop y se fusionan en develop cuando están listas.

    **Experiment (experiment/nombre-experimento)**: Para probar modelos y realizar experimentos de ML sin afectar el código estable.

    **Hotfix (hotfix/nombre-hotfix)**: Para corregir errores críticos en producción. Se crean desde master y se fusionan en master y develop.

    **Release (release/nombre-release)**: Para preparar nuevas versiones antes de pasarlas a producción. Se crean desde develop y se fusionan en master y develop tras completar pruebas.

## A nivel de ciclo de Desarrollo

1. Crear una nueva rama feature para desarrollar nueva funcionalidad sin afectar a master y develop

    1.1 Se llevan a cabo experimentos creando ramas de experiment, donde en caso de ser exitoso el experimento, se fusiona la rama de experiment con la de develop.
        
     * Con ayuda de MLFLow se puede dejar registrado hiperparámetros, métricas y artefactos
    
    1.2 Versionado de los datos con ayuda de DVC

2. Fusionar rama feature en rama develop, garantizando que develop siempre tenga las últimas mejoras antes de un lanzamiento
    
    2.1 Llevar a cabo pruebas (CI/CD) antes de fusionar ramas

3. Crear rama release para estabilizar el código antes de llevarlo a producción, ajustando documentación y realizando pruebas finales para preparar el despliegue

4. Se fusiona rama release con la rama master para el despliegue en Producción

    4.1 Llevar a cabo pruebas (CI/CD) antes de fusionar ramas

5. Si hay un error en el master, se genera rama de hotfix para llevar a cabo una rápida corrección, fusionando esta rama con las ramas de develop y master.

## Herramientas

### [Git](01_git.md)

### [GitHub](02_github.md)

### [DVC](03_dvc.md)

### [DagsHub](04_dasghub.md)
