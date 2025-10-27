from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Optional

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    registry,
    relationship,
)


def utc_now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


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
        id (int): NORAD ID.
        name (str): Name.
        epoch (datetime): Epoch time.
        position (Optional[Vector3D]): Position vector in kilometers from the center of the earth in the idiosyncratic True Equator Mean Equinox coordinate frame used by SGP4.
        velocity (Optional[Vector3D]): Velocity vector is the rate at which the position is changing, expressed in kilometers per second.
        source (Optional[Literal["CELESTRAK"]]): Data source.
    """
    epoch: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(100))
    position_id: Mapped[int] = mapped_column(ForeignKey("vector3d.id"))
    position: Mapped["Vector3D"] = relationship("Vector3D", foreign_keys=[position_id])
    velocity_id: Mapped[int] = mapped_column(ForeignKey("vector3d.id"))
    velocity: Mapped["Vector3D"] = relationship("Vector3D", foreign_keys=[velocity_id])
    source: Mapped[Optional[Literal["CELESTRAK"]]] = mapped_column(String(30))

    __table_args__ = (PrimaryKeyConstraint("id", "epoch"),)


@dataclass
class Satellite(Base):
    __tablename__ = "satellite"
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

    object_name: Mapped[str] = mapped_column(String(100))
    object_id: Mapped[str] = mapped_column(String(100))
    epoch: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    mean_motion: Mapped[float] = mapped_column(Float)
    eccentricity: Mapped[float] = mapped_column(Float)
    inclination: Mapped[float] = mapped_column(Float)
    ra_of_asc_node: Mapped[float] = mapped_column(Float)
    arg_of_pericenter: Mapped[float] = mapped_column(Float)
    mean_anomaly: Mapped[float] = mapped_column(Float)
    ephemeris_type: Mapped[int] = mapped_column(Integer)
    classification_type: Mapped[str] = mapped_column(String(100))
    norad_cat_id: Mapped[int] = mapped_column(Integer)
    element_set_no: Mapped[int] = mapped_column(Integer)
    rev_at_epoch: Mapped[int] = mapped_column(Integer)
    bstar: Mapped[float] = mapped_column(Float)
    mean_motion_dot: Mapped[float] = mapped_column(Float)
    mean_motion_ddot: Mapped[float] = mapped_column(Float)

    __table_args__ = (PrimaryKeyConstraint("norad_cat_id", "epoch"),)
