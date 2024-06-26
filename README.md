# ¡Bienvenido al proyecto individual 1 de labs!

¡Hola! Soy David Marimón y soy el desarrollador de este repositorio. Quiero darte la bienvenida al trabajo realizado para el primer proyecto individual dentro de la etapa de Labs de mis estudios con Henry. Para el desarrollo del proyecto, tomamos [tres bases de datos](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) proporcionadas por Steam en las cuales encontramos información sobre: los juegos que encontramos en la plataforma así como información descriptiva de cada uno, reviews realizadas por los usuarios a los juegos en la plataforma, y los juegos comprados por cada usuario, así como la sumatoria de horas que acumula cada uno para cada uno de sus juegos. La composición de las bases de datos puede ser explorada en este [diccionario](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link). 

El proyecto tiene como objetivo el desarrollo de un modelo de recomendación Usuario-Ítem consumible a través de la Web haciendo uso de FastAPI, el cual tiene un deploy en Railway a través del siguiente [enlace](https://proyectomarzo-production.up.railway.app/docs#/). 

## Composición del repositorio.
Con este objetivo en mente, encontrás que el repositorio está compuesto de la siguiente manera: 
- [**Carpeta Principal**](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main): La cual está a su vez compuesta por los archivos principales del proyecto para el funcionamiento de la API, tales como el *[main.py](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/main.py)*, donde está el código de las consultas de la API; la documentación de los *[requerimientos](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/requirements.txt)* para el correcto funcionamiento de la API; y el [Procfile](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Procfile) el cual permite la lectura de la API en Railway. Asimismo, podemos ubicar las siguientes sub-carpetas:
- **[Data](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Data)**: Aquí ubicamos a los archivos con la información consumida por las consultas en la API. Dentro de *[Final](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Data/final)* están ubicadas todas las bases de datos después del [procesamiento realizado](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%201/apertura.ipynb) en la primera parte del proyecto; mientras que en *[modelo](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Data/modelo)* se encuentra el archivo donde está ubicado el modelo de recomendación consumible por la API.
- **[Parte 1](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Parte%201)**: En esta carpeta encontramos desarrollada la primera parte del proyecto, la cual consiste en la apertura de las [bases originales](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) compartidas por steam, el pre-procesamiento realizado para su correcta apertura, y un [proceso de limpieza](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%201/apertura.ipynb) que nos permitiera contar con la información mínima necesaria para [la construcción de las primeras 5 consultas](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%201/consultas.ipynb) de la API.
- **[Parte 2](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Parte%202)**: En esta carpeta encontramos toda la información relacionada con el desarrollo del modelo de recomendación, donde contamos con una [revisión estadística](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%202/Revision_EDA.ipynb) de la información en nuestras bases de datos, y el [propio proceso de construcción](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%202/recomendacion.ipynb) del modelo de recomendación, junto con la consulta de la API asociada a este.

## Desarrollo del proyecto. 
Este proyecto está desarrollado en 3 partes:
1. Apertura de las bases de datos y construcción de las consultas descriptivas de la API. 
2. Construcción del Modelo de Recomendación y su consulta asociada para la API.
3. Desarrollo de la API. 

### 1. Apertura de las bases de datos y construcción de las consultas descriptivas de la API.

*Documentación asociada [aquí](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Parte%201)*

Al revisar las [bases de datos originales](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) podemos notar que los archivos están en formato Json, comprimidos a través de Gzip. Sin embargo, de las 3 bases, sólo "steam_games" abre haciendo uso de la librería de pandas y su función "read_json". Para abrir "user_reviews" y "user_items" se intenta convertir cada una de las líneas a texto, transformando los errores de escritura encontrados para intentar convertir cada una de las líneas en formato Json válido, las cuales son convertidas en un dataframe, descartando aquellas líneas cuya transformación a Json válido no fue posible. 

Para el caso de este proyecto, y para el desarrollo de las consultas requeridas por la API, la información necesaria para su correcto funcionamiento es la siguiente: 
- Año y horas jugadas por juego y género de los juegos.
- Horas jugadas por usuario, género y años en los que dicho usuario jugó.
- Recomendaciones por juego (recommend y comentarios) realizadas por los usuarios.
- Año y número de comentarios con sentimientos identificados como positivos, negativos o neutrales en los comentarios realizados por los usuarios.

Con estos 4 parámetros de revisión en mente, dentro del documento [apertura.ipynb](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%201/apertura.ipynb) identificaremos las limpiezas realizadas a las 3 bases de datos para: eliminar nulos, dejar las columnas que se consideraron como necesarias para la obtención de la información de las consultas, y la transformación de dichas columnas para que los datos cumplan con el formato adecuado para la posterior construcción de las consultas. 

Para la limpieza de los datos se usaron las siguientes librerías de Python: pandas, dateutil, gzip, json, unicodedata, langdetect, regex, re y nltk. Todas las bases datos, después de procesadas, fueron guardadas en formato .parquet, con el propósito de ahorrar espacio. 

Con las bases limpias, se procedió a la creación de las primeras 5 consultas de la API. Esta construcción puede ser ubicada en [consultas.ipynb](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%201/consultas.ipynb). Haciendo uso de la librería de Pandas, se construyeron las siguientes consultas:

- *PlayTimeGenre*, la cual recibe en formato string el nombre de un género de vídeojuegos y devuelve año de lanzamiento con más horas jugadas para dicho género. Un ejemplo de retorno de esta consulta es: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}.
- *UserForGenre*, la cual recibe en formato string el nombre de un género de vídeojuegos y devuelve el ID del usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento. Un ejemplo de retorno de esta consulta es: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}.
- *UsersRecommend*, la cual recibe en formato entero un año y devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. Donde se toma en cuenta para esta recomendación que el dato ubicado en la columna "recommend" de la base "reviews" sea verdadero y el análisis de sentimiento para el comentario realizado sea positivo o neutral. Un ejemplo de retorno para esta consulta es: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].
- *UsersNotRecommend*, la cual recibe en formato entero un año y devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. Donde se toma en cuenta para esta recomendación que el dato ubicado en la columna "recommend" de la base "reviews" sea falso y el análisis de sentimiento para el comentario realizado sea negativo. Un ejemplo de retorno para esta consulta es: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].
- *sentiment_analysis*, la cual recibe en formato entero un año y devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento para el año de lanzamiento especificado. Un ejemplo de retorno para esta consulta es: {Negative = 182, Neutral = 120, Positive = 278}.

## 2. Construcción del Modelo de Recomendación y su consulta asociada para la API.
*Documentación asociada [aquí](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Parte%202)*

Aquí, una vez procesadas las bases de datos en la primera parte del proyecto, se procede a realizar una revisión estadística de la información obtenida, con el propósito de observar la composición de la información y ver qué información es de utilidad para el desarrollo del modelo de recomendación. Puedes encontrar la actividad relacionada en el archivo de [Revision_EDA.ipynb](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%202/Revision_EDA.ipynb). Como curiosidad de esta sección, se anidan todas las bases de datos en un solo dataframe, con el propósito de observar cómo se comportan los datos al relacionarlos entre ellos por juego. 

Como se decide trabajar con un modelo de recomendación usuario-ítem, se hace uso de los datos en "review", específicamente los datos agregados en "user_id", "id_item" y "sentiment_analysis", observando el comportamiento de estas variables en relación al ser agrupadas por juego. 

Para esta revisión se hizo uso de las librerías pandas, numpy, scipy.stats, seaborn y matplotlib.pyplot.

En el archivo [recomendacion.ipynb](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Parte%202/recomendacion.ipynb), se puede observar la construcción del modelo de recomendación de Usuario-Ítem, haciendo uso de la librería scikit-surprise. Para ello se usa la información proporcionada por reviews en las columnas "user_id", "id_item" y "sentiment_analysis", datos necesarios para el entrenamiento del modelo. 

Una vez entrenado el modelo, este es guardado en un archivo en la carpeta ["modelo"](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main/Data/modelo) ubicada en la carpeta Data. Con el modelo de recomendación desarrollado, se crea la consulta *recomendacion_usuario* la cual da como resultado una lista con 5 juegos recomendados para un id de usuario dado. Un ejemplo de retorno de esta consulta es: {"item 1":{"id_juego": X, "game name": XY}, "item 2":{"id_juego": X, "game name": XY}, "item 3":{"id_juego": X, "game name": XY}, "item 4":{"id_juego": X, "game name": XY}, "item 5":{"id_juego": X, "game name": XY}}.

## 3. Desarrollo de la API. 

*Documentación asociada [aquí](https://github.com/DaAnMaGi/Proyecto_Marzo/tree/main)*

Para el desarrollo de la API se hace de un entorno virtual alojado inicialmente de manera local usando el método de creación "python -m venv venv" y accediendo a dicho entorno con Uvicorn para probar el funcionamiento de la API. Las librerías (de forma general y sin contar sus dependencias) para el funcionamiento de la API fueron: fastapi, pandas y scikit-surprise. Todas estas se encuentran copiadas en el documento *[requirements.txt](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/requirements.txt)*.

El funcionamiento del código de la API puede ser ubicado en el documento [main.py](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/main.py), el cual extrae las bases de datos y el modelo de recomendación desde su ruta correspondiente en la carpeta de Data para cada una de las consultas desarrolladas en las partes anteriores de este proyecto: 

* PlayTimeGenre
* UserForGenre
* UsersRecommend
* UsersNotRecommend
* sentiment_analysis
* recomendacion_usuario

Como se mencionó anteriormente, el deployment de la API fue realizado a través de [Railway](https://railway.app/dashboard), el cual requiere la configuración del documento [Procfile](https://github.com/DaAnMaGi/Proyecto_Marzo/blob/main/Procfile) para la correcta lectura y funcionamiento de las consultas.

Finalmente, se puede acceder al deployment final del proyecto a través del siguiente [enlace](https://proyectomarzo-production.up.railway.app/docs#/). 