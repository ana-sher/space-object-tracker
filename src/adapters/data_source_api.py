import logging
from datetime import datetime, timezone

import pandas as pd
import requests
from sgp4 import omm
from sgp4.api import Satrec, jday

from src.tracker.models.satellite import SatelliteCreate
from src.tracker.models.space_object import SpaceObjectCreate
from src.tracker.models.vector3d import Vector3DCreate


def get_satellite_data() -> list[dict]:
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
        logging.warning(
            "Celestrak data retrieval error. Status code: %s", response.status_code
        )
    response.raise_for_status()
    logging.info("Celestrak data retrieved successfully.")

    json = response.json()
    return json


def extract_satellite_data(data: list[dict]) -> list[SatelliteCreate]:
    """
    Extracts satellite data from the provided dictionary and returns a list of Satellite instances.

    Args:
        data (list[dict]): List of dictionaries containing satellite data.

    Returns:
        list[Satellite]: List of Satellite instances.
    """
    logging.info("Extracting satellites data.")
    return [_to_satellite(fields) for fields in data]


def extract_space_object_data(data: list[dict]) -> list[SpaceObjectCreate]:
    """
    Extracts space object data from the provided dictionary and returns a list of SpaceObject instances.

    Args:
        data (list[dict]): List of dictionaries containing space object data.

    Returns:
        list[SpaceObject]: List of SpaceObject instances.
    """
    logging.info("Extracting and calculating space objects data.")
    spaceObjects = []
    for fields in data:
        sat = Satrec()
        omm.initialize(sat, fields)
        when = datetime.fromisoformat(fields["EPOCH"]).replace(tzinfo=timezone.utc)
        jd, fr = jday(
            when.year,
            when.month,
            when.day,
            when.hour,
            when.minute,
            when.second + when.microsecond / 1e6,
        )
        error, position, velocity = sat.sgp4(jd, fr)
        if error != 0:
            raise RuntimeError(f"SGP4 propagation error code: {error}")
        fields["X"], fields["Y"], fields["Z"] = position
        fields["VX"], fields["VY"], fields["VZ"] = velocity
        spaceObjects.append(_to_space_object(fields))

    return spaceObjects


def space_object_to_df(space_objects: list[SpaceObjectCreate]) -> pd.DataFrame:
    """
    Converts space_objects list to DataFrame.

    Args:
        space_objects (list[SpaceObject]): List of space objects.

    Returns:
        DataFrame: Pandas DataFrame.
    """
    logging.info("Extracting DataFrame from space objects data.")
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


def _to_space_object(data: dict) -> SpaceObjectCreate:
    return SpaceObjectCreate(
        id=data["NORAD_CAT_ID"],
        name=data["OBJECT_NAME"],
        epoch=datetime.fromisoformat(data["EPOCH"]),
        position=Vector3DCreate(x=data["X"], y=data["Y"], z=data["Z"]),
        velocity=Vector3DCreate(x=data["VX"], y=data["VY"], z=data["VZ"]),
        source="CELESTRAK",
    )


def _to_satellite(data: dict) -> SatelliteCreate:
    return SatelliteCreate(
        object_id=data["OBJECT_ID"],
        object_name=data["OBJECT_NAME"],
        ephemeris_type=data["EPHEMERIS_TYPE"],
        classification_type=data["CLASSIFICATION_TYPE"],
        element_set_no=data["ELEMENT_SET_NO"],
        norad_cat_id=data["NORAD_CAT_ID"],
        epoch=datetime.fromisoformat(data["EPOCH"]),
        inclination=data["INCLINATION"],
        ra_of_asc_node=data["RA_OF_ASC_NODE"],
        eccentricity=data["ECCENTRICITY"],
        arg_of_pericenter=data["ARG_OF_PERICENTER"],
        mean_anomaly=data["MEAN_ANOMALY"],
        mean_motion=data["MEAN_MOTION"],
        rev_at_epoch=data["REV_AT_EPOCH"],
        bstar=data["BSTAR"],
        mean_motion_dot=data["MEAN_MOTION_DOT"],
        mean_motion_ddot=data["MEAN_MOTION_DDOT"],
    )
