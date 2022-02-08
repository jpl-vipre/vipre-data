# VIPRE Data

This project will handle data management for the VIPRE Application, including data models, ingestion scripts, and any ad-hoc processing/exploration that needs to be performed.

## Data Fields

Fields extracted from directory/file structure:

```text
body
hEntry
vID
```

Fields from the trajectory header:

```text
Bvec-theta(rad)
Bvec-abs(km)
entryTrajec(boolean)
stateEqu-rX(km)
stateEqu-rY(km)
stateEqu-rZ(km)
stateEqu-vX(km/s)
stateEqu-vY(km/s)
stateEqu-vZ(km/s)
safe(boolean)
entryState-rX(km)
entryState-rY(km)
entryState-rZ(km)
entryState-vX(km/s)
entryState-vY(km/s)
entryState-vZ(km/s)
lon_entry(rad)
lat_entry(rad)
vRot-x(km/s)
vRot-y(km/s)
vRot-z(km/s)
FPA(rad)
vRel_entry-x(km/s)
vRel_entry-y(km/s)
vRel_entry-z(km/s)

Fields from the Body.csv trip parameter headers:

```text
launch (days past J2000)
arrive (days past J2000)
Vinfinity (km/s EMO2000)
y (inferred)
z (inferred)
planet pos (km EMO2000)
y (inferred)
z (inferred)
planet vel (km/s EMO2000)
y (inferred)
z (inferred)
C3 (km2/s2)
DeltaV (km/s)
arrival mass (kg Falcon H Rec + biprop)
flyby body
days past J2000
```

## Data Files

```text
$ tree -L 3
.
├── README.md
├── data
│	├── Neptune
│	│   ├── 00700
│	│   └── 00750
│	│	    ├── Neptune00700-vID1.txt
│	│	    └── ...
│	├── Neptune.csv
│	├── Saturn
│	│	├── 00700
│	│	└── 00750
│	├── Saturn.csv
│	├── Uranus
│	│	├── 00700
│	│	└── 00750
│	└── Uranus.csv
├── data.zip
├── poetry.lock
├── pyproject.toml
└── src
    ├── __init__.py
    ├── ingest.py
    └── models.py
```
