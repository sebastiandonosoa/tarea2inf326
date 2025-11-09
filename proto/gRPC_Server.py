import grpc
from concurrent import futures
from . import analytics_pb2
from . import analytics_pb2_grpc
import sqlite3
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_analytics_db():
    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS URLHits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT NOT NULL,
            short_url TEXT NOT NULL,
            long_url TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        )
    
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_hash ON URLHits(hash)''')
    conn.commit()
    conn.close()

class AnalyticsServicer(analytics_pb2_grpc.AnalyticsServiceServicer):
    def RecordHit(self, request, context):
        try:
            conn = sqlite3.connect("analytics.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO URLHits (hash, short_url, long_url, timestamp) VALUES (?, ?, ?, ?)",
                (request.hash, request.short_url, request.long_url, request.timestamp)
            )
            conn.commit()
            conn.close()
            
            logger.info(f"Hit almacenado por {request.hash} a las {request.timestamp}")
            
            return analytics_pb2.HitResponse(
                success=True,
                message="Hit almacenado correctamente."
            )
        except Exception as e:
            logger.error(f"Error almacenando Hit: {e}")
            return analytics_pb2.HitResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def GetStats(self, request, context):
        try:
            conn = sqlite3.connect("analytics.db")
            cursor = conn.cursor()
            
            if request.hash:
                cursor.execute(
                    """
                    SELECT hash, short_url, long_url, COUNT(*) as hits, MAX(timestamp) as last_accessed, MIN(timestamp) as created_at
                    FROM URLHits
                    WHERE hash = ?
                    GROUP BY hash, short_url, long_url
                    """
                , (request.hash,)
                )
            
            else:
                cursor.execute(
                '''
                    SELECT hash, short_url, long_url, COUNT(*) as hits, MAX(timestamp) as last_accessed, MIN(timestamp) as created_at
                    FROM URLHits
                    GROUP BY hash, short_url, long_url
                    ORDER BY hits DESC
                '''    
                )
            
            results = cursor.fetchall()
            conn.close()
            
            stats_list = []
            for row in results:
                stats_list.append(analytics_pb2.URLStats(
                    hash=row[0],
                    short_url=row[1],
                    long_url=row[2],
                    hit_count=row[3],
                    last_accessed=row[4],
                    created_at=row[5] 
                ))
            
            return analytics_pb2.StatsResponse(stats=stats_list)
        
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return analytics_pb2.StatsResponse()
    
def serve():
    init_analytics_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(
        AnalyticsServicer(), server
    )
    server.add_insecure_port('[::]:50051') ## !Este puede ser el comando que debamos activar para HTTPS. 
    server.start()
    logger.info("gRPC Analytics Server iniciado en el puerto 50051")
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()            
           