# Space Object Tracker

Storing historical OMM/TLE satelite data, transforms to calculated spatial and temporal properties via SGP4 for future analysis and prediction. Data being accessible and available via API endpoints, runnable locally via Docker. Unit testing via PyTest.

## Features

- Read OMM from source (Celestrak)
- Orbit propagation (SGP4)
- Storing and retrieval of historical data via API endpoints (FastAPI)

## Planned Features
Tracking, analyzing and predicting the behavior of artificial satellites and debris. Focus areas: orbital pattern analysis, risk assessment, tracking evolution and orbital decay prediction, and flexible filtering pipelines.

- Orbital pattern analysis (clustering, classification of orbital regimes)
- Collision risk evaluation
- Orbital decay prediction and lifetime estimation
- Filter dataset (by altitude, inclination, operator, NORAD ID, lifetime, custom rules)
- CLI and Python API for batch processing and experiments

## Algorithms & methods

- Propagation: SGP4
- Risk assessment: closest approach calculation
- Decay prediction
- Filtering: endpoint with JSON filters object

## Quickstart

1. Install

```
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

2. Run db initialization, DataFrame console output

```
python src/main.py
```

3. (optional) Run API

Locally:

```
fastapi dev src/application/api.py
```

Docker:

```
docker build -t space-object-tracker-image .
docker run -d --name space-object-tracker-image -p 8000:80 space-object-tracker
```

Swagger Docs: <http://127.0.0.1:8000/docs>

## Data sources

- Celestrak (OMM): public OMM files and collections

## Examples

- analyze how many satellites operate in low-Earth orbit (LEO)
- find objects decaying within 180 days
- monitor certain NORAD IDs for collision risk

## Testing & validation

- unit tests in tests/

To run tests:

```
pytest
```

(- sample datasets for backtesting in tests/data)
(- CI should run propagation consistency and scoring regressions)
