from click.testing import CliRunner

from logsight_cli.logsight_cli import cli

AUTH = ['--json', '--email', 'logsight.testing.001@gmail.com', '--password', 'hibhiv-5hurce-zovnyG']


def test_config():
    runner = CliRunner()
    result = runner.invoke(cli, AUTH + ['config'], obj={})
    assert result.exit_code == 0
    assert 'EMAIL' in result.output
    assert AUTH[2] in result.output
    assert AUTH[4] in result.output


def test_compare_ls():
    runner = CliRunner()
    result = runner.invoke(cli, AUTH + ['compare', 'ls'], obj={})
    assert result.exit_code == 0


if __name__ == '__main__':
    test_config()

