import grpc
from api_gateway_app.stats_grpc import stats_pb2_grpc
from api_gateway_app.config import STATS_SERVICE_GRPC_URL

async def get_stats_stub():
    channel = grpc.aio.insecure_channel(STATS_SERVICE_GRPC_URL)
    stub = stats_pb2_grpc.StatsServiceStub(channel)
    return stub