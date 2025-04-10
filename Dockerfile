# syntax=docker/dockerfile:experimental
FROM ubuntu

# Instalar git
RUN apt-get update && apt-get install -y git openssh-client python3.10 python3-pip python3-venv

# Asegurarse de que el directorio .ssh y known_hosts estén configurados
RUN mkdir -p ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

# Clonar un repositorio privado usando la clave SSH
RUN --mount=type=ssh git clone git@github.com:carlosgalve92/databank_mlops.git

# Se establece directorio de trabajo
WORKDIR /databank_mlops

# Instalación del paquete
RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install .


# Se descargan datos de dagshub
RUN --mount=type=secret,id=dvc_secrets,target=/databank_mlops/.dvc/config.local\
    dvc pull

# Se expone el contenedor en el puerto 8000
EXPOSE 8000

# Comando que se ejecuta al iniciarse el contenedor 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]