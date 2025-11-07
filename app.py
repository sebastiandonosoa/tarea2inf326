from litestar import Litestar, get, post
from base62 import encode, decode
from typing import Dict
import sqlite3


@post("/url_shortener")
async def create_shortURL(data: Dict[str, str]) -> str:
    conn = sqlite3.connect("URLShort2.db")
    cursor = conn.cursor()

    url_short = data["url_long"].split("/")[0]

    cursor.execute('''CREATE TABLE IF NOT EXISTS ShortURL (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   hash TEXT NOT NULL,
                   long_url TEXT NOT NULL
                   )''')
    
    cursor.execute("SELECT * FROM ShortURL")
    lista = cursor.fetchall()

    if(len(lista) == 0):
        cursor.execute("INSERT INTO ShortURL (id, hash, long_url) VALUES (597652313, ?, ?)", (encode(597652313), data["url_long"]))
        url_short = url_short + "/" + encode(597652313)
    
    else:
        cursor.execute("INSERT INTO ShortURL (hash, long_url) VALUES (?, ?)", ("2", data["url_long"]))

        cursor.execute("SELECT * FROM ShortURL")
        ult_id = cursor.fetchall()[-1][0]

        cursor.execute("UPDATE ShortURL SET hash = ? WHERE id = ?", (encode(ult_id), ult_id))
        url_short = url_short + "/" + encode(ult_id)

    cursor.execute("SELECT * FROM ShortURL")
    lista = cursor.fetchall()
    #print(lista)

    conn.commit()
    conn.close()

    return ("Guardado el url: " + url_short)


@get("/url_shortener/{hash: str}")
async def get_longURL(hash: str) -> str:
    conn = sqlite3.connect("URLShort2.db")
    cursor = conn.cursor()

    id = decode(hash)

    cursor.execute("SELECT * FROM ShortURL WHERE id = ?", (id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        print("El URL original es: ", result[2])
        return result[2]
    return "URL no encontrado"


app = Litestar(route_handlers=[create_shortURL, get_longURL])