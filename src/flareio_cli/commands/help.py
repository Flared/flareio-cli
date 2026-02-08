import typer


app = typer.Typer()


@app.command()
def help(ctx: typer.Context) -> None:
    root_ctx = ctx.find_root()
    typer.echo(root_ctx.get_help())
