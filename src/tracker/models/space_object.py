from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from src.tracker.models.vector3d import Vector3DCreate, Vector3DRead


class SpaceObjectCreate(BaseModel):
    """
    Represents a space object with attributes.

    Attributes:
        id (int): NORAD ID.
        name (str): Name.
        epoch (datetime): Epoch time.
        position (Optional[Vector3D]): Position vector in kilometers from the center of the earth in the idiosyncratic True Equator Mean Equinox coordinate frame used by SGP4.
        velocity (Optional[Vector3D]): Velocity vector is the rate at which the position is changing, expressed in kilometers per second.
        source (Optional[Literal["CELESTRAK"]]): Data source.
    """

    epoch: datetime
    id: int
    name: str
    position_id: int
    position: Vector3DCreate
    velocity_id: int
    velocity: Vector3DCreate
    source: Optional[Literal["CELESTRAK"]]


class SpaceObjectRead(BaseModel):
    epoch: datetime
    id: int
    name: str
    position_id: int
    position: Vector3DRead
    velocity_id: int
    velocity: Vector3DRead
    source: Optional[Literal["CELESTRAK"]]

    model_config = {"from_attributes": True}
