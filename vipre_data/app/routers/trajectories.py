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
    prefix="/trajectories",
    tags=["trajectories"],
)


@router.post(
    "/", response_model=list[schemas.response.Trajectory], response_model_exclude_unset=True
)
def get_trajectories(req: schemas.request.TrajectoryRequest, db: Session = Depends(deps.get_db)):
    query = crud.make_query(db, models.Trajectory, req.filters, req.fields, req.limit)
    result = query.all()
    return result


@router.get("/{trajectory_id}", response_model=schemas.response.TrajectoryFull)
def get_trajectory(trajectory_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_trajectory(db, trajectory_id)
    return result


@router.get("/{trajectory_id}/entries", response_model=list[schemas.response.Entry])
def get_trajectory_entries(
    trajectory_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(deps.get_db)
):
    result = crud.get_trajectory_entries(db, trajectory_id, limit, offset)
    # TODO: add LatLongH field to all the entries
    return result


@router.get("/{trajectory_id}/entries/count", response_model=int)
def count_trajectory_entries(trajectory_id: int, db: Session = Depends(deps.get_db)):
    result = crud.count_trajectory_entries(db, trajectory_id)
    return result
