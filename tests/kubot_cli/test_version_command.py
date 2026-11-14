"""Tests for the /version slash command."""

from unittest.mock import patch

from cli import KubotCLI






def test_process_command_version_prints_version_info():
    cli_obj = KubotCLI.__new__(KubotCLI)

    with patch("kubot_cli.main._print_version_info") as mock_print:
        assert cli_obj.process_command("/version") is True

    mock_print.assert_called_once_with(check_updates=True)
