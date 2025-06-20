import os

from dotenv import load_dotenv

load_dotenv()

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
POST_SERVICE_GRPC_URL = os.getenv('POST_SERVICE_GRPC_URL')
STATS_SERVICE_GRPC_URL = os.getenv('STATS_SERVICE_GRPC_URL')