from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class Vector3D:
    x: float
    y: float
    z: float


@dataclass
class SpaceObject:
    """
    Represents a space object with attributes.

    Attributes:
        id (str): NORAD ID.
        name (str): Name.
        epoch (datetime): Epoch time.
        position (Optional[Vector3D]): Position vector.
        velocity (Optional[Vector3D]): Velocity vector.
        source (Optional[Literal["CELESTRAK"]]): Data source.
    """
    id: str
    name: str
    epoch: datetime
    position: Optional[Vector3D] = None
    velocity: Optional[Vector3D] = None
    source: Optional[Literal["CELESTRAK"]] = None
