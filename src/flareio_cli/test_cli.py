from click.testing import Result
from flareio_cli.cli import create_app
from typer.testing import CliRunner


def run_test(
    *,
    args: list[str],
) -> Result:
    runner = CliRunner()
    app = create_app()
    result = runner.invoke(app, args)
    return result


def test_app_no_args_is_help() -> None:
    result = run_test(
        args=[],
    )
    assert result.exit_code == 2
    assert "Usage:" in result.output
