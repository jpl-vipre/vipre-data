"""Generate SQLAlchemy models based on the vipre-schemas data model"""

import json
from pathlib import Path

import black
from jinja2 import Environment, PackageLoader

if __name__ == "__main__":
    schemas = Path(__file__).parent.parent.resolve() / "vipre-schemas" / "models"
    version_file = schemas.parent / "VERSION"
    if version_file.exists():
        version = version_file.open().read().strip()
    else:
        version = ""
    print(schemas.absolute())
    models = [json.load(f.open()) for f in schemas.glob("*.json")]
    models.sort(key=lambda x: x["tablename"])

    env = Environment(loader=PackageLoader("scripts"))

    template = env.get_template("models.py.jinja")
    rendered = template.render(models=models, version=version)
    formatted = black.format_str(
        rendered,
        mode=black.FileMode(line_length=100, magic_trailing_comma=False),
    )
    with (Path(__file__).parent.resolve() / "rendered.models.py").open("w") as f:
        f.write(formatted)
