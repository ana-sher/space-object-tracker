from datetime import datetime

from pydantic import BaseModel


class SatelliteCreate(BaseModel):
    """
    Represents a satellite with TLE attributes.
    Attributes:
        object_name (str): Name.
        object_id (str): Object ID.
        epoch (datetime): Epoch time.
        mean_motion (float): Mean motion.
        eccentricity (float): Eccentricity.
        inclination (float): Inclination.
        ra_of_asc_node (float): Right ascension of ascending node.
        arg_of_pericenter (float): Argument of pericenter.
        mean_anomaly (float): Mean anomaly.
        ephemeris_type (int): Ephemeris type.
        classification_type (str): Classification type.
        norad_cat_id (int): NORAD catalog ID.
        element_set_no (int): Element set number.
        rev_at_epoch (int): Revolution at epoch.
        bstar (float): B* drag term.
        mean_motion_dot (float): First time derivative of mean motion.
        mean_motion_ddot (int): Second time derivative of mean motion.
    """

    object_name: str
    object_id: str
    epoch: datetime
    mean_motion: float
    eccentricity: float
    inclination: float
    ra_of_asc_node: float
    arg_of_pericenter: float
    mean_anomaly: float
    ephemeris_type: int
    classification_type: str
    norad_cat_id: int
    element_set_no: int
    rev_at_epoch: int
    bstar: float
    mean_motion_dot: float
    mean_motion_ddot: float


class SatelliteRead(BaseModel):
    object_name: str
    object_id: str
    epoch: datetime
    mean_motion: float
    eccentricity: float
    inclination: float
    ra_of_asc_node: float
    arg_of_pericenter: float
    mean_anomaly: float
    ephemeris_type: int
    classification_type: str
    norad_cat_id: int
    element_set_no: int
    rev_at_epoch: int
    bstar: float
    mean_motion_dot: float
    mean_motion_ddot: float

    model_config = {"from_attributes": True}
