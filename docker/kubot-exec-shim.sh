#!/bin/sh
# shellcheck shell=sh
# /opt/kubot/bin/kubot — `docker exec` privilege-drop shim.
#
# Background
# ----------
# The s6 image runs the supervised gateway/main process as the unprivileged
# `kubot` user (UID 10000). When an operator runs `docker exec <c> kubot ...`
# the default UID is root (0), and any file the command writes under
# $KUBOT_HOME — auth.json, .env, config.yaml — ends up root-owned and
# unreadable to the supervised gateway. The most common manifestation: the
# user runs `docker exec <c> kubot login`, this writes
# /opt/data/auth.json as root:root mode 0600, and from then on the gateway
# returns "Provider authentication failed: Kubot is not logged into Nous
# Portal" on every incoming message — even though `docker exec <c> kubot
# chat -q ping` (also running as root) succeeds because root happens to be
# able to read its own root-owned file. See systematic-debugging skill
# notes attached to this fix.
#
# Fix
# ---
# This shim sits at /opt/kubot/bin/kubot and is placed earliest on PATH.
# When invoked as root, it drops to the kubot user (via s6-setuidgid)
# before exec'ing the real venv binary, so anything that writes under
# $KUBOT_HOME is uid-aligned with the supervised processes. When invoked
# as any non-root UID — including the supervised processes themselves,
# `docker exec --user kubot`, kanban subagents, etc. — it short-circuits
# straight to the venv binary with no privilege change. Net: one extra
# fork on the docker-exec-as-root path, zero behavioral change on every
# other path.
#
# Recursion safety: the shim exec's the venv binary by *absolute path*
# (/opt/kubot/.venv/bin/kubot), so the second hop cannot re-enter this
# shim regardless of PATH state. No sentinel env var needed.
#
# Opt-out: set KUBOT_DOCKER_EXEC_AS_ROOT=1 (1/true/yes, case-insensitive)
# to keep running as root. Reserved for diagnostic sessions where the
# operator deliberately wants root semantics — e.g. inspecting root-only
# state via the kubot CLI. Default is to drop.

set -e

REAL=/opt/kubot/.venv/bin/kubot

# Defensive: if the venv binary is missing (corrupted image, partial
# install), fail loudly rather than silently masking it.
if [ ! -x "$REAL" ]; then
    echo "kubot-shim: $REAL not found or not executable" >&2
    exit 127
fi

# Already non-root? Just exec the real binary. This is the hot path for
# supervised processes (uid 10000) and for `docker exec --user kubot`.
if [ "$(id -u)" != "0" ]; then
    exec "$REAL" "$@"
fi

# Root, with opt-out set? Honor it.
case "${KUBOT_DOCKER_EXEC_AS_ROOT:-}" in
    1|true|TRUE|True|yes|YES|Yes)
        exec "$REAL" "$@"
        ;;
esac

# Root, no opt-out. Drop to the kubot user.
#
# s6-setuidgid lives under /command/ which is NOT on `docker exec`'s PATH
# (s6-overlay only puts /command/ on PATH for supervision-tree children).
# Reference it by absolute path so the drop is robust against PATH
# manipulation.
S6_SUID=/command/s6-setuidgid
if [ ! -x "$S6_SUID" ]; then
    # Non-s6 image (someone stripped s6-overlay, or a hand-built variant).
    # Fail loud rather than silently re-execing as root and leaking the
    # bug this shim exists to prevent.
    echo "kubot-shim: $S6_SUID not found; refusing to silently run as root." >&2
    echo "kubot-shim: re-run with --user kubot or set KUBOT_DOCKER_EXEC_AS_ROOT=1." >&2
    exit 126
fi

# Reset HOME to the kubot user's home before dropping privileges. Without
# this, $HOME stays /root and any library that resolves paths off $HOME
# (XDG caches, lockfiles, .config writes) will try to write to /root and
# fail with EACCES. Mirrors main-wrapper.sh.
export HOME=/opt/data

exec "$S6_SUID" kubot "$REAL" "$@"
