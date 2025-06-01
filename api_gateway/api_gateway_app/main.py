from fastapi import FastAPI
from api_gateway_app.proxy import setup_proxy_routes

app = FastAPI(title="API Gateway")

setup_proxy_routes(app)