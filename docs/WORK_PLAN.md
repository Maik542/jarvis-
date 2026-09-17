# Gemeinsamer Arbeitsplan: Maik und Torben

Dieser Plan teilt die **erste parallele Etappe** auf. Das gemeinsame öffentliche Repository ist [Maik542/jarvis-](https://github.com/Maik542/jarvis-). Torben kann es sofort klonen; für einen Branch direkt im Repository braucht er Schreibzugriff. Ohne Schreibzugriff kann er in seinem eigenen Fork arbeiten und von dort einen Pull Request öffnen.

## Gemeinsame Spielregeln

1. Jeder verwendet einen eigenen Clone und einen eigenen Branch von aktuellem `main`. Nicht gleichzeitig im selben Arbeitsverzeichnis arbeiten. Torben startet mit `git clone https://github.com/Maik542/jarvis-.git`.
2. Kein direkter Push auf `main`. Für jede Aufgabe einen Pull Request öffnen und die andere Person um Review bitten.
3. Während der parallelen Etappe `main.py`, `jarvis/config.py`, `.env.example` und `pyproject.toml` nur nach Absprache ändern. Keine Zugangsdaten oder lokalen Profile committen.
4. Nach jeder Änderung die passenden Tests und mindestens `ruff check` laufen lassen. Im Pull Request notieren, was tatsächlich geprüft wurde.
5. Vor dem Zusammenführen prüfen, ob der Branch noch auf aktuellem `main` basiert. Konflikte gemeinsam auflösen; keine fremden Änderungen still überschreiben.
6. Ein GPT kann beim Erklären und Entwerfen helfen, aber maßgeblich sind der aktuelle Commit, der echte Code und die lokal ausgeführten Tests. Keine Behauptung „funktioniert“, wenn nur Code gelesen wurde.

Das bisherige GitHub-Repository enthält bereits eingecheckte Cache-Dateien und Logs. `.gitignore` verhindert nur neue versehentliche Commits; die bereits versionierten Artefakte sollten Maik und Torben in einem späteren, eigenen Hygiene-Pull-Request prüfen und aus der Versionsverwaltung entfernen. Keine Historie umschreiben und keine Dateien ohne Prüfung löschen.

## Parallele Etappe 1

| Person | Branch-Vorschlag | Eigene Dateien | Ergebnis |
| --- | --- | --- | --- |
| Maik | `maik/browser-reliability` | `jarvis/skills/browser/browser_skill.py`, neue `tests/test_browser_skill.py` | Browser-Suche und YouTube-Play mit automatisierten Tests gegen Rückfälle absichern. |
| Torben | `torben/command-parser` | neue `jarvis/core/commands.py`, neue `tests/test_commands.py` | Reinen, testbaren Befehls-Parser ohne Browser-, Spotify- oder Datei-Nebenwirkungen bauen. |

### Maiks Aufgabe

Prüfe die Browser-Fälle `search youtube for ...` ohne Wiedergabe, `play ... on youtube` mit Video, Google-/GitHub-Suche, Tab schließen und beim nächsten Befehl erneut öffnen. Automatisierte Tests sollen das Befehlsverhalten prüfen, ohne ein echtes Chrome-Profil oder Internet vorauszusetzen. Einen echten Chrome-Durchlauf zusätzlich manuell ausführen. Spotify-Code und Torbens Parser-Dateien bleiben unangetastet.

**Fertig, wenn:** Tests für die genannten Fälle vorhanden sind; der echte Browser-Test funktioniert; `ruff check` und die vorhandene Testsuite bestehen; der Pull Request nur Maiks Bereich betrifft.

### Torbens Aufgabe

Erstelle eine Funktion, die Eingabetext in eine klare Befehlsbeschreibung umwandelt, zum Beispiel Aktion (`open`, `search`, `play`, `pause`, `exit`), Dienst (`youtube`, `google`, `github`, `spotify`) und Suchtext. Die Schlüsselwörter sind unabhängig von Groß-/Kleinschreibung; der Suchtext behält die Schreibweise des Nutzers. Leere Suchtexte und unbekannte Befehle sollen ein eindeutiges Ergebnis liefern. Der Parser selbst darf keine Programme öffnen, API-Aufrufe machen oder Musik starten.

Mindestens diese Fälle testen: `search youtube for C418 Sweden`, `search google for Python lernen`, `search github for playwright`, `search spotify for Sweden`, `play C418 Sweden on youtube`, `play C418 Sweden on spotify`, `pause spotify`, `open github`, `exit` und unbekannte Eingaben. `main.py` in diesem Branch **noch nicht** ändern; die Integration folgt nach dem Review.

**Fertig, wenn:** der Parser vollständig offline testbar ist; die genannten Befehle korrekt erkannt werden; die vorhandenen Tests weiter bestehen; der Pull Request nur Torbens Bereich betrifft.

## Integration nach beiden Pull Requests

1. Maik übernimmt die beiden geprüften Pull Requests nacheinander nach `main`.
2. Maik erstellt danach einen eigenen Integrations-Branch und schreibt `main.py` selbst so um, dass es Torbens Parser nutzt. Das bisherige Such-/Play-Verhalten bleibt gleich.
3. Torben prüft diesen Integrations-Pull-Request besonders auf Parser-Grenzfälle und unerwartete Nebenwirkungen.
4. Gemeinsam ausführen: komplette Testsuite, Ruff, Typprüfung sowie je ein echter Browser- und Spotify-Test. Danach erst die nächste Funktion auswählen.

Der Plan kann nach der ersten Etappe angepasst werden. Neue Aufgaben bitte vor Beginn einer Datei und einer verantwortlichen Person zuordnen, damit unabhängiges Arbeiten auch wirklich unabhängig bleibt.
