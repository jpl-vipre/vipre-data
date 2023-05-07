# Copyright (c) 2021-2023 California Institute of Technology ("Caltech"). U.S.
# Government sponsorship acknowledged.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Caltech nor its operating division, the Jet Propulsion
#   Laboratory, nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written
#   permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.sql import crud, models

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
)


@router.post("/", response_model=list[schemas.response.Entry], response_model_exclude_unset=False)
def query_entries(req: schemas.request.EntryRequest, db: Session = Depends(deps.get_db)):
    query = crud.make_query(db, models.Entry, req.filters, req.fields, req.limit)
    result = query.all()
    return result


# @router.post(
#     "/{trajectory_id}",
#     response_model=list[schemas.Entry],
#     response_model_exclude_unset=False,
# )
# def query_trajectory_entries(
#     trajectory_id: int, req: schemas.EntryRequest, db: Session = Depends(deps.get_db)
# ):
#     query = crud.query_entries(db, req.filters, req.fields, req.limit, trajectory_id)
#     result = query.all()
#     print(result)
#     return result


@router.get("/{entry_id}", response_model=schemas.response.EntryFull)
def get_entry(entry_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_entry(db, entry_id)
    entry = schemas.response.EntryFull.from_orm(result)
    entry.mission_delta_v = result.trajectory.interplanetary_dv + sum(
        m.dv_maneuver_mag for m in result.maneuvers
    )
    # entry.trajectory = schemas.response.TrajectoryFull.from_orm(result.trajectory)
    return entry


@router.get("/{entry_id}/datarates", response_model=list[schemas.response.DataRate])
def get_entry(entry_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_datarates(db, entry_id)
    return result
