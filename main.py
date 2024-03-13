# Se importan las librerías necesarias
from fastapi import FastAPI
import pandas as pd

# Se crea la app.
app = FastAPI()

# Se cargan los dataframes
# Games
games = pd.read_parquet("./Data/final/games_final.parquet")
# Reviews
reviews = pd.read_parquet("./Data/final/reviews_final.parquet")
# Items
items = pd.read_parquet("./Data/final/items_final.parquet")

# Se define la función PlayTimeGenre
@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero:str):
    try:
        # Se obtiene la base de juegos y se extraen los géneros por juego a través de un explode.
        g = games.explode("genres")
        # Se obtienen únicamente los juegos del género especificado.
        g = g[g["genres"] == genero]
        # Se obtiene la sumatoria de horas jugadas por juego a partir del dataframe de items.
        i = items.groupby("item_id")["playtime_forever"].sum()
        # Se obtiene un dataframe con las horas por juego y el año de lanzamiento.
        s = pd.merge(g,i,how = "inner",left_on="id",right_on="item_id")
        # Se agrupan las horas jugadas por año de lanzamiento.
        s = s.groupby(s["release_date"].dt.year)["playtime_forever"].sum()

        # se obtiene el año con más horas jugadas.
        año = s.idxmax()
        
        # Se genera la respuesta.
        respuesta = {f"Año de lanzamiento con más horas jugadas para el género {genero}":año}

        return respuesta
    # Se crea una excepción para los casos en donde el género señalado no esté en la base de datos.
    except Exception:
        return {"No se encontraron datos para el género referenciado"}

# Se define la función UserForGenre
@app.get("/UserForGenre")
def UserForGenre(genero:str):
    try:
        # Se obtiene la base de juegos y se extraen los géneros por juego a través de un explode.
        g = games.explode("genres")
        # Se obtienen únicamente los juegos del género especificado.
        g = g[g["genres"] == genero][["release_date","id"]]
        # Se obtiene la lista de id de juegos del género especificado.
        juegos = list(g["id"].unique())
        # Se obtienen los juegos de los usuarios que cumplen con la condición del género.
        i = items[items["item_id"].isin(juegos)]
        # Se unen en un mismo dataframe el año de lanzamiento y las horas jugadas. Se decide usar el año de lanzamiento como referencia para los juegos utilizados. Si bien esto no es garantía de que efectivamente haya jugado el juego en esta fecha, nos sirve como referencia más amplia de años que los datos en review.
        i = pd.merge(i,g,how="inner",left_on="item_id",right_on="id")
        # Se obtienen la sumatoria de horas por usuario.
        i = i.groupby(["user_id",i["release_date"].dt.year])["playtime_forever"].sum()
        # Se obtiene el id del jugador con más horas.
        player = i.idxmax()[0]
        # Se obtiene la información para el jugador identificado.
        player_data = i.loc[player]

        # Se estructura la respuesta: 
        response_data = {
            f"Usuario con más horas jugadas para el género {genero}":player,
            "Horas jugadas": [{"año":year,
                            "horas":playtime
                            }
                            for year,playtime in player_data.items()
                            ]
        }

        return response_data
    # Se crea una excepción para los casos en donde el género señalado no esté en la base de datos.
    except Exception:
        return {"No se encontraron datos para el género referenciado"}

# Se define la función UsersRecommend
@app.get("/UsersRecommend")
def UsersRecommend(año:int):
    try:
        # Se obtienen todos los juegos que tuvieron recomendaciones en el año especificado y cuentan con una recomendación positiva.
        r = reviews[(reviews["posted"].dt.year == año) & (reviews["recommend"] == True) & (reviews["sentiment_analysis"].isin([1,2]))][["item_id","posted","sentiment_analysis"]]
        # Se obtiene la sumatoria de favorabilidad del juego.
        h = r.groupby("item_id")["sentiment_analysis"].sum()
        # Se obtienen los tres juegos más recomendados.
        recomendados = h.nlargest(3).reset_index()

        # Se estructura la respuesta. 
        respuesta = {
            "Puesto 1": games.loc[games["id"] == recomendados.loc[0,"item_id"],"app_name"].iloc[0],
            "Puesto 2": games.loc[games["id"] == recomendados.loc[1,"item_id"],"app_name"].iloc[0],
            "Puesto 3": games.loc[games["id"] == recomendados.loc[2,"item_id"],"app_name"].iloc[0],
        }

        return respuesta
    
    # Se crea una excepción para los casos en donde el año señalado no esté en la base de datos.
    except Exception:
        return {"No se encontraron datos para el año indicado"}

# Se define la función UsersNotRecommend
@app.get("/UsersNotRecommend")
def UsersNotRecommend(año:int):
    try:
        # Se obtienen todos los juegos que tuvieron recomendaciones en el año especificado y cuentan con una recomendación negativa.
        r = reviews[(reviews["posted"].dt.year == año) & (reviews["recommend"] == False) & (reviews["sentiment_analysis"] == 0)][["item_id","posted","sentiment_analysis"]]
        # Se obtiene el número de recomendaciones negativas del juego.
        h = r.groupby("item_id")["sentiment_analysis"].count()
        # Se obtienen los tres juegos menos recomendados.
        recomendados = h.nlargest(3).reset_index()

        # Se estructura la respuesta. 
        respuesta = {
            "Puesto 1": games.loc[games["id"] == recomendados.loc[0,"item_id"],"app_name"].iloc[0],
            "Puesto 2": games.loc[games["id"] == recomendados.loc[1,"item_id"],"app_name"].iloc[0],
            "Puesto 3": games.loc[games["id"] == recomendados.loc[2,"item_id"],"app_name"].iloc[0],
        }

        return respuesta
    
    # Se crea una excepción para los casos en donde el año señalado no esté en la base de datos.
    except Exception:
        return {"No se encontraron datos para el año especificado"}

# Se define la función sentiment_analysis
@app.get("/sentiment_analysis")
def sentiment_analysis(año:int):
    try:
        # Se obtienen todas las reseñas para el año especificado:
        r = reviews[reviews["posted"].dt.year == año]
        # Se obtienen el número de comentario por cada categoria
        r = r.groupby("sentiment_analysis")["user_id"].count()
        # Se estructura la respuesta
        respuesta = {
        "Negative":r[0],
        "Neutral":r[1],
        "Positive":r[2]
        }

        return respuesta
    # Se crea una excepción para los casos en donde el año señalado no esté en la base de datos.
    except Exception:
        return {"No existen datos para el año referenciado"}