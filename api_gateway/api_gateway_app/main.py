from fastapi import FastAPI

from api_gateway_app.proxy_routes import users, posts, stats


app = FastAPI(
    title="API Gateway",
    description="Маршрутизатор между UI и сервисами",
    version="1.0"
)

app.include_router(users.auth_router, prefix="/auth", tags=["auth"])
app.include_router(users.users_router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])