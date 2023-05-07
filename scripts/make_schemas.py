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

from pathlib import Path
import csv
import json


def make_schema_jsons(path: Path):
    for csv_path in path.glob("VIPRE Database Values*.csv"):
        # Read in the csv file
        with csv_path.open() as csv_file:
            # Capture note header
            note_header: str = csv_file.__next__()
            note: str = note_header.split(",")[1]
            csv_file.__next__()
            reader = csv.DictReader(csv_file)
            rows: list[dict[str, str]] = [row for row in reader]

        tablename = csv_path.stem.split("-")[-1].strip().lower()
        # Read the existing json file to preserve any hand-edits
        json_file = csv_path.parent / f"vipre_schema-{tablename}.json"
        if json_file.exists():
            with json_file.open() as f:
                data = json.load(f)
        else:
            # Initialize metadata values if json file did not already exist
            data = {"tablename": tablename, "note": note, "fields": []}
        with json_file.open("w") as json_file:
            data["fields"] = rows  # Attach the fields we read in from csv file
            json.dump(data, json_file, indent=2)


if __name__ == "__main__":
    schemas = Path().absolute().parent / "vipre-schemas/sheets"
    print(schemas)
    assert schemas.exists()

    make_schema_jsons(schemas)
