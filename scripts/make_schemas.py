from pathlib import Path
import csv
import json


def make_schema_jsons(path: Path):
    for csv_path in path.glob("*.csv"):
        data = {"tablename": csv_path.stem.split("-")[-1], "note": "TODO", "fields": []}
        with csv_path.open() as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data["fields"].append(row)

        with csv_path.with_suffix(".json").open("w") as json_file:
            json.dump(data, json_file, indent=2)


if __name__ == '__main__':
    schemas = Path().absolute().parent / "schemas"
    print(schemas)
    assert (schemas.exists())

    make_schema_jsons(schemas)
