from user_service_app.database import Base, engine
from user_service_app.routers import auth, users
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="User Service API",
    description="Сервис управления пользователями",
    version="1.0"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])