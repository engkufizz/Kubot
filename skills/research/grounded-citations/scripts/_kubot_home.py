"""Resolve KUBOT_HOME for standalone skill scripts.

Skill scripts may run outside the Kubot process (system Python, nix env,
CI) where ``kubot_constants`` is not importable.  This module provides the
same ``get_kubot_home()`` contract without requiring it on ``sys.path``.

When ``kubot_constants`` IS available it is used directly so profile
resolution and any future enhancements are picked up automatically.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from kubot_constants import get_kubot_home
except (ModuleNotFoundError, ImportError):

    def get_kubot_home() -> Path:
        """Return the Kubot home directory (default: ``~/.kubot``)."""
        val = os.environ.get("KUBOT_HOME", "").strip()
        return Path(val) if val else Path.home() / ".kubot"
