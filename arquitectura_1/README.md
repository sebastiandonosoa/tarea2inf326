# tarea2inf326
Repositorio de Tarea 2 del ramo Arquitectura De Software.

Comenzamos ubicandonos en la carpeta "base":

```bash
cd ".../tarea2inf326/arquitectura_1"
```

Es recomendable que instales los paquetes en un entorno conda. Para eso, utiliza el siguiente comando, que se encarga de crear el ambiente conda con los paquetes necesarios:

```bash
conda env create -f enviroment.yml
conda activate tarea2inf326
```

### Opción 2: Usando venv
Este método utiliza `venv`, la herramienta de entornos virtuales que viene con Python.
1.  Navega a la carpeta del proyecto:
    ```bash
    cd ".../tarea2inf326/arquitectura_1"
    ```
2.  Crea y activa un entorno virtual:
    ```bash
    # Crear
    py -m venv .venv
    # Activar
    .\.venv\Scripts\activate
    ```
3.  Instala las dependencias (con el entorno activado):
    ```bash
    pip install "litestar[standard]" uvicorn jinja2 pybase62 grpcio grpcio-tools
    ``

Tenemos que iniciar como módulo el gRPC_Server.py, el cual es el archivo encargado gestionar las peticiones por parte del cliente (hit a página, o solicitud de estadísticas realizadas por el archivo gRPC_Client.py, el cual es llamado desde su endpoint en LiteStar) que deben ser almacenadas en la base de datos del servidor.

```bash
python -m proto.gRPC_Server
```

Ahora desde otra terminal, tenemos que encargarnos de iniciar nuestra API (LiteStar), usando el siguiente comando:

```bash
litestar --app app:app run --host 0.0.0.0 --port <puerto_tuyo> --reload
```
