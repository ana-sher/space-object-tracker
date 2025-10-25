from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship, DeclarativeBase
from sqlalchemy import DateTime, Float, ForeignKey, String, func

class Base(DeclarativeBase):
    pass

@dataclass
class Vector3D(Base):
    __tablename__ = "vector3d"
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    z: Mapped[float] = mapped_column(Float)


@dataclass
class SpaceObject(Base):
    __tablename__ = "space_object"
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
    epoch: Mapped[datetime] = mapped_column(
        insert_default=func.utc_timestamp(), default=None
    )
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id"))
    position: Mapped["Vector3D"] = relationship("Vector3D", foreign_keys=[position_id])
    velocity_id: Mapped[int] = mapped_column(ForeignKey("velocity.id"))
    velocity: Mapped["Vector3D"] = relationship("Vector3D", foreign_keys=[velocity_id])
    source: Mapped[Optional[Literal["CELESTRAK"]]] = mapped_column(String(30))
