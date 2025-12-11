from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column

from src.tracker.schema.base_model import Base


@dataclass
class Vector3D(Base):
    __tablename__ = "vector3d"

    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    z: Mapped[float] = mapped_column(Float)
