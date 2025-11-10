# Consideración de hash únicos en un sistema de ambiente Distribuido

Para un ambiente distribuido, para lograr que los ID fueran unicos en el sistema, se podría fijar un numero de valores al final o principio del ID,
que sirva como ID propio del sistema al que pertenece dentro del sistema distribuido. Esto se deberia calcular en base a la cantidad de sistemas
considerados, por ejemplo, fijar el ID "XXX09" para un sistema que se encuentra en Valparaiso y un ID "XXX65" para un sistema que se encuentra en 
Santiago, como se realiza con los números telefonicos.
