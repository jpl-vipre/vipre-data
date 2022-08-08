# Model Generation

This project includes a code generator to help keep the SQLAlchemy Models in sync with the data
model defined in `vipre-schemas` (see [submodule](../vipre-schemas) in this repo). It does this by
parsing the json schemas for each data model and injecting relevant information into a Jinja
template (see the [template here](./templates/models.py.jinja)). The template defines the necessary
boilerplate and structure for each SQLAlchemy model, creating `Column()`s for each `"field"` in the
data model. The output is then formatted with `black` and written
to [`rendered.models.py`](./rendered.models.py). This can be diffed with the actively
used [`models.py`](../src/sql/models.py) so that any changes from the generation can be inspected
and brought in manually.

## Running the Generator

The generator is a simple python script that can be run any environment with both `black`
and `jinja2` installed (this project defines a virtual environment that can be set up by
running `poetry install`).

Generate the `rendered.models.py` file with:

```shell
poetry run python -m scripts.make_models
```

Inspect the differences between newly rendered and currently used models:

```shell
diff scripts/rendered.models.py vipre_data/sql/models.py
```
