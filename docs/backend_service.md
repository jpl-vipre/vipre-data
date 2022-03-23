# Backend Services Discussion

**Date**: *3/23/22*

**Participants**: *Damon, Alex, Michael, Ryan*

## Objective

Discuss requirements of the backend service (`vipre-data`) and target a development plan (language, paradigm, etc.).

## Context

The long and short of it is: the Electron App will include everything a user needs to run the program on their computer; we have no idea what “their computer” will look like and thus packaging things is very important. As an interpreted language, Python is much more prone to runtime errors and also relies on a clean environment in which to run. Additionally, it’s quite slow and could bog down the fluidity of the visualization.

In contrast, Golang is a highly-performant, compiled language and would be much easier to distribute as a binary executable that our electron app fires up upon starting. The drawback is that it is not as commonly used among the science community and thus may be ill-suited to performing “on-the-fly” calculations (those done by vipre-gen) if we decide to move some of those calcs out of the matlab scripts/database schema.

I think the main discussion to have here is what overlap are we expecting/requiring between the mathematical calculations (vipre-gen), and the visualization app (vipre-vis + vipre-data).

Personally, I would advocate for a complete separation of these things and keep all the data needed for visualization inside the database. More specifically:

- `vipre-gen` (matlab) generates all the necessary data and writes to `vipre-db`
- `vipre-db` (sqlite database) has all the data that the frontend (`vipre-vis`) will want to show
- `vipre-vis` (React App) will present visualizations and filter options to the user, requesting necessary data from `vipre-data`
- `vipre-data` (REST API, Python or Go) will listen for http requests for data (made by `vipre-vis` or others), interpret those, and fetch the necessary raw data from vipre-db, formatting it as json in an http response

## Discussion

- In addition to showing the values computed by MatLab and stored in the database (trajectories, flybys, entries, etc.), VIPRE will also ned to display trajectory hyperbola, and other values which are computed on-the-fly for a single, selected point. These values should not be pre-computed due to their computational simplicity yet large dimensionality.
- VIPRE will also make use of many other scripts and tools that have been developed by scientists at JPL; most of these have been written in Python or with Python in mind.
- Additionally, the support/maintenance plan for VIPRE is uncertain, but it is likely that TeamX will be interested in this tool; they use Python for all of their development and thus would be most comfortable supporting a tool written in Python.
- Alex is comfortable with Python and can easily translate as much of the MatLab code as is helpful to Python/Numpy functions.
- Damon is also working on the development of other related tools that will be written in/executed by Python. It is possible that these tools may be integrated at some point in the future.
- Expected users will be comfortable with Python
- Expected users will likely *not* have Docker installed
- Expected users will include many Windows environments

## Outcome

- The backend service `vipre-data` will use a combination of pre-computed values and on-the-fly calculations to serve the data requests of the front-end.
- This will all be done in Python to support maintenance and adaptability in the future.
- `vipre-data` will expose a REST API over http to serve such data requests.
- Alex will develop a library to perform these on-the-fly calculations that will be called by `vipre-data` when needed.
- Ryan will provide a draft API spec that outlines some of the data requests he will need to make from the front-end application.
- Michael will develop a REST API using Python (FastAPI) to answer these requests.
