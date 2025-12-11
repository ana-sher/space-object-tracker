from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.tracker.schema.base_model import Base, utc_now
from src.tracker.schema.vector3_d_model import Vector3D


@dataclass
class SpaceObject(Base):
    __tablename__ = "space_object"
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

    epoch: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(100))

    position_id: Mapped[int] = mapped_column(ForeignKey("vector3d.id"))
    position: Mapped[Vector3D] = relationship("Vector3D", foreign_keys=[position_id])

    velocity_id: Mapped[int] = mapped_column(ForeignKey("vector3d.id"))
    velocity: Mapped[Vector3D] = relationship("Vector3D", foreign_keys=[velocity_id])

    source: Mapped[Optional[Literal["CELESTRAK"]]] = mapped_column(String(30))

    __table_args__ = (PrimaryKeyConstraint("id", "epoch"),)
