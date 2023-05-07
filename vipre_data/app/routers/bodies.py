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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.sql import crud

router = APIRouter(
    prefix="/bodies",
    tags=["bodies"],
)


@router.get("/", response_model=list[schemas.response.Body])
def get_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)


@router.get("/targeted", response_model=list[schemas.response.BodySummary])
def get_targeted_bodies(db: Session = Depends(deps.get_db)):
    """
    Retrieve the set of all targeted bodies in the database.

    Targeted bodies are those for which there exist some trajectories terminating at the body.
    There may be other bodies present in the sequence of flybys that are never present as the
    ultimate destination of a trajectory (e.g. not a target body)
    """
    return crud.get_targeted_bodies(db)


@router.get("/body/{body_id}", response_model=schemas.response.Body)
def get_body(body_id: int, db: Session = Depends(deps.get_db)):
    bodies = crud.get_bodies(db, body_id=body_id)
    if len(bodies) == 0:
        raise HTTPException(404, f"No body was found with the ID: {body_id}")
    return bodies[0]


@router.get("/list", response_model=list[schemas.response.BodySummary])
def list_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)


@router.get("/architecture", response_model=list[schemas.response.BodySummary])
def get_architecture(architecture_sequence: str, db: Session = Depends(deps.get_db)):
    bodies = [
        crud.get_bodies(db, int(body_id.strip())) for body_id in architecture_sequence.split("-")
    ]
