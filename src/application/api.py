from fastapi import FastAPI
from sqlalchemy import create_engine

from adapters.database_storage import load_satellites, load_space_objects
from tracker.models import Satellite, SpaceObject
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_connection_string: str = "sqlite:///space_objects.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
app = FastAPI()

engine = create_engine(settings.db_connection_string, echo=True)

@app.get("/satellites", response_model=list)
async def satellites(page: int = 0, limit: int = 100):
    return load_satellites(engine, page, limit)


@app.get("/space-objects", response_model=list)
async def space_objects(page: int = 0, limit: int = 100):
    return load_space_objects(engine, page, limit)
