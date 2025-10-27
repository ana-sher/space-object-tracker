from dataclasses import asdict
from typing import Any, Optional, TypeVar

from sqlalchemy import Engine, insert
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, selectinload

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


def save_or_skip(objects: list[T], db_engine: Engine, pkey: Optional[str] = None):
    """
    Bulk save or skip a list of T to the database.

    Args:
        objects (list[T]): List of T instances to save.
        db_engine (Engine): SQLAlchemy database engine.
        pkey (Optional[str]): Primary key attribute name. If None, the first primary key of the model will be used.
    """
    if not objects:
        return

    model_type: Any = objects[0].__class__

    if pkey is None:
        mapper = inspect(model_type)
        if not mapper:
            return
        pk_attr = mapper.primary_key[0]
        pkey = pk_attr.key

    if pkey is None:
        return

    ids = [getattr(obj, pkey) for obj in objects]

    with Session(db_engine) as session:
        existing_ids = {
            id_[0] for id_ in session.query(pk_attr).filter(pk_attr.in_(ids)).all()
        }
        to_insert = [o for o in objects if getattr(o, pkey) not in existing_ids]

        if not to_insert:
            return
        values = [asdict(o) for o in to_insert]  # type: ignore
        query = insert(model_type).values(values)
        session.execute(query)
        session.commit()


def load_space_objects(db_engine: Engine, page: int = 0, limit: int = 100) -> list[SpaceObject]:
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
            .offset(page * limit).limit(limit)
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
