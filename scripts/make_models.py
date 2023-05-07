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
