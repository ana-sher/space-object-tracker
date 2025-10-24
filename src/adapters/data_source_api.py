from datetime import datetime, timezone
import logging
import numpy as np
import requests

from sgp4 import omm
from sgp4.api import Satrec, jday

import pandas as pd

from tracker.models import SpaceObject, Vector3D


def get_satellite_data() -> list[SpaceObject]:
    """
    Gets satellite data from Celestrak active satellites OMM in JSON format,
    propagates their positions and velocities to the current time using SGP4,
    and returns a list of SpaceObject instances.

    Returns:
        list[SpaceObject]: Retrieved list of SpaceObject instances.
    """
    logging.info("Retrieving satellite data from Celestrak...")
    response = requests.get(
        "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
    )
    if not response.ok:
        logging.warning("Celestrak data retrieval error. Status code: %s", response.status_code)
    response.raise_for_status()
    logging.info("Celestrak data retrieved successfully.")

    json = response.json()

    when = datetime.now(timezone.utc)
    jd, fr = jday(
        when.year,
        when.month,
        when.day,
        when.hour,
        when.minute,
        when.second + when.microsecond / 1e6,
    )

    spaceObjects = []
    for fields in json:
        sat = Satrec()
        omm.initialize(sat, fields)
        error, position, velocity = sat.sgp4(jd, fr)
        if error != 0:
            raise RuntimeError(f"SGP4 propagation error code: {error}")
        fields["X"], fields["Y"], fields["Z"] = position
        fields["VX"], fields["VY"], fields["VZ"] = velocity
        spaceObjects.append(_to_space_object(fields))

    return spaceObjects


def space_object_to_df(space_objects: list[SpaceObject]) -> pd.DataFrame:
    """
    Converts space_objects list to DataFrame.

    Args:
        space_objects (list[SpaceObject]): List of space objects.

    Returns:
        DataFrame: Pandas DataFrame.
    """
    return pd.DataFrame(
        [
            {
                "id": obj.id,
                "name": obj.name,
                "epoch": obj.epoch,
                "pos_x": obj.position.x if obj.position else None,
                "pos_y": obj.position.y if obj.position else None,
                "pos_z": obj.position.z if obj.position else None,
                "vel_x": obj.velocity.x if obj.velocity else None,
                "vel_y": obj.velocity.y if obj.velocity else None,
                "vel_z": obj.velocity.z if obj.velocity else None,
                "source": obj.source,
            }
            for obj in space_objects
        ]
    )


def _to_space_object(data: dict) -> SpaceObject:
    return SpaceObject(
        id=data["NORAD_CAT_ID"],
        name=data["OBJECT_NAME"],
        epoch=datetime.fromisoformat(data["EPOCH"]),
        position=Vector3D(x=data["X"], y=data["Y"], z=data["Z"]),
        velocity=Vector3D(x=data["VX"], y=data["VY"], z=data["VZ"]),
        source="CELESTRAK",
    )
