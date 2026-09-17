# Gemeinsamer Arbeitsplan: Maik und Torben

Dieser Plan teilt die **erste parallele Etappe** auf. Das gemeinsame öffentliche Repository ist [Maik542/jarvis-](https://github.com/Maik542/jarvis-). Maik und Torben arbeiten mit getrennten lokalen Clones, aber auf demselben GitHub-Branch `main`. Torben braucht dafür Schreibzugriff auf das Repository; ohne diesen Zugriff kann er nicht auf den gemeinsamen Branch pushen.

Wichtig für Maik: Der bisherige lokale Projektordner besitzt einen eigenen Initial-Commit und noch keinen `origin`-Remote. Seine Git-Historie ist **nicht** die Historie dieses GitHub-Repositories, obwohl die zentralen Python-Dateien derzeit gleich sind. Maik kann dort weiterhin Code schreiben und lokal testen. Für den gemeinsamen Commit und Push übernimmt er aber nur die geprüften, selbst geänderten Dateien in seinen **neuen Clone** des GitHub-Repositories und testet dort erneut. Den alten Ordner als Sicherung behalten; nicht dessen `main` direkt zum GitHub-`main` pushen oder die Historien mit `--force` beziehungsweise `--allow-unrelated-histories` verbinden.

## Gemeinsame Spielregeln

1. Jeder verwendet einen eigenen Clone des aktuellen `main`; nicht gleichzeitig im selben Arbeitsverzeichnis arbeiten. Torben startet mit `git clone https://github.com/Maik542/jarvis-.git`.
2. Es gibt **nur einen gemeinsamen Branch `main`**. Vor Arbeitsbeginn `git pull --ff-only origin main` ausführen. Vor einem Push dem anderen kurz Bescheid geben und prüfen, ob inzwischen neue Commits auf GitHub liegen. Kleine, klar benannte Commits mit jeweils nur den eigenen Dateien erstellen.
3. Während der parallelen Etappe `main.py`, `jarvis/config.py`, `.env.example` und `pyproject.toml` nur nach Absprache ändern. Keine Zugangsdaten oder lokalen Profile committen.
4. Nach jeder Änderung die passenden Tests und mindestens `ruff check` laufen lassen. Dem anderen Commit, betroffene Dateien und tatsächlich ausgeführte Tests nennen.
5. Wenn der andere inzwischen gepusht hat, nicht mit `--force` pushen. Neue Commits zuerst holen und einen nötigen Merge oder Konflikt gemeinsam klären; niemals fremde Änderungen still überschreiben. Bei Unsicherheit vor dem Push anhalten und abstimmen.
6. Ein GPT kann beim Erklären und Entwerfen helfen, aber maßgeblich sind der aktuelle Commit, der echte Code und die lokal ausgeführten Tests. Keine Behauptung „funktioniert“, wenn nur Code gelesen wurde.

Das bisherige GitHub-Repository enthält bereits eingecheckte Cache-Dateien und Logs. `.gitignore` verhindert nur neue versehentliche Commits; die bereits versionierten Artefakte sollten Maik und Torben später gemeinsam prüfen und in einem gesonderten, abgesprochenen Commit aus der Versionsverwaltung entfernen. Keine Historie umschreiben und keine Dateien ohne Prüfung löschen.

## Parallele Etappe 1

| Person | Eigene Dateien auf `main` | Ergebnis |
| --- | --- | --- |
| Maik | `jarvis/skills/browser/browser_skill.py`, neue `tests/test_browser_skill.py` | Browser-Suche und YouTube-Play mit automatisierten Tests gegen Rückfälle absichern. |
| Torben | neue `.github/workflows/checks.yml` | Automatische Windows-Prüfung für jeden Push auf `main` einrichten. |

### Maiks Aufgabe

Prüfe die Browser-Fälle `search youtube for ...` ohne Wiedergabe, `play ... on youtube` mit Video, Google-/GitHub-Suche, Tab schließen und beim nächsten Befehl erneut öffnen. Automatisierte Tests sollen das Befehlsverhalten prüfen, ohne ein echtes Chrome-Profil oder Internet vorauszusetzen. Einen echten Chrome-Durchlauf zusätzlich manuell ausführen. Spotify-Code und Torbens Workflow-Datei bleiben unangetastet.

**Fertig, wenn:** Tests für die genannten Fälle vorhanden sind; der echte Browser-Test funktioniert; `ruff check` und die vorhandene Testsuite bestehen; Maiks Commit nur seinen Bereich betrifft.

### Torbens Aufgabe

Richte GitHub Actions für das gemeinsame Repository ein. Der Workflow soll bei jedem Push auf `main` auf einem Windows-Runner Python 3.12 einrichten, `requirements.txt` und `requirements-dev.txt` installieren, die komplette Testsuite mit `pytest -q` ausführen und `ruff check main.py jarvis tests` starten. Eine manuelle Ausführung über `workflow_dispatch` ist hilfreich, aber nicht zwingend. Nutze aktuelle offizielle Versionen der GitHub-Actions-Bausteine.

Der Workflow darf weder Spotify-Zugangsdaten noch ein echtes Chrome-Profil benötigen; Maiks neue Browser-Tests verwenden Attrappen. Torben ändert in dieser Etappe weder `main.py` noch Maiks Browser-Dateien. Bei einem roten Lauf den konkreten Fehler untersuchen, statt Tests auszuschalten oder zu überspringen.

**Fertig, wenn:** ein echter Lauf im GitHub-Tab „Actions“ auf `main` für Tests und Ruff grün ist, keine Secrets hinterlegt werden mussten und Torbens Commit nur die Workflow-Datei betrifft.

## Nach den beiden Aufgaben

1. Torben teilt den geprüften Workflow-Commit auf `main`; Maik aktualisiert danach seinen Team-Clone.
2. Maik überträgt seinen im alten Ordner getesteten Browser-Test in den Team-Clone, prüft ihn dort erneut und teilt dann seinen Commit auf `main`.
3. Beide kontrollieren, dass der neue GitHub-Actions-Lauf grün ist. Ein fehlgeschlagener Lauf wird vor der nächsten Funktion untersucht.
4. Zusätzlich manuell ausführen: ein echter Chrome-Durchlauf einschließlich `Strg+W` sowie bei künftigen Spotify-Änderungen ein echter Spotify-Test.

Der Plan kann nach der ersten Etappe angepasst werden. Neue Aufgaben bitte vor Beginn einer Datei und einer verantwortlichen Person zuordnen, damit unabhängiges Arbeiten auch wirklich unabhängig bleibt.
