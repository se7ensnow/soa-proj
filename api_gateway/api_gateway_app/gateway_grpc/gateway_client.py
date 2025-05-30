import grpc
from api_gateway_app.gateway_grpc import post_pb2_grpc
from api_gateway_app.config import POST_SERVICE_GRPC_URL

async def get_post_stub():
    channel = grpc.aio.insecure_channel(POST_SERVICE_GRPC_URL)
    stub = post_pb2_grpc.PostServiceStub(channel)
    return stub