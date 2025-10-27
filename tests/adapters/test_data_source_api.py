import pytest
from adapters.data_source_api import (
    extract_satellite_data,
    get_satellite_data,
    extract_space_object_data,
)
from tracker.models import Satellite, SpaceObject
from datetime import datetime, timezone


@pytest.fixture(scope="module")
def setup_test_data():
    test_data = [
        {
            "OBJECT_ID": "25544",
            "OBJECT_NAME": "ISS (ZARYA)",
            "EPOCH": "2024-01-01T00:00:00.000",
            "NORAD_CAT_ID": 25544,
            "INCLINATION": 51.6432,
            "ECCENTRICITY": 0.0006703,
            "ARG_OF_PERICENTER": 130.5360,
            "RA_OF_ASC_NODE": 325.0288,
            "ELEMENT_SET_NO": 999,
            "EPHEMERIS_TYPE": 0,
            "MEAN_MOTION": 15.48912345,
            "MEAN_ANOMALY": 325.0288,
            "MEAN_MOTION_DOT": 0.00012345,
            "MEAN_MOTION_DDOT": 0.00000000,
            "REV_AT_EPOCH": 12345,
            "BSTAR": 0.0001234,
            "CLASSIFICATION_TYPE": "U",
            "X": 1234.5,
            "Y": 6789.0,
            "Z": 1011.2,
            "VX": 1.0,
            "VY": 2.0,
            "VZ": 3.0,
        }
    ]
    return test_data

def test_get_satellite_data():
    data = get_satellite_data()
    assert isinstance(data, list)
    assert len(data) > 0
    first_item = data[0]
    expected_keys = {
        "OBJECT_ID",
        "OBJECT_NAME",
        "EPOCH",
        "NORAD_CAT_ID",
        "INCLINATION",
        "ECCENTRICITY",
        "ARG_OF_PERICENTER",
        "RA_OF_ASC_NODE",
        "ELEMENT_SET_NO",
        "EPHEMERIS_TYPE",
        "MEAN_MOTION",
        "MEAN_ANOMALY",
        "MEAN_MOTION_DOT",
        "MEAN_MOTION_DDOT",
        "REV_AT_EPOCH",
        "BSTAR",
        "CLASSIFICATION_TYPE",
    }
    assert set(first_item.keys()) >= expected_keys

def test_extract_space_object_data(setup_test_data):
    data = setup_test_data

    satellites = extract_space_object_data(data)
    assert isinstance(satellites, list)
    assert len(satellites) > 0
    first_object = satellites[0]

    assert isinstance(first_object, SpaceObject)
    assert first_object.id == data[0]["NORAD_CAT_ID"]
    assert first_object.name == data[0]["OBJECT_NAME"]
    assert first_object.epoch.timestamp() == datetime.fromisoformat(data[0]["EPOCH"]).timestamp()
    assert first_object.position.x == 1868.0032467769893
    assert first_object.source == "CELESTRAK"
    assert first_object.position.y == 3811.677524434829
    assert first_object.position.z == 5296.074735418253
    assert first_object.velocity.x == -6.51613678696814
    assert first_object.velocity.y == 3.9971693526230117
    assert first_object.velocity.z == -0.5809016400286962

def test_extract_satellite_data(setup_test_data):
    data = setup_test_data

    satellites = extract_satellite_data(data)
    assert isinstance(satellites, list)
    assert len(satellites) > 0
    first_object = satellites[0]

    assert isinstance(first_object, Satellite)
    assert first_object.object_id == data[0]["OBJECT_ID"]
    assert first_object.object_name == data[0]["OBJECT_NAME"]
    assert first_object.epoch.timestamp() == datetime.fromisoformat(data[0]["EPOCH"]).timestamp()
    assert first_object.norad_cat_id == data[0]["NORAD_CAT_ID"]
    assert first_object.inclination == data[0]["INCLINATION"]
    assert first_object.eccentricity == data[0]["ECCENTRICITY"]
    assert first_object.arg_of_pericenter == data[0]["ARG_OF_PERICENTER"]
    assert first_object.ra_of_asc_node == data[0]["RA_OF_ASC_NODE"]
    assert first_object.element_set_no == data[0]["ELEMENT_SET_NO"]
    assert first_object.ephemeris_type == data[0]["EPHEMERIS_TYPE"]
    assert first_object.mean_motion == data[0]["MEAN_MOTION"]
    assert first_object.mean_anomaly == data[0]["MEAN_ANOMALY"]
    assert first_object.classification_type == data[0]["CLASSIFICATION_TYPE"]
    assert first_object.bstar == data[0]["BSTAR"]
    assert first_object.mean_motion_dot == data[0]["MEAN_MOTION_DOT"]
    assert first_object.rev_at_epoch == data[0]["REV_AT_EPOCH"]

