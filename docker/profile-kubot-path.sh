# shellcheck shell=sh
# Installed as /etc/profile.d/kubot.sh. Debian's /etc/profile resets PATH for
# every login shell (`bash -l`, `docker exec <c> bash -l`, ssh, the terminal
# tool's background `bash -lic`), dropping the image's ENV PATH dirs, so bare
# `kubot` exits 127 there. Put them back in the ENV PATH order; dirs a login
# PATH already lists keep their position.
for __kubot_p in /opt/data/.local/bin /opt/kubot/.venv/bin /opt/kubot/bin; do
    case ":$PATH:" in
        *":$__kubot_p:"*) ;;
        *) PATH="$__kubot_p:$PATH" ;;
    esac
done
unset __kubot_p
export PATH
