### Building with Pex

**DEPRECATED**: PyInstaller is now used as the universal build tool (see [README](../README.md) for details)

[See the Docs](https://pex.readthedocs.io/en/v2.1.102/buildingpex.html)

Pex must be installed in the active environment (it is already included in the pyproject.toml). The
build command specifies a requirements.txt file for dependency installation, a working directory for
bundling source code, and a command that is used for starting the process when invoked. This can all
be done with the following command:

```shell
poetry run pex -r ../requirements.txt -D . -c uvicorn -o ../vipre-api.pex
```

To verify that the application was built successfully, run:

```shell
mv ../vipre-api.pex ~/Downloads
~/Downloads/vipre-api.pex app.main:app
```
