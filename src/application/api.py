from fastapi import Depends, FastAPI

from src.adapters.database_storage import load_satellites, load_space_objects
from src.application.session import get_db
from src.tracker.models.satellite import SatelliteRead
from src.tracker.models.space_object import SpaceObjectRead

app = FastAPI()


@app.get("/satellites", response_model=list[SatelliteRead])
async def satellites(
    page: int = 0, limit: int = 100, db=Depends(get_db)
) -> list[SatelliteRead]:
    db_sats = load_satellites(db, page, limit)
    return [SatelliteRead.model_validate(obj) for obj in db_sats]


@app.get("/space-objects", response_model=list[SpaceObjectRead])
async def space_objects(
    page: int = 0, limit: int = 100, db=Depends(get_db)
) -> list[SpaceObjectRead]:
    db_so = load_space_objects(db, page, limit)
    return [SpaceObjectRead.model_validate(obj) for obj in db_so]
