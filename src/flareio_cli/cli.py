import dataclasses
import typer

import typing as t


@dataclasses.dataclass
class Command:
    name: str
    callable: t.Callable


def create_app() -> typer.Typer:
    app = typer.Typer(
        no_args_is_help=True,
    )

    from flareio_cli.commands.export_identifier_credentials import (
        run_export_identifier_credentials,
    )
    from flareio_cli.commands.export_tenant_credentials import (
        run_export_tenant_credentials,
    )
    from flareio_cli.commands.export_tenant_events import run_export_tenant_events
    from flareio_cli.commands.help import run_help
    from flareio_cli.commands.version import run_version

    commands: list[Command] = [
        Command(
            name="help",
            callable=run_help,
        ),
        Command(
            name="version",
            callable=run_version,
        ),
        Command(
            name="export-tenant-events",
            callable=run_export_tenant_events,
        ),
        Command(
            name="export-tenant-credentials",
            callable=run_export_tenant_credentials,
        ),
        Command(
            name="export-identifier-credentials",
            callable=run_export_identifier_credentials,
        ),
    ]
    for command in commands:
        app.command(name=command.name)(command.callable)

    return app


def main() -> None:
    app = create_app()
    app()


if __name__ == "__main__":
    main()
