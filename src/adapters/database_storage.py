from typing import Any, TypeVar

from sqlalchemy import Engine, and_
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Mapper, Session, selectinload

from tracker.models import Satellite, SpaceObject

T = TypeVar("T")


def save(objects: list[T], db_engine: Engine):
    """
    Save a list of T to the database.

    Args:
        objects (list[T]): List of object instances to save.
        db_engine (Engine): SQLAlchemy database engine.
    """
    with Session(db_engine) as session:
        session.add_all(objects)
        session.commit()


def save_or_skip(objects: list[T], db_engine: Engine):
    """
    Bulk save or skip a list of T to the database.

    Args:
        objects (list[T]): List of T instances to save.
        db_engine (Engine): SQLAlchemy database engine.
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

    with Session(db_engine) as session:
        existing_ids = [
            existing_pks
            for existing_pks in session.query(*pk_attrs)
            .filter(
                *[
                    and_(
                        *[pk_attr == ids_m[i][j] for i, pk_attr in enumerate(pk_attrs)]
                    )
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
        session.add_all(to_insert)
        session.commit()


def load_space_objects(
    db_engine: Engine, page: int = 0, limit: int = 100
) -> list[SpaceObject]:
    """
    Load all space objects from the database.

    Args:
        db_engine (Engine): SQLAlchemy database engine.
        page (int): Page number for pagination.
        limit (int): Number of records per page.

    Returns:
        list[SpaceObject]: List of space object instances retrieved from the database.
    """
    with Session(db_engine) as session:
        results = (
            session.query(SpaceObject)
            .offset(page * limit)
            .limit(limit)
            .options(
                selectinload(SpaceObject.position), selectinload(SpaceObject.velocity)
            )
            .all()
        )
    return results


def load_satellites(
    db_engine: Engine, page: int = 0, limit: int = 100
) -> list[Satellite]:
    """
    Load all satellites from the database.

    Args:
        db_engine (Engine): SQLAlchemy database engine.
        page (int): Page number for pagination.
        limit (int): Number of records per page.

    Returns:
        list[Satellite]: List of satellite instances retrieved from the database.
    """
    with Session(db_engine) as session:
        results = session.query(Satellite).offset(page * limit).limit(limit).all()
    return results
