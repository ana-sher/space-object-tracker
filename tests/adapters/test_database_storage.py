import copy
from datetime import datetime

from sqlalchemy.orm import Session

from adapters.database_storage import save_or_skip
from tracker.models import Satellite, SpaceObject, Vector3D


def test_save_space_objects(test_engine):
    space_object = SpaceObject(
        id=1,
        name="Test Object",
        epoch=datetime.now(),
        position=Vector3D(x=1000.0, y=2000.0, z=3000.0),
        velocity=Vector3D(x=1.0, y=2.0, z=3.0),
        source="CELESTRAK",
    )

    save_or_skip([copy.deepcopy(space_object)], test_engine)
    session = Session(test_engine)
    loaded_objects = session.query(SpaceObject).all()

    assert len(loaded_objects) == 1
    assert loaded_objects[0].id == space_object.id
    assert loaded_objects[0].name == space_object.name
    assert loaded_objects[0].epoch == space_object.epoch
    assert loaded_objects[0].position.x == space_object.position.x
    assert loaded_objects[0].position.y == space_object.position.y
    assert loaded_objects[0].position.z == space_object.position.z
    assert loaded_objects[0].velocity.x == space_object.velocity.x
    assert loaded_objects[0].velocity.y == space_object.velocity.y
    assert loaded_objects[0].velocity.z == space_object.velocity.z
    assert loaded_objects[0].source == space_object.source
    session.close()


def test_save_satellites(test_engine):
    satellite = Satellite(
        object_name="ZHIHUI TIANWANG-1 01A",
        object_id="2024-087A",
        bstar=0.0001,
        inclination=98.7,
        epoch=datetime.now(),
        mean_motion=14.5,
        eccentricity=0.001,
        mean_anomaly=45.0,
        ra_of_asc_node=150.0,
        arg_of_pericenter=250.0,
        classification_type="U",
        ephemeris_type=0,
        norad_cat_id=12345,
        rev_at_epoch=100,
        element_set_no=999,
        mean_motion_ddot=0,
        mean_motion_dot=0.03,
    )

    save_or_skip([copy.deepcopy(satellite)], test_engine)
    session = Session(test_engine)
    loaded_objects = session.query(Satellite).all()

    assert len(loaded_objects) == 1
    assert loaded_objects[0].object_name == satellite.object_name
    assert loaded_objects[0].object_id == satellite.object_id
    assert loaded_objects[0].norad_cat_id == satellite.norad_cat_id
    assert loaded_objects[0].epoch == satellite.epoch
    assert loaded_objects[0].mean_motion == satellite.mean_motion
    assert loaded_objects[0].eccentricity == satellite.eccentricity
    assert loaded_objects[0].inclination == satellite.inclination
    assert loaded_objects[0].ra_of_asc_node == satellite.ra_of_asc_node
    assert loaded_objects[0].arg_of_pericenter == satellite.arg_of_pericenter
    assert loaded_objects[0].mean_anomaly == satellite.mean_anomaly
    assert loaded_objects[0].ephemeris_type == satellite.ephemeris_type
    assert loaded_objects[0].classification_type == satellite.classification_type
    assert loaded_objects[0].rev_at_epoch == satellite.rev_at_epoch
    assert loaded_objects[0].element_set_no == satellite.element_set_no
    assert loaded_objects[0].bstar == satellite.bstar
    assert loaded_objects[0].mean_motion_dot == satellite.mean_motion_dot
    assert loaded_objects[0].mean_motion_ddot == satellite.mean_motion_ddot
    session.close()


def test_save_and_skip_space_objects(test_engine):
    space_object = SpaceObject(
        id=1,
        name="Test Object",
        epoch=datetime.now(),
        position=Vector3D(x=1000.0, y=2000.0, z=3000.0),
        velocity=Vector3D(x=1.0, y=2.0, z=3.0),
        source="CELESTRAK",
    )

    save_or_skip([copy.deepcopy(space_object)], test_engine)
    changed_space_object = copy.deepcopy(space_object)
    changed_space_object.name = "Changed Name"
    save_or_skip([copy.deepcopy(changed_space_object)], test_engine)
    session = Session(test_engine)
    loaded_objects = session.query(SpaceObject).all()

    assert len(loaded_objects) == 1
    assert loaded_objects[0].id == space_object.id
    assert loaded_objects[0].name == space_object.name
    assert loaded_objects[0].epoch == space_object.epoch
    assert loaded_objects[0].position.x == space_object.position.x
    assert loaded_objects[0].position.y == space_object.position.y
    assert loaded_objects[0].position.z == space_object.position.z
    assert loaded_objects[0].velocity.x == space_object.velocity.x
    assert loaded_objects[0].velocity.y == space_object.velocity.y
    assert loaded_objects[0].velocity.z == space_object.velocity.z
    assert loaded_objects[0].source == space_object.source
    session.close()


def test_save_and_skip_space_objects_add_new(test_engine):
    space_object = SpaceObject(
        id=1,
        name="Test Object",
        epoch=datetime.now(),
        position=Vector3D(x=1000.0, y=2000.0, z=3000.0),
        velocity=Vector3D(x=1.0, y=2.0, z=3.0),
        source="CELESTRAK",
    )

    save_or_skip([copy.deepcopy(space_object)], test_engine)
    changed_space_object = copy.deepcopy(space_object)
    changed_space_object.name = "Changed Name"
    save_or_skip([copy.deepcopy(changed_space_object)], test_engine)
    changed_space_object.epoch = datetime.now()
    save_or_skip([copy.deepcopy(changed_space_object)], test_engine)
    session = Session(test_engine)
    loaded_objects = session.query(SpaceObject).all()

    assert len(loaded_objects) == 2
    assert loaded_objects[0].id == space_object.id
    assert loaded_objects[0].name == space_object.name
    assert loaded_objects[0].epoch == space_object.epoch
    assert loaded_objects[0].position.x == space_object.position.x
    assert loaded_objects[0].position.y == space_object.position.y
    assert loaded_objects[0].position.z == space_object.position.z
    assert loaded_objects[0].velocity.x == space_object.velocity.x
    assert loaded_objects[0].velocity.y == space_object.velocity.y
    assert loaded_objects[0].velocity.z == space_object.velocity.z
    assert loaded_objects[0].source == space_object.source

    assert loaded_objects[1].epoch == changed_space_object.epoch
    assert loaded_objects[1].name == changed_space_object.name
    session.close()
