import typer


def create_app() -> typer.Typer:
    app = typer.Typer(
        no_args_is_help=True,
    )

    from flareio_cli.commands.export_identifier_credentials import (
        app as export_identifier_credentials_app,
    )
    from flareio_cli.commands.export_tenant_credentials import (
        app as export_tenant_credentials_app,
    )
    from flareio_cli.commands.export_tenant_events import (
        app as export_tenant_events_app,
    )
    from flareio_cli.commands.help import app as help_app
    from flareio_cli.commands.version import app as version_app

    for cmd_app in [
        export_identifier_credentials_app,
        export_tenant_credentials_app,
        export_tenant_events_app,
        help_app,
        version_app,
    ]:
        app.add_typer(cmd_app)

    return app


def main() -> None:
    app = create_app()
    app()


if __name__ == "__main__":
    main()
