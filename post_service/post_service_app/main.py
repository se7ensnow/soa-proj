import grpc
import asyncio

from post_service_app.post_grpc import post_pb2_grpc
from post_service_app.post_grpc.post_server import PostService
from post_service_app.database import Base, engine

async def serve():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    server = grpc.aio.server()
    post_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port('[::]:50051')
    print("PostService gRPC aio server is running on port 50051...")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())