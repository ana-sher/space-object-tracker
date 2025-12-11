import logging
import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.data_source_api import (
    extract_satellite_data,
    extract_space_object_data,
    get_satellite_data,
    space_object_to_df,
)
from src.adapters.database_storage import load_space_objects, save_or_skip
from src.tracker.schema.base_model import Base
from src.tracker.schema.satellite import Satellite
from src.tracker.schema.space_object import SpaceObject


def run_tracker():
    """
    Runs basic tracker functionality, WIP.
    Fetches satellite data from data source, converts to DataFrame, and prints 5 first records.
    """
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    engine = _init_db()

    satellites_json = get_satellite_data()
    satellites = extract_satellite_data(satellites_json)
    space_objects = extract_space_object_data(satellites_json)
    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, future=True
    )
    session = session_local()

    save_or_skip(
        [SpaceObject(**space_object.model_dump()) for space_object in space_objects],
        session,
    )
    save_or_skip(
        [Satellite(**satellite.model_dump()) for satellite in satellites], session
    )
    saved = load_space_objects(session)
    print(len(saved))
    df = space_object_to_df(space_objects)
    print(df.head())


def _init_db() -> Engine:
    DB_CONNECTION_STRING = os.getenv(
        "DB_CONNECTION_STRING", "sqlite:///space_objects.db"
    )
    engine = create_engine(DB_CONNECTION_STRING, echo=True)
    Base.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    run_tracker()
