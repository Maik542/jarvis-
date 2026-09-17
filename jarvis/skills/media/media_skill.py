from __future__ import annotations

from jarvis.core.tool import RiskLevel, SyncTool, ToolParameter


class MediaSkill:
    """Foundation for media playback controls."""

    def __init__(self) -> None:
        # Allgemeiner Medien-Entwurf; echte Wiedergabe l?uft aktuell ?ber
        # BrowserSkill (YouTube) oder SpotifySkill (Spotify).
        self.tools = [
            SyncTool(
                name="media.play",
                description="Request playback of a media source.",
                func=self.play,
                parameters=[ToolParameter("source", "str", "Media source or URL.", required=True)],
                risk_level=RiskLevel.SAFE,
            ),
            SyncTool(
                name="media.pause",
                description="Pause the current media playback.",
                func=self.pause,
                parameters=[],
                risk_level=RiskLevel.SAFE,
            ),
        ]

    def play(self, source: str) -> str:
        # Platzhalter: Meldet nur die geplante Aktion zur?ck.
        return f"Media tool prepared to play: {source}"

    def pause(self) -> str:
        # Platzhalter: Pausiert keine laufende Wiedergabe.
        return "Media tool prepared to pause playback."
