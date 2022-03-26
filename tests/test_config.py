from click.testing import CliRunner

from logsight_cli.logsight_cli import cli


AUTH = ['--email', 'jorge.cardoso.pt@gmail.com', '--password', 'xymneq-jasqA9-faxtyz']


def test_config():
    runner = CliRunner()
    result = runner.invoke(cli, AUTH + ['config'], obj={})
    assert result.exit_code == 0
    assert 'EMAIL' in result.output


def test_application():
    runner = CliRunner()
    result = runner.invoke(cli, AUTH + ['application', 'ls'], obj={})
    assert result.exit_code == 0
    assert 'APPLICATION' in result.output


if __name__ == '__main__':
    test_config()
