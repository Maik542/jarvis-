# Jarvis V0.1: Einstieg für Torben

Dieses Dokument ist für einen menschlichen Mitentwickler gedacht. Du brauchst dafür kein Codex. Das gemeinsame Repository ist [Maik542/jarvis-](https://github.com/Maik542/jarvis-). Lies zuerst auch die [README](../README.md) und den [gemeinsamen Arbeitsplan](WORK_PLAN.md).

## Kontext für dein GPT

Wenn du ChatGPT oder ein anderes GPT als Lernhilfe verwendest, gib ihm den folgenden Einstieg. Bei Codefragen hänge danach die betroffenen aktuellen Dateien oder einen Commit-/PR-Link an; ein Chat kennt spätere Änderungen nicht automatisch. Falls dein GPT GitHub-Links nicht öffnen kann, kopiere die drei genannten Markdown-Dateien in den Chat.

> Ich arbeite mit Maik am öffentlichen Python-Projekt https://github.com/Maik542/jarvis-. Lies README.md, docs/TORBEN_START.md und docs/WORK_PLAN.md als Projektkontext. Ich arbeite ohne Codex in meinem eigenen Git-Clone; wir teilen uns den GitHub-Branch main und bearbeiten getrennte Dateien. Meine erste Aufgabe ist ein neuer Sitzungskontext: Nach einer Suche oder Wiedergabe versteht Jarvis `play that on youtube` und `play that on spotify` anhand der letzten gültigen Anfrage. Ich bearbeite dafür jarvis/core/context.py, main.py und tests/test_followup_commands.py, aber nicht Maiks Browser-Dateien oder spotify_skill.py. Die Tests müssen ohne Internet und Tokens laufen. Gib bei Vorschlägen betroffene Dateien, konkrete Tests und offene Annahmen an. Fordere niemals .env, OAuth-Tokens oder andere Zugangsdaten an. Behaupte nicht, Änderungen im Repository vorgenommen zu haben, wenn du nur Text vorgeschlagen hast.

## Ziel und aktueller Stand

Jarvis ist ein lokaler Python-Assistent für Windows. Derzeit gibt es eine interaktive Kommandozeile, einen dauerhaften eigenen Chrome-Profilordner für Browseraktionen und eine Spotify-Anbindung an die Desktop-App. Sprachsteuerung, Bildschirmverständnis, freies KI-Planen und allgemeine Windows-Steuerung sind noch nicht fertig.

Der Einstiegspunkt ist `main.py`. Er verarbeitet Befehle und ruft die Browser- und Spotify-Skills auf. Die Klassen unter `jarvis/core/` bilden bislang ein separates Grundgerüst; `JarvisAgent` steuert die aktuelle Kommandozeile noch nicht.

| Bereich | Wichtige Dateien | Aktuelles Verhalten |
| --- | --- | --- |
| CLI | `main.py` | Liest Befehle, hält die Sitzung bis `exit` offen. |
| Browser | `jarvis/skills/browser/browser_skill.py` | Nutzt Playwright mit `%LOCALAPPDATA%\Jarvis\BrowserProfile` und installiertem Chrome. |
| Spotify | `jarvis/skills/spotify/spotify_skill.py`, `jarvis/config.py` | Sucht Titel und steuert die Spotify-Desktop-App über die Web API. |
| Architektur | `jarvis/core/` | Tool-Registry, Planner, Executor und Agent als noch nicht vollständig integriertes Grundgerüst. |
| Tests | `tests/` | Kernfunktionen und Spotify-Verhalten; vor Beginn der Teamarbeit liefen 24 Tests. |

## Verhalten, das erhalten bleiben soll

- `search youtube for ...` zeigt nur Suchergebnisse; `play ... on youtube` öffnet ein Video.
- `search google for ...` und `search github for ...` öffnen Suchergebnisse im Jarvis-Chrome.
- `search spotify for ...` öffnet die Suche in der Spotify-Desktop-App; `play ... on spotify` spielt dort einen Titel ab.
- `Strg+W` schließt einen Chrome-Tab, Jarvis bleibt in der Kommandozeile. Erst `exit` beendet Jarvis und seinen Browser.
- Die Spotify-Wiedergabe startet den gefundenen Titel derzeit innerhalb seines Album-Kontexts. Der direkte Aufruf mit einer einzelnen Titel-URI wurde vom lokalen Spotify-Client zwar angenommen, spielte aber nichts ab. Diese Besonderheit bitte nicht ohne echten Wiedergabetest ersetzen.
- `playwright_test.py` ist ein älterer, eigenständiger YouTube-Test. Er gehört nicht zum aktuellen `main.py`-Befehlsablauf.

## Lokal starten

Unter Windows im Projektordner:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe main.py
```

Python 3.12 oder neuer ist erforderlich; falls `py -3.12` nicht installiert ist, verwende eine vorhandene neuere Version. Für Browserbefehle muss Google Chrome installiert sein. Spotify ist nur für Spotify-Befehle nötig. Kopiere für eigene Spotify-Tests `.env.example` nach `.env` und verwende ausschließlich deine eigenen Zugangsdaten und Freigaben.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check main.py jarvis tests
.\.venv\Scripts\mypy.exe main.py jarvis\skills\browser\browser_skill.py jarvis\skills\spotify\spotify_skill.py
```

`.env`, `.spotify_cache`, `.venv` und Logs dürfen nicht ins Repository. Bitte keine Zugangsdaten, OAuth-Codes oder kompletten Token-Cache in Issues, Pull Requests oder Chats kopieren. Das Chrome-Profil liegt außerhalb des Repositories und darf nicht von zwei Jarvis-Prozessen auf demselben Computer gleichzeitig verwendet werden.

## Zusammenarbeit

Maik schreibt seine Python-Änderungen selbst in VS Code; Codex darf ihm Code erklären und nach dem Speichern prüfen, aber seine Python-Dateien nicht direkt ändern. Torben entwickelt seine eigenen Aufgaben selbstständig ohne Codex. Jede Person arbeitet in ihrem eigenen Clone; beide verwenden den gemeinsamen Branch `main`. Die erste konkrete Dateiaufteilung und Abnahmekriterien stehen im [Arbeitsplan](WORK_PLAN.md).

Vor einer Änderung an `main.py` oder an Dateien der anderen Person bitte kurz abstimmen. Nach einer fertigen Aufgabe nenne dem anderen Commit, Verhalten, betroffene Dateien und Testergebnis. Vor einem Push den aktuellen Stand von `main` prüfen; nie mit `--force` fremde Änderungen überschreiben.
