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
