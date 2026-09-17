from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryStore:
    """Simple in-memory store for future agent memory features."""

    # Ein W?rterbuch pro Instanz; nach Programmende gehen alle Eintr?ge verloren.
    items: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.items[key] = value

    def get(self, key: str, default: Any | None = None) -> Any:
        # default wird nur zur?ckgegeben, wenn der Schl?ssel fehlt.
        return self.items.get(key, default)

    def clear(self) -> None:
        self.items.clear()
