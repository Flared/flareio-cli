import typer

from flareio_cli.commands.export_enant_feed import run_export_tenant_feed


app = typer.Typer()


@app.command()
def help(ctx: typer.Context) -> None:
    root_ctx = ctx.find_root()
    typer.echo(root_ctx.get_help())
    raise typer.Exit()


app.command(name="export-tenant-feed")(run_export_tenant_feed)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
