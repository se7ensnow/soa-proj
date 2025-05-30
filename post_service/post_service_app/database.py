from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from post_service_app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()