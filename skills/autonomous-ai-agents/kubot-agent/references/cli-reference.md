# Kubot CLI Reference

Live sources when anything looks stale: `kubot --help`, `kubot <command> --help`,
https://kubot-agent.nousresearch.com/docs/reference/cli-commands

### Global Flags

```
kubot [flags] [command]        (no subcommand = interactive chat)

  --version, -V             Show version
  -z, --oneshot PROMPT      One-shot: print ONLY the final response (for scripts/pipes)
  -m MODEL  --provider P    Model/provider override for this invocation
  -t, --toolsets LIST       Comma-separated toolsets for this invocation
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --tui / --cli             Force the Ink TUI / classic REPL
  --ignore-rules            Skip AGENTS.md/SOUL.md/memory/skill injection
  --safe-mode               Disable ALL customizations (troubleshooting)
  --pass-session-id         Include session ID in system prompt
```

### Chat

```
kubot chat [flags]
  -q, --query TEXT          Single query, non-interactive
  --image PATH              Attach a local image to a single query
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --max-turns N             Cap tool-calling iterations
  --source TAG              Session source tag (default: cli)
```
(plus the global flags above)

### Configuration

```
kubot setup [section]      Wizard (model|tts|terminal|gateway|tools|agent)
kubot model                Interactive model/provider picker
kubot fallback [add|remove|list]  Fallback provider chain
kubot config [show|edit|get|set|unset|path|env-path|check|migrate]
kubot login / logout       OAuth sign-in / clear stored auth
kubot doctor [--fix]       Check dependencies and config
kubot status [--full]      Component summary (--full: every section)
```

### Tools & Skills

```
kubot tools [list|enable NAME|disable NAME]   Per-platform toolsets (curses UI with no args)

kubot skills list|browse|search QUERY|inspect ID
kubot skills install ID    Hub identifier OR a direct https://…/SKILL.md URL
kubot skills config        Enable/disable skills per platform
kubot skills check|update|uninstall|publish PATH
kubot skills tap add REPO  Add a GitHub repo as a skill source
kubot bundles              Skill bundles (one /<name> alias loads several skills)
```

### MCP Servers

```
kubot mcp add NAME (--url or --command) | remove | list | test NAME
kubot mcp catalog | install NAME     Curated catalog install
kubot mcp configure NAME             Toggle tool selection
kubot mcp-serve                      Run Kubot as an MCP server (mcp-serve plugin)
```
Details (transport, tool discovery, catalog): `references/native-mcp.md`.

### Gateway (Messaging Platforms)

```
kubot gateway run|install|start|stop|restart|status|setup
```

20+ platforms: Telegram, Discord, Slack, WhatsApp (Baileys + Business Cloud API), iMessage (Photon — `kubot photon setup`), Signal, Email, SMS, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, API Server, Webhooks. Open WebUI connects via the API Server adapter. Most adapters ship under `plugins/platforms/`.
Docs: https://kubot-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
kubot sessions list|browse|rename ID TITLE|delete ID|export OUT|prune|stats
```

### Cron / Webhooks

```
kubot cron list|create SCHED|edit ID|pause|resume|run ID|remove|status
    Schedules: '30m', 'every 2h', '0 9 * * *', ISO timestamp
kubot webhook subscribe NAME|list|remove NAME|test NAME
```
Webhook payloads/routes: `references/webhooks.md`.

### Profiles

```
kubot profile list|create NAME (--clone|--clone-all|--clone-from)|use|show|delete
kubot profile rename A B | alias NAME | export NAME | import FILE
kubot profile migrate-identity A B   Retry a completed rename's session/routing identity migration
```

### Credentials & Pools

```
kubot auth                 Interactive credential manager
kubot auth add [PROVIDER]  Add OAuth or API-key credential (nous, openai-codex, qwen-oauth, …)
kubot auth list|remove P IDX|reset PROVIDER|status
```
Multiple credentials per provider form a pool that rotates automatically and skips exhausted keys.

### Other

```
kubot desktop / gui        Native desktop app
kubot dashboard            Web admin panel + embedded chat (--stop / --status)
kubot proxy                OpenAI-compatible local proxy backed by an OAuth provider
kubot portal               Quick setup / sign in via Nous Portal
kubot kanban <verb>        Multi-agent work-queue board
kubot project              Named multi-folder workspaces (see references/projects-and-folders.md)
kubot skin list|use|set    Switch/tweak skins (see references/themes.md)
kubot pets <verb>          Pet mascots (see references/petdex.md)
kubot memory setup|status|off|reset   Memory provider
kubot secrets bitwarden|onepassword   External secret stores
kubot moa                  Mixture-of-Agents slots
kubot hooks / security / backup / import / checkpoints / console
kubot logs [-f] [errors]   View agent/error logs
kubot send                 One-off message through a gateway platform
kubot pairing / plugins / insights / journey / computer-use
kubot acp                  ACP server (IDE integration)
kubot completion bash|zsh|fish
kubot update / uninstall
```

Plugin- and provider-supplied subcommands (e.g. `kubot photon setup`) only appear once their plugin is installed/active. Importing from OpenClaw, Claude Code, Codex CLI or Cursor (`kubot import-agent <agent>`, plus the older `kubot claw migrate|cleanup`) comes from the `agent-importers` plugin; a fresh `kubot setup` that finds one of those agents offers to install it.

### Where to Find Things

| Looking for... | Location |
|---|---|
| Config options | `kubot config edit` · [Configuration docs](https://kubot-agent.nousresearch.com/docs/user-guide/configuration) |
| Tools / toolsets | `kubot tools list` · [Tools reference](https://kubot-agent.nousresearch.com/docs/reference/tools-reference) |
| Skills catalog | `kubot skills browse` · [Skills catalog](https://kubot-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `kubot model` · [Providers guide](https://kubot-agent.nousresearch.com/docs/integrations/providers) |
| Env variables | `kubot config env-path` · [Env vars reference](https://kubot-agent.nousresearch.com/docs/reference/environment-variables) |
| Gateway logs | `~/.kubot/logs/gateway.log` (or `kubot logs`) |
| Sessions | `kubot sessions browse` (reads state.db) |
