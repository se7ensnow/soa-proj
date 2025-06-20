import asyncio
import threading
import grpc

from stats_service_app.database import clickhouse_client
from stats_service_app.models import init_clickhouse_schema
from stats_service_app.stats_kafka.stats_consumer import run_consumer
from stats_service_app.stats_grpc import stats_pb2_grpc
from stats_service_app.stats_grpc.stats_server import StatsService

async def serve_grpc():
    server = grpc.aio.server()
    stats_pb2_grpc.add_StatsServiceServicer_to_server(StatsService(), server)
    server.add_insecure_port('[::]:50052')
    print("[gRPC] StatsService gRPC aio server is running on port 50052...")
    await server.start()
    await server.wait_for_termination()

async def main():
    print("[Init] Creating ClickHouse schema...")
    init_clickhouse_schema(clickhouse_client)

    print("[Kafka] Starting consumer thread...")
    threading.Thread(target=run_consumer, args=(clickhouse_client,), daemon=True).start()

    print("[gRPC] Launching gRPC server...")
    await serve_grpc()

if __name__ == "__main__":
    asyncio.run(main())