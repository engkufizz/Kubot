"""Login shells in the image keep Kubot' own dirs on PATH.

Debian's ``/etc/profile`` resets PATH for every login shell, so without
``/etc/profile.d/kubot.sh`` a ``bash -l`` (``docker exec <c> bash -l``, ssh, the
terminal tool's background ``bash -lic``) lost ``/opt/kubot/bin`` and bare
``kubot`` exited 127 (#56634).
"""
from __future__ import annotations

import subprocess


def test_login_shell_resolves_kubot_to_the_image_shim(built_image: str) -> None:
    r = subprocess.run(
        ["docker", "run", "--rm", "-u", "kubot", "--entrypoint", "bash", built_image,
         "-lc", 'echo "kubot=$(command -v kubot)"; echo "path=$PATH"'],
        capture_output=True, text=True, timeout=60, check=False,
    )
    assert r.returncode == 0, r.stderr
    lines = dict(line.split("=", 1) for line in r.stdout.splitlines() if "=" in line)
    assert lines["kubot"] == "/opt/kubot/bin/kubot"
    entries = lines["path"].split(":")
    assert entries.index("/opt/kubot/bin") < entries.index("/opt/kubot/.venv/bin")
    assert entries.count("/opt/kubot/bin") == 1
