"""Tests for container-aware CLI routing (NixOS container mode).

When container.enable = true in the NixOS module, the activation script
writes a .container-mode metadata file. The host CLI detects this and
execs into the container instead of running locally.
"""
import os
from unittest.mock import MagicMock, patch

import pytest

from kubot_cli.config import (
    get_container_exec_info,
)


# =============================================================================
# get_container_exec_info
# =============================================================================


@pytest.fixture
def container_env(tmp_path, monkeypatch):
    """Set up a fake KUBOT_HOME with .container-mode file."""
    kubot_home = tmp_path / ".kubot"
    kubot_home.mkdir()
    monkeypatch.setenv("KUBOT_HOME", str(kubot_home))
    monkeypatch.delenv("KUBOT_DEV", raising=False)

    container_mode = kubot_home / ".container-mode"
    container_mode.write_text(
        "# Written by NixOS activation script. Do not edit manually.\n"
        "backend=podman\n"
        "container_name=kubot-agent\n"
        "exec_user=kubot\n"
        "kubot_bin=/data/current-package/bin/kubot\n"
    )
    return kubot_home


def test_get_container_exec_info_returns_metadata(container_env):
    """Reads .container-mode and returns all fields including exec_user."""
    with patch("kubot_constants.is_container", return_value=False):
        info = get_container_exec_info()

    assert info is not None
    assert info["backend"] == "podman"
    assert info["container_name"] == "kubot-agent"
    assert info["exec_user"] == "kubot"
    assert info["kubot_bin"] == "/data/current-package/bin/kubot"


# =============================================================================
# exec_in_container (kubot_cli/main_container.py)
# =============================================================================


@pytest.fixture
def docker_container_info():
    return {
        "backend": "docker",
        "container_name": "kubot-agent",
        "exec_user": "kubot",
        "kubot_bin": "/data/current-package/bin/kubot",
    }


def test_exec_in_container_calls_execvp(docker_container_info):
    """Verifies os.execvp is called with correct args: runtime, tty flags,
    user, env vars, container name, binary, and CLI args."""
    from kubot_cli.main_container import exec_in_container

    with patch("shutil.which", return_value="/usr/bin/docker"), \
         patch("subprocess.run") as mock_run, \
         patch("sys.stdin") as mock_stdin, \
         patch("os.execvp") as mock_execvp, \
         patch.dict(os.environ, {"TERM": "xterm-256color", "LANG": "en_US.UTF-8"},
                    clear=False):
        mock_stdin.isatty.return_value = True
        mock_run.return_value = MagicMock(returncode=0)

        exec_in_container(docker_container_info, ["chat", "-m", "opus"])

    mock_execvp.assert_called_once()
    cmd = mock_execvp.call_args[0][1]
    assert cmd[0] == "/usr/bin/docker"
    assert cmd[1] == "exec"
    assert "-it" in cmd
    idx_u = cmd.index("-u")
    assert cmd[idx_u + 1] == "kubot"
    e_indices = [i for i, v in enumerate(cmd) if v == "-e"]
    e_values = [cmd[i + 1] for i in e_indices]
    assert "TERM=xterm-256color" in e_values
    assert "LANG=en_US.UTF-8" in e_values
    assert "kubot-agent" in cmd
    assert "/data/current-package/bin/kubot" in cmd
    assert "chat" in cmd


