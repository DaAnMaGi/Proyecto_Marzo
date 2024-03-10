# Se importan las librerías necesarias
from fastapi import FastAPI
import pandas as pd

# Se crea la app.
app = FastAPI()

# Se cargan los dataframes
# Games
games = pd.read_json("../Data/corregida/r_games.json.gzip",compression="gzip",convert_dates=['release_date'],date_unit="ms")
# Reviews
reviews = pd.read_json("../Data/corregida/r_reviews.json.gzip",compression="gzip",convert_dates=["posted"],date_unit="ms")
# Items
items = pd.read_parquet("../Data/corregida/items.parquet.gzip")

# Se define la función PlayTimeGenre
@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero:str):
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

# Se define la función UserForGenre
@app.get("/UserForGenre")
def UserForGenre(genero:str):
    # Se obtiene la base de juegos y se extraen los géneros por juego a través de un explode.
    g = games.explode("genres")
    # Se obtienen únicamente los juegos del género especificado.
    g = g[g["genres"] == genero][["release_date","id"]]
    # Se obtiene la lista de id de juegos del género especificado.
    juegos = list(g["id"].unique())
    # Se obtienen los juegos de los usuarios que cumplen con la condición del género.
    i = items[items["item_id"].isin(juegos)]
    # Se unen en un mismo dataframe el año de lanzamiento y las horas jugadas.
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

# Se define la función UsersRecommend
@app.get("/UsersRecommend")
def UsersRecommend(año:int):
    # Se obtienen todos los juegos que tuvieron lanzamiento en el año especificado.
    g = games[games["release_date"].dt.year == año][["id","app_name"]]
    # Se obtienen los ID de los juegos 
    juegos = list(g["id"].unique())
    # Se obtienen los juegos con recomendación positiva para el año especificado. 
    r = reviews[reviews["item_id"].isin(juegos) & reviews["recommend"] == True & reviews["sentiment_analysis"].isin([1,2])][["item_id","recommend","sentiment_analysis"]]
    # Se obtiene la sumatoria de favorabilidad del juego.
    h = r.groupby("item_id")["sentiment_analysis"].sum()
    # Se unen los dataframes.
    g = pd.merge(g,h,how="inner",left_on="id",right_on="item_id")
    # Se obtienen los tres juegos más recomendados.
    recomendados = g.nlargest(3,"sentiment_analysis")
    # Se estructura la respuesta. 
    respuesta = {
        "Puesto 1":recomendados.iloc[0]["app_name"],
        "Puesto 2":recomendados.iloc[1]["app_name"],
        "Puesto 3":recomendados.iloc[2]["app_name"]
    }

    return respuesta

# Se define la función UsersNotRecommend
@app.get("/UsersNotRecommend")
def UsersNotRecommend(año:int):
    # Se obtienen todos los juegos que tuvieron lanzamiento en el año especificado.
    g = games[games["release_date"].dt.year == año][["id","app_name"]]
    # Se obtienen los ID de los juegos 
    juegos = list(g["id"].unique())
    # Se obtienen los juegos con recomendación negativa para el año especificado. 
    r = reviews[(reviews["item_id"].isin(juegos)) & (reviews["recommend"] == False) & (reviews["sentiment_analysis"] == 0)][["item_id","recommend","sentiment_analysis"]]
    # Se obtiene el número de veces que el juego no fue recomendado.
    h = r.groupby("item_id")["sentiment_analysis"].count()
    # Se unen los dataframes.
    g = pd.merge(g,h,how="inner",left_on="id",right_on="item_id")
    # Se obtienen los tres juegos menos recomendados.
    no_recomendados = g.nlargest(3,"sentiment_analysis")
    # Se estructura la respuesta. 
    respuesta = {
        "Puesto 1":no_recomendados.iloc[0]["app_name"],
        "Puesto 2":no_recomendados.iloc[1]["app_name"],
        "Puesto 3":no_recomendados.iloc[2]["app_name"]
    }

    return respuesta

# Se define la función sentiment_analysis
@app.get("/sentiment_analysis")
def sentiment_analysis(año:int):
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