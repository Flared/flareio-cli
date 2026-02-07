# flareio-cli

`flareio-cli` is a beta CLI interface for the [flare.io API](https://api.docs.flare.io/).

The [full CLI documentation](https://api.docs.flare.io/sdk/cli) can be found on Flare's API documentation website.

## Installing

`flareio-cli` is [available on PyPI](https://pypi.org/project/flareio-cli/).
You may find all available versions on the Github [releases](https://github.com/Flared/flareio-cli/releases) page.

Invoke it directly using [uv](https://docs.astral.sh/uv/) (recommended):
```bash
# Running the most recent version.
uvx flareio-cli --help

# Running a specific version. Recommended to ensure stability.
# Example: uvx flareio-cli@0.5.0 --help
uvx flareio-cli@version --help
```

Or install it:
```bash
# Using uv
uv tool install flareio-cli

# Using pip
pip install flareio-cli
```

## Usage Example

Export Tenant Feed to CSV file:
```
export FLARE_API_KEY="<api-key>"

uvx run flareio-cli export-tenant-feed \
    --cursor-file=cursor.txt \
    --output-file=output.csv \
    --from-date=2025-01-01
```

Learn more in the [full CLI documentation](https://api.docs.flare.io/sdk/cli).

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
