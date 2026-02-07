# flareio-cli

Beta CLI interface for the [flare.io API](https://api.docs.flare.io/).

## Documentation

The [full CLI documentation](https://api.docs.flare.io/sdk/cli) can be found on Flare's API documentation website.

## Basic Usage

We recommend that you run `flareio-cli` using [uv](https://docs.astral.sh/uv/).

```
$ uvx flareio-cli --help
```

## Configuration

For most commands, the cli requires that you export the `FLARE_API_KEY` environment variable.

## Usage Examples

**Export Tenant Feed to jsonl file**
```
$ export FLARE_API_KEY="<api-key>"
$ uvx run flareio-cli export-tenant-feed --cursor-file=cursor.txt --output-file=output.txt --from-date=2025-01-01
```

## Contributing

We recommend the following dependencies:
- make
- uv
- direnv

Dev commands are defined in `Makefile` and `bin/`.

## Feedback

Do you have ideas or feature requests? Feel free to open issues.
