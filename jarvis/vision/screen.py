from __future__ import annotations

from pathlib import Path


class ScreenInspector:
    """Placeholder for future screen understanding features."""

    def __init__(self) -> None:
        # F?r einen k?nftigen Screenshot-Pfad reserviert; capture setzt ihn
        # in dieser fr?hen Version noch nicht.
        self.last_capture_path: Path | None = None

    def capture(self) -> str:
        """Return a placeholder message until real screen capture support is added."""
        return "Screen capture support is not implemented yet."
