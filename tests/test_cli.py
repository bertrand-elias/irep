import importlib.metadata

from typer.testing import CliRunner

from irep.cli import app

runner = CliRunner()

def test_version_flag() -> None:
    expected_version = importlib.metadata.version("irep")
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"irep {expected_version}" in result.output