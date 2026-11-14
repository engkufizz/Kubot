"""Resolve KUBOT_HOME for standalone skill scripts.

Skill scripts may run outside the Kubot process (e.g. system Python,
nix env, CI) where ``kubot_constants`` is not importable.  This module
provides the same ``get_kubot_home()`` and ``display_kubot_home()``
contracts as ``kubot_constants`` without requiring it on ``sys.path``.

When ``kubot_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``kubot_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``KUBOT_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from kubot_constants import display_kubot_home
    from kubot_constants import get_kubot_home
except (ModuleNotFoundError, ImportError):

    def get_kubot_home() -> Path:
        """Return the Kubot home directory (default: ~/.kubot).

        Mirrors ``kubot_constants.get_kubot_home()``."""
        val = os.environ.get("KUBOT_HOME", "").strip()
        return Path(val) if val else Path.home() / ".kubot"

    def display_kubot_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``kubot_constants.display_kubot_home()``."""
        home = get_kubot_home()
        try:
            return "~/" + home.relative_to(Path.home()).as_posix()
        except ValueError:
            return str(home)
