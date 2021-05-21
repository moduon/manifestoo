import textwrap

from typer.testing import CliRunner

from manifestoo.__main__ import app

from .common import populate_addons_dir


def test_integration(tmp_path):
    addons = {
        "a": {"version": "13.0.1.0.0", "depends": ["b", "c"]},
        "b": {"depends": ["base"]},
        "c": {"depends": ["account", "b"]},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        ["--select=a", f"--addons-path={tmp_path}", "tree"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == textwrap.dedent(
        """\
            a (13.0.1.0.0)
            ├── b (no version)
            │   └── base (✘ not installed)
            └── c (no version)
                ├── account (✘ not installed)
                └── b ⬆
        """
    )
