import grpc
from . import analytics_pb2
from . import analytics_pb2_grpc
import logging
import time

logger = logging.getLogger(__name__)

class AnalyticsClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = analytics_pb2_grpc.AnalyticsServiceStub(self.channel)
        
    def record_hit(self, hash_value: str, short_url: str, long_url: str):
        try:
            timestamp = int(time.time())
            request = analytics_pb2.HitRequest(
                hash=hash_value,
                short_url=short_url,
                long_url=long_url,
                timestamp=timestamp
            )
            response = self.stub.RecordHit(request, timeout=5)
            return response.success
        except grpc.RpcError as e:
            logger.error(f"gRPC error almancenando Hit: {e}")
            return False
        except Exception as e:
            logger.error(f"Error almacenando hit: {e}")
            return False
    
    def get_stats(self, hash_value: str = None):
        try:
            request = analytics_pb2.StatsRequest(hash=hash_value or "")
            response = self.stub.GetStats(request, timeout=10)
            return response.stats
        except grpc.RpcError as e:
            logger.error(f"Error del gRPC para obtener las estadísticas: {e}")
            return []
        except Exception as e:
            logger.error(f"Error obteniendo características: {e}")
            return []
    
    def close(self):
        self.channel.close()