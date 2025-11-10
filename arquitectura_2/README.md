# Arquitectura 2 (Litestar Framework)

## Dependencias

Se debe instalar los modulos "Litestar" y "Base62" para el correcto funcionamiento de los códigos, una forma de instalarlo es usando pip de la siguiente forma en la terminal:

```bash
"pip install pybase62"
"pip install litestar[standard]"
```

## Uso del framework

Se accede a la carpeta en donde esta la app y se ejecuta de la siguiente forma:

```bash
litestar run
```

Con ello se ejecuta la API y que permite acceder a los siguientes Endpoints: POST que entrega un hash para acceder en base a un url_short y GET para acceder usando el url_short y que redirige a la página del url_long. Importante considerar que solo se crea la API y sus Endpoints, no se creó una interfaz, por lo que una herramiento como "Postman" resulta útil para probar la implementación 

## POST: http://localhost:8000/url_shortener

Se ejecuta un request del tipo **POST**, se requiere pasar en el body del request el url_long que se quiere guardar, siendo el body el siguiente JSON de ejemplo:

```bash
{
    "url_long" : "usm.cl/informatica/postulaciones-a-postgrado/2025"
}
```

Se obtendra un enlace url_short que permite acceder a la url_long, por ejemplo, se obtendría "usm.cl/eRgfR"

## GET: http://localhost:8000/url_shortener/{hash}

Se ejecuta un request del tipo **GET**, se paso solo el hash como parametro, lo que devolvera el url_long que ha sido guardado en la base de datos.
