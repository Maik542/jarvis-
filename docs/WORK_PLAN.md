# Gemeinsamer Arbeitsplan: Maik und Torben

Dieser Plan teilt die **erste parallele Etappe** auf. Das gemeinsame öffentliche Repository ist [Maik542/jarvis-](https://github.com/Maik542/jarvis-). Maik und Torben arbeiten mit getrennten lokalen Clones, aber auf demselben GitHub-Branch `main`. Torben braucht dafür Schreibzugriff auf das Repository; ohne diesen Zugriff kann er nicht auf den gemeinsamen Branch pushen.

Wichtig für Maik: Der bisherige lokale Projektordner besitzt einen eigenen Initial-Commit und noch keinen `origin`-Remote. Seine Git-Historie ist **nicht** die Historie dieses GitHub-Repositories, obwohl die zentralen Python-Dateien derzeit gleich sind. Für die Teamarbeit bitte einen **neuen Clone** des GitHub-Repositories anlegen; den alten Ordner als Sicherung behalten. Nicht dessen `main` direkt zum GitHub-`main` pushen und die Historien nicht mit `--force` oder `--allow-unrelated-histories` verbinden.

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
| Torben | neue `jarvis/core/commands.py`, neue `tests/test_commands.py` | Reinen, testbaren Befehls-Parser ohne Browser-, Spotify- oder Datei-Nebenwirkungen bauen. |

### Maiks Aufgabe

Prüfe die Browser-Fälle `search youtube for ...` ohne Wiedergabe, `play ... on youtube` mit Video, Google-/GitHub-Suche, Tab schließen und beim nächsten Befehl erneut öffnen. Automatisierte Tests sollen das Befehlsverhalten prüfen, ohne ein echtes Chrome-Profil oder Internet vorauszusetzen. Einen echten Chrome-Durchlauf zusätzlich manuell ausführen. Spotify-Code und Torbens Parser-Dateien bleiben unangetastet.

**Fertig, wenn:** Tests für die genannten Fälle vorhanden sind; der echte Browser-Test funktioniert; `ruff check` und die vorhandene Testsuite bestehen; Maiks Commit nur seinen Bereich betrifft.

### Torbens Aufgabe

Erstelle eine Funktion, die Eingabetext in eine klare Befehlsbeschreibung umwandelt, zum Beispiel Aktion (`open`, `search`, `play`, `pause`, `exit`), Dienst (`youtube`, `google`, `github`, `spotify`) und Suchtext. Die Schlüsselwörter sind unabhängig von Groß-/Kleinschreibung; der Suchtext behält die Schreibweise des Nutzers. Leere Suchtexte und unbekannte Befehle sollen ein eindeutiges Ergebnis liefern. Der Parser selbst darf keine Programme öffnen, API-Aufrufe machen oder Musik starten.

Mindestens diese Fälle testen: `search youtube for C418 Sweden`, `search google for Python lernen`, `search github for playwright`, `search spotify for Sweden`, `play C418 Sweden on youtube`, `play C418 Sweden on spotify`, `pause spotify`, `open github`, `exit` und unbekannte Eingaben. `main.py` bei dieser Aufgabe **noch nicht** ändern; die Integration folgt nach dem gemeinsamen Review.

**Fertig, wenn:** der Parser vollständig offline testbar ist; die genannten Befehle korrekt erkannt werden; die vorhandenen Tests weiter bestehen; Torbens Commit nur seinen Bereich betrifft.

## Integration nach den beiden Aufgaben

1. Beide teilen ihre geprüften Commits nacheinander auf `main` und aktualisieren anschließend ihren jeweiligen Clone.
2. Maik schreibt `main.py` nach Absprache selbst so um, dass es Torbens Parser nutzt. Das bisherige Such-/Play-Verhalten bleibt gleich.
3. Torben prüft diese Integration besonders auf Parser-Grenzfälle und unerwartete Nebenwirkungen.
4. Gemeinsam ausführen: komplette Testsuite, Ruff, Typprüfung sowie je ein echter Browser- und Spotify-Test. Danach erst die nächste Funktion auswählen.

Der Plan kann nach der ersten Etappe angepasst werden. Neue Aufgaben bitte vor Beginn einer Datei und einer verantwortlichen Person zuordnen, damit unabhängiges Arbeiten auch wirklich unabhängig bleibt.
