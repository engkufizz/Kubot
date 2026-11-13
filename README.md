# Kubot 🤖

> **100% Pure-Python Agentic CLI & Dashboard Harness**
> Rebuilt from the ground up with zero Node.js, npm, pnpm, or JavaScript dependencies.

---

## Highlights

- **100% Pure Python**: Installs cleanly in standard Python 3.11+ virtual environments using `pip install -e .`. Zero Node.js runtime required.
- **Dual UI Options**:
  - **Interactive CLI/TUI**: Terminal harness built on `prompt_toolkit` and `rich` with full color themes and command history.
  - **Pure-Python Web Dashboard & Desktop Window**: Built directly with FastAPI, HTMX, and modern responsive CSS with zero build steps or npm tools needed. Launch with `kubot ui` or `kubot desktop`.
- **Autonomous Goals & Planning**: Autonomous goal execution engine supporting `/goal` and `/subgoal` quality gates.
- **DeepSeek & OpenAI Compatibility**: First-class support for DeepSeek Chat (`deepseek-chat`), DeepSeek Reasoner (`deepseek-reasoner`), and any OpenAI-compatible endpoint.
- **Extensible Skills Architecture**: Load local skills via `SKILL.md` specifications.

---

## Quickstart

### 1. Create a Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Kubot

```bash
pip install -e .
```

### 3. Configure Your Model Endpoint

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Set your API key for DeepSeek or OpenAI:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

Or configure via the CLI:

```bash
kubot config
```

### 4. Run Kubot

```bash
# Launch interactive terminal session
kubot

# Launch the pure-Python Web Dashboard
kubot ui

# Launch the standalone Desktop Window
kubot desktop

# Single prompt query
kubot chat -q "Hello Kubot!"

# Run an autonomous goal loop
kubot chat -q "/goal create a clean python web scraper with tests"
```

---

## Directory Structure

- `~/.kubot/`: Default configuration directory containing `config.yaml`, session state databases, and custom skills.
- `hermes_cli/`: Core Python CLI, console engine, and web server routers.
- `hermes_cli/web_dist/`: Pure-Python zero-node web application assets.
- `agent/`: Conversation loop, tool dispatch, and prompt engineering.
- `tools/`: Built-in execution, file operations, search, and skills tools.

---

## License

MIT License.
