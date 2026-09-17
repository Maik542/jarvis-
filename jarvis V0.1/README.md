# Jarvis V0.1

Jarvis is a local Python assistant for Windows. It can search the web in its own Chrome profile and control the Spotify desktop app.

This is a learning project. It does not yet implement autonomous computer control or a production-grade AI reasoning engine.

## Project status

Current milestone:

- Project foundation and package layout
- Interactive CLI commands for browser search, YouTube playback, and Spotify
- Persistent Jarvis Chrome profile under `%LOCALAPPDATA%\Jarvis\BrowserProfile`
- Tool + registry abstraction
- Planner and executor skeletons
- Skill architecture for browser, computer, media, Spotify, and system
- Logging and configuration foundation
- Automated tests for core registry/agent behavior and Spotify playback

## Architecture overview

The project is organized into a small set of reusable layers:

- `main.py` — interactive CLI entry point
- `jarvis/config.py` — environment and settings management
- `jarvis/core/` — agent, planner, executor, registry, and tool abstractions
- `jarvis/skills/` — domain-specific capability modules
- `jarvis/vision/` — screen and OCR-oriented future components
- `jarvis/voice/` — speech interfaces
- `jarvis/memory/` — future user/context memory layer
- `jarvis/utils/` — logging utilities

## Requirements

- Python >= 3.12
- Access to a local development environment
- Google Chrome for the Jarvis browser
- Spotify desktop app and a Spotify Premium account for playback commands

## Virtual environment setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Dependency installation

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Browser setup

Jarvis uses the installed Google Chrome through Playwright. Its separate profile keeps browser data between runs. Close any other Jarvis process using that profile before starting another one.

## Environment setup

Copy the sample environment file and populate any values you need locally:

```powershell
Copy-Item .env.example .env
```

The repository intentionally keeps secrets out of source control.

## Running Jarvis

```powershell
python main.py
```

Available commands include:

- `search youtube for C418 Sweden` — show YouTube results without playing
- `search google for Python lernen` — search Google in Jarvis Chrome
- `search github for Python` — search GitHub in Jarvis Chrome
- `search spotify for C418 Sweden` — search in the Spotify desktop app
- `play C418 Sweden on youtube` — open the first matching YouTube video
- `play C418 Sweden on spotify` — play through the Spotify desktop app
- `pause spotify` — pause Spotify playback
- `open youtube`, `open google`, `open github`, `open spotify`
- `exit` — close Jarvis and its browser

Use `Strg+W` to close the current Chrome tab. Jarvis stays at its command prompt.

Spotify playback requires a developer app and the `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI` values in your local `.env`. Never commit `.env` or `.spotify_cache`.

## Running tests

```powershell
pytest
```

## Linting and type checking

```powershell
ruff check .
mypy jarvis
```

## High-level roadmap

```text
V0.1 - Core architecture + CLI
V0.2 - Reliable browser control
V0.3 - Spotify integration
V0.4 - Windows UI automation
V0.5 - Screen understanding / vision
V0.6 - LLM planner
V0.7 - Verification + recovery loop
V0.8 - Voice input/output
V0.9 - Memory and user preferences
V1.0 - Integrated local Jarvis assistant
```

## Notes

This foundation does not include destructive computer control, unrestricted shell execution, or advanced autonomous behavior.
