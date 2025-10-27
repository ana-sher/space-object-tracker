import logging
import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine

from adapters.data_source_api import (
    extract_satellite_data,
    extract_space_object_data,
    get_satellite_data,
    space_object_to_df,
)
from adapters.database_storage import load_space_objects, save_or_skip
from tracker.models import Base


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

    save_or_skip(space_objects, engine)
    save_or_skip(satellites, engine)
    saved = load_space_objects(engine)
    print(len(saved))
    df = space_object_to_df(saved)
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
