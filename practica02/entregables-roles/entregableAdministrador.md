# Administración del equipo

## Semana 1

La primera semana realizamos una reunión los tres para decidir cual sería el diseño de la interfaz, y
valorando en conjunto cual sería el mejor patrón arquitectónico para este tipo de aplicación.  
Una vez hecho el esbozo inicial, decidimos cómo interaccionaría el usuario con la app y que   
funcionalidades podría tener.  
También se comenzó con una implementación básica de la misma.  

-----

## Semana 2

Para la segunda semana comenzamos con la implementación del diseño. Comenzamos distribuyendo el 
trabajo y que haría cada uno durante esta fase de la práctica.  
También modificamos el diseño de la tablet porque era muy similar al de la semana uno. Este 
nuevo diseño es parecido pero cambia la distribución de los elementos que aparecen en pantalla 
en función del ancho más corto.  
 
-----

## Semana 3

Durante la tercera semana investigamos cómo hacer test end-to-end, y dado que nuestra úníca entrada
de datos que tenemos, es la entrada de divisas para hacer la conversión. Decidimos hacer test sólo
para este campo porque es el que depende de nosotros y no de la API.  
Otro motivo, fue que los test que requieren de una conexión HTTP para obtener datos, la respuesta
de esta conexión es siempre error 400.  
