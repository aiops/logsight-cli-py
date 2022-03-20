from click.testing import CliRunner

from src.logsight_cli import cli


def test_config():
    runner = CliRunner()
    result = runner.invoke(cli, ['config'], obj={})
    assert result.exit_code == 0
    assert 'EMAIL' in result.output


def test_application():
    runner = CliRunner()
    result = runner.invoke(cli, ['application', 'ls'], obj={})
    assert result.exit_code == 0
    assert 'APPLICATION' in result.output


if __name__ == '__main__':
    test_config()