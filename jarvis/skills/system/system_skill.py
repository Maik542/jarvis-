from __future__ import annotations

from jarvis.core.tool import RiskLevel, SyncTool, ToolParameter


class SystemSkill:
    """Foundation for local system actions and metadata queries."""

    def __init__(self) -> None:
        # Nur Werkzeugbeschreibungen; main.py registriert diesen Skill noch nicht.
        self.tools = [
            SyncTool(
                name="system.open_path",
                description="Open a local filesystem path.",
                func=self.open_path,
                parameters=[ToolParameter("path", "str", "Path to open.", required=True)],
                risk_level=RiskLevel.CONFIRM,
            ),
            SyncTool(
                name="system.get_running_apps",
                description="List running application names if available.",
                func=self.get_running_apps,
                parameters=[],
                risk_level=RiskLevel.SAFE,
            ),
        ]

    def open_path(self, path: str) -> str:
        # Platzhalter: ?ffnet derzeit keine Datei oder Anwendung.
        return f"System tool prepared to open path: {path}"

    def get_running_apps(self) -> str:
        # Platzhalter: Fragt noch keine Windows-Prozesse ab.
        return "System tool prepared to list running applications."
