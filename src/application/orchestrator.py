from adapters.data_source_api import get_satellite_data, space_object_to_df
import pandas as pd
import logging


def run_tracker():
    """
    Runs basic tracker functionality, WIP.
    Fetches satellite data from data source, converts to DataFrame, and prints 5 first records.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    space_objects = get_satellite_data()
    df = space_object_to_df(space_objects)
    print(df.head())
