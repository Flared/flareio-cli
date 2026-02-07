# flareio-cli

`flareio-cli` is a beta CLI interface for the [flare.io API](https://api.docs.flare.io/).

The [full CLI documentation](https://api.docs.flare.io/sdk/cli) can be found on Flare's API documentation website.

## Installing

`flareio-cli` is [available on PyPI](https://pypi.org/project/flareio-cli/), you can install it using:
```
pip install flareio-cli
```

However, we recommend that you invoke it using [uv](https://docs.astral.sh/uv/). Example:
```
uvx flareio-cli --help
```

## Configuration

For most commands, the cli requires that you export the `FLARE_API_KEY` environment variable.

## Usage Example

Export Tenant Feed to jsonl file:
```
export FLARE_API_KEY="<api-key>"

uvx run flareio-cli export-tenant-feed \
    --cursor-file=cursor.txt \
    --output-file=output.txt \
    --from-date=2025-01-01
```

## Contributing

We recommend the following dependencies:
- `make`
- `uv`
- `direnv`

The `Makefile` contains the following targets:
- `make test` will run tests
- `make check` will run typechecking
- `make format` format will format the code
- `make format-check` will run linting
- `make ci` will run CI equivalent

## Feedback

Do you have ideas or feature requests? Feel free to open issues.
