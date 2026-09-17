from __future__ import annotations

from jarvis.core.tool import RiskLevel, SyncTool, ToolParameter


class ComputerSkill:
    """Foundation for future Windows desktop automation."""

    def __init__(self) -> None:
        # Geplante Computer-Werkzeuge; noch nicht mit der CLI verbunden.
        self.tools = [
            SyncTool(
                name="computer.open_application",
                description="Open an application by name.",
                func=self.open_application,
                parameters=[
                    ToolParameter("name", "str", "Application name.", required=True),
                ],
                risk_level=RiskLevel.CONFIRM,
            ),
            SyncTool(
                name="computer.screenshot",
                description="Capture a screenshot of the current desktop.",
                func=self.screenshot,
                parameters=[],
                risk_level=RiskLevel.SAFE,
            ),
        ]

    def open_application(self, name: str) -> str:
        # Platzhalter: Keine echte Anwendung wird ge?ffnet.
        return f"Computer tool prepared to open: {name}"

    def screenshot(self) -> str:
        # Platzhalter: Noch kein Bild wird aufgenommen.
        return "Computer tool prepared to capture a screenshot."
