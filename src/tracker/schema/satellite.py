from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from src.tracker.schema.base_model import Base, utc_now


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
    epoch: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

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
