# Repository Guidelines

## Project Structure & Module Organization

`main.py` is the application entry point: it loads settings, initializes logging and SQLite, registers questionnaires, and starts the Discord client. Discord-specific code lives in `bot/`; add command cogs below `bot/commands/` and shared Discord abstractions below `bot/core/`. Business operations belong in `services/`, while persistence is split between `database/repositories/` and parameterized SQL files under `database/sql/{create,reads,writes,deletes}/`. Runtime settings are defined in `config/`, questionnaire and extension definitions are in `cfg/*.yaml`, and reusable models, exceptions, and logging helpers live in `utils/`. Treat `data/db/` and `logs/` as runtime output, not source assets.

## Build, Test, and Development Commands

This project has no build step. From the repository root, use:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

The final command initializes the configured SQLite database and connects the bot. Before running it, set `NINETY_THOUSAND_ACRES_DISCORD_BOT_TOKEN` in `.env`. For a quick syntax check, run `python -m compileall bot config database services utils main.py`.

## Coding Style & Naming Conventions

Use Python 3 conventions and four-space indentation. Follow PEP 8: `snake_case` for modules, functions, and variables; `PascalCase` for classes; and `UPPER_CASE` for constants and environment keys. Add type hints to public APIs and keep async Discord handlers explicitly `async`. Keep SQL in the matching operation directory and use descriptive names such as `match_signup_forms_answers_upsert.sql`. No formatter or linter is currently configured; keep imports grouped as standard library, third-party, then local modules.

## Testing Guidelines

There is currently no automated test suite or coverage threshold. New behavior should include focused `pytest` tests under `tests/`, named `test_<module>.py`, with test functions named `test_<behavior>()`. Mock Discord/network interactions and use temporary SQLite databases; never mutate `data/db/NinetyThousandAcres_discord.db`. Run tests with `python -m pytest` after adding `pytest` as a development dependency.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout, so use concise, imperative commit subjects, preferably Conventional Commit prefixes such as `feat: add signup cancellation` or `fix: validate guild configuration`. Pull requests should explain the user-visible change, identify configuration or schema impacts, link related issues, and include test results. Attach screenshots for changes to Discord embeds, modals, or command flows.

## Security & Configuration

Never commit `.env`, bot tokens, populated databases, or logs. Update `.env.example` whenever configuration keys change, using safe placeholder values. Avoid logging secrets or raw user data, and keep SQL parameterized through repository methods.
