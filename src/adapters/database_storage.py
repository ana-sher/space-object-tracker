from typing import Any, TypeVar

from sqlalchemy import and_
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Mapper, Session, selectinload

from src.tracker.schema.satellite import Satellite
from src.tracker.schema.space_object import SpaceObject

T = TypeVar("T")


def save(objects: list[T], db: Session):
    """
    Save a list of T to the database.

    Args:
        objects: List of object instances to save.
        db: SQLAlchemy session.
    """

    db.add_all(objects)
    db.commit()


def save_or_skip(objects: list[T], db: Session):
    """
    Bulk save or skip a list of T to the database.

    Args:
        objects: List of T instances to save.
        db: SQLAlchemy session.
    """
    if not objects:
        return

    model_type: Any = objects[0].__class__

    mapper: Mapper = inspect(model_type)
    if not mapper:
        return
    pk_attrs = mapper.primary_key
    pkeys = [pk_attr.key for pk_attr in pk_attrs]

    if pkeys is None:
        return
    if pkeys.count(None) > 0:
        return

    ids_m = [
        [getattr(obj, pkey) for obj in objects] for pkey in pkeys if pkey is not None
    ]

    existing_ids = [
        existing_pks
        for existing_pks in db.query(*pk_attrs)
        .filter(
            *[
                and_(*[pk_attr == ids_m[i][j] for i, pk_attr in enumerate(pk_attrs)])
                for j in range(len(ids_m[0]))
            ]
        )
        .all()
    ]
    to_insert = [
        o
        for o in objects
        if tuple(getattr(o, pkey) for pkey in pkeys if pkey is not None)
        not in existing_ids
    ]
    if not to_insert:
        return
    db.add_all(to_insert)
    db.commit()


def load_space_objects(
    db: Session, page: int = 0, limit: int = 100
) -> list[SpaceObject]:
    """
    Load all space objects from the database.

    Args:
        db: SQLAlchemy session.
        page: Page number for pagination.
        limit: Number of records per page.

    Returns:
        list[SpaceObject]: List of space object instances retrieved from the database.
    """

    results = (
        db.query(SpaceObject)
        .offset(page * limit)
        .limit(limit)
        .options(selectinload(SpaceObject.position), selectinload(SpaceObject.velocity))
        .all()
    )
    return results


def load_satellites(db: Session, page: int = 0, limit: int = 100) -> list[Satellite]:
    """
    Load all satellites from the database.

    Args:
        db: SQLAlchemy session.
        page: Page number for pagination.
        limit: Number of records per page.

    Returns:
        list[Satellite]: List of satellite instances retrieved from the database.
    """
    results = db.query(Satellite).offset(page * limit).limit(limit).all()
    return results
