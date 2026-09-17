from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionContext:
    """Shared context for an agent conversation or execution."""

    # Der Verlauf lebt nur im Arbeitsspeicher und wird beim Neustart verworfen.
    session_id: str = "default"
    conversation: list[dict[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        # Die Rolle (z. B. user/assistant) bleibt mit dem Text erhalten.
        # Noch keine K?rzung, Datenbank oder automatische LLM-?bergabe.
        self.conversation.append({"role": role, "content": content})
