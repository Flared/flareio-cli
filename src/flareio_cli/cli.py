import dataclasses
import typer

import typing as t


@dataclasses.dataclass
class Command:
    name: str
    callable: t.Callable


def main() -> None:
    app = typer.Typer()

    from flareio_cli.commands.export_tenant_credentials import (
        run_export_tenant_credentials,
    )
    from flareio_cli.commands.export_tenant_events import run_export_tenant_events
    from flareio_cli.commands.help import run_help

    commands: list[Command] = [
        Command(
            name="help",
            callable=run_help,
        ),
        Command(
            name="export-tenant-events",
            callable=run_export_tenant_events,
        ),
        Command(
            name="export-tenant-credentials",
            callable=run_export_tenant_credentials,
        ),
    ]
    for command in commands:
        app.command(name=command.name)(command.callable)

    app()


if __name__ == "__main__":
    main()
