"""Generate SQLAlchemy models based on the vipre-schemas data model"""

import json
from pathlib import Path

import black
from jinja2 import Environment, PackageLoader

if __name__ == "__main__":
    schemas = Path(__file__).parent.parent.parent.resolve() / "schemas" / "models"
    print(schemas.absolute())
    models = [json.load(f.open()) for f in schemas.glob("*.json")]
    models.sort(key=lambda x: x["tablename"])

    env = Environment(loader=PackageLoader("scripts"))

    template = env.get_template("models.py.jinja")
    rendered = template.render(models=models)
    formatted = black.format_str(
        rendered,
        mode=black.FileMode(line_length=100, magic_trailing_comma=False),
    )
    with (Path(__file__).parent.resolve() / "rendered.models.py").open("w") as f:
        f.write(formatted)
