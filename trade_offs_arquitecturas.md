# Arquitectura 1

## Trade-offs 

La arquitectura 1 presenta las siguientes ventajas:

1. Gracias al uso del código "HTTP 302 - Temporary Redirect" es posible obtener información precisa sobre los usuarios que acceden a URLs largas a través de nuestro acortador. Esto nos permite realizar análisis detallados del comportamiento de nuestros clientes.
2. Al implementar redireccionamiento temporal, si una de las URLs largas cambia (ya sea por decisión de cliente, o por nosotros en la base de datos), el usuario que accede a dicha dirección mediante nuestro acortador no se verá afectado, ya que basta con actualizar la URL larga correspondiente.
3. En el caso de que las URLs almacenadas en nuestra base de datos se convierte en una dirección maliciosa, podemos bloquear el acceso a ella a través de su dirección acortada, redirigiendo al usuario hacia una dirección nueva o segura. Esto añade una capa adicional de seguridad al sistema.

Respecto a las desventajas:

1. El almacenamiento de información de cada "url hit" en la base de datos del servidor gRPC, junto a la búsqueda local sobre la dirección solicitada, genera una alta carga computacional en la arquitectura.
2. El uso de un servidor remoto que realiza operaciones constantes sobre la base de datos puede provocar cuellos de botella en situaciones de alto tráfico, dificultando la escabilidad de la arquitectura a medida que aumenta el número de usuarios activos.
3. Al no contar con réplicas de la base de datos, una caida del servidor provocaría una interrupción total del servicio. Generando problemas de disponibilidad.
4. Debido al alto costo computacional, será necesario invertir más en recursos de cómputos, lo que podría afectar la viabilidad económica de la arquitectura.

## Consideración respecto al dominio

Si consideramos el dominio de la USM (según lo indicado en el enunciado de la tarea), resulta conveniente que la universidad (o empresa que contrate los servicios de nuestra url shortener) pueda conocer los sitios más visitados por el público. Esta información puede reflejar tendencias de interés, como carreras más visitadas, o el aréa de interés de los alumnos, y servir de apoyo en estrategias de marketing o toma de decisiones institucionales.

Asi mismo, el uso constante de redireccionamientos no permite garantizar que los enlaces acortados sean seguros, evitando riesgos de dañar la imagen del cliente. Sin embargo, es importante considerar que, a medida que aumenta el número de usuarios, el sistema tiende a disminuir su desempeño y puede generar latencias, lo que podría impactar negativamente la experiencia de uso.

En conclusión, la arquitectura propuesta resulta pertinente para el dominio de la USM, aunque es recomendable optimizar su rendimiento ante escenarios de alto tráfico para asegurar escalabilidad y disponibilidad. 
