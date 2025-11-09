from litestar import Litestar, get, post, Request, Response
from litestar.status_codes import HTTP_302_FOUND
from litestar.datastructures import Headers
from litestar.response import Template
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from pathlib import Path
from base62 import encode, decode
from typing import Dict
import sqlite3
import logging
import time
import re
from proto.gRPC_Client import AnalyticsClient 
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analytics_client = AnalyticsClient()

def init_db():
    conn = sqlite3.connect("URLShort1.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ShortURL (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   hash TEXT NOT NULL UNIQUE,
                   long_url TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )''')
    conn.commit()
    conn.close()

def validate_url(url: str) -> tuple[bool, str]:
    """
    Método encargado de validar el URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    
    url_pattern = re.compile(
        r'^https?://'  
        r'(?:'  
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)*'  
            r'[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?'  
            r'\.[A-Z]{2,}\.?'  
        r'|'  
            r'localhost'  # localhost
        r'|'  
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # Dirección IP
        r')'
        r'(?::\d+)?'  # Puerto opcional (:8080)
        r'(?:/?|[/?]\S+)?$',  # Ruta y query params opcionales
        re.IGNORECASE
    )
    
    is_valid = url_pattern.match(url) is not None
    return is_valid, url
    
@get("/")
async def index() -> Template:
    return Template(template_name="index.html")

@post("/url_shortener")
async def create_shortURL(data: Dict[str, str], request: Request) -> Dict[str, str]:
    long_url = data.get("url_long", "").strip()

    # Validamos URL ...
    if not long_url:
        return Response(
            content={"error": "La URL es necesaria."},
            status_code = 400
        )
    
    is_valid, normalized_url = validate_url(long_url)
    if not is_valid:
        return Response(
            content={"error": "La URL es inválida."},
            status_code=400
        )
    
    try:
        conn = sqlite3.connect("URLShort1.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT hash from ShortURL WHERE long_url = ?", (normalized_url,))
        existing = cursor.fetchone()
        
        if existing:
            hash_value = existing[0]
            logger.info(f"URL ya existente: {hash_value}")
        else:
            cursor.execute("SELECT MAX(id) from ShortURL")
            max_id = cursor.fetchone()[0]
            
            if max_id is None:
                new_id = 597652313
            else:
                new_id = max_id + 1 ##! Revisar esta parte
            
            hash_value = encode(new_id)
            cursor.execute("INSERT INTO ShortURL (id, hash, long_url) VALUES (?, ?, ?)", (new_id, hash_value, normalized_url))
            conn.commit()
            logger.info(f"URL corta creada: {hash_value}")
            
        base_url = f"{request.url.scheme}://{request.url.netloc}" 
        short_url = f"{base_url}/s/{hash_value}" # Para navegador...
        
        conn.close()
        
        return {
            "short_url": short_url,
            "long_url": long_url,
            "hash": hash_value,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error creando la URL corta: {e}")
        return Response(
            content={"Error": "Fallo al crear la URL corta"},
            status_code=500
        )


@get("/s/{hash: str}")
async def get_longURL(hash: str, request: Request) -> Response:
    try:
        conn = sqlite3.connect("URLShort1.db")
        cursor = conn.cursor()
        
        id_value = decode(hash)
        cursor.execute("SELECT long_url FROM ShortURL WHERE id = ?", (id_value,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            long_url = result[0]
            short_url = f"{request.url.scheme}://{request.url.netloc}/s/{hash}"
            
            analytics_client.record_hit(hash, short_url, long_url)
            
            logger.info(f"Redirigiendo {short_url} -> {long_url}")
            
            return Response(
                content=None,
                status_code=HTTP_302_FOUND,
                headers=Headers({
                    "Location": long_url,
                    "Cache-Control": "no-cache, no-store, must-revalidate"
                })
            )
        
        logger.warning(f"URL no encontrada para hash: {hash}")
        return Template(template_name="404.html", context = {"hash": hash})
    
    except Exception as e:
        logger.error(f"Error recuperando URL: {e}")
        return Response(
            content={"error": "URL corta inválida"},
            status_code = 404
        )
        
@get("/stats")
async def get_stats() -> Template:
    stats = analytics_client.get_stats()
    
    formatted_stats = []
    for stat in stats:
        formatted_stats.append({
            'hash': stat.hash,
            'short_url': stat.short_url,
            'long_url': stat.long_url,
            'hit_count': stat.hit_count,
            'last_accessed': datetime.fromtimestamp(stat.last_accessed).strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': datetime.fromtimestamp(stat.created_at).strftime('%Y-%m-%d %H:%M:%S')
        })
    return Template(template_name="stats.html", context={"stats": formatted_stats})

async def cleanup() -> None:
    """Cleanup gRPC client on shutdown"""
    analytics_client.close()


init_db()

app = Litestar(
    route_handlers=[index, create_shortURL, get_longURL, get_stats], # Agregar stats post
    debug=True,
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    on_shutdown=[cleanup]
)


