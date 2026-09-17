from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    """Action risk categories for future computer-use safety checks."""

    # Metadaten f?r sp?tere Freigaben; Executor erzwingt diese Stufen noch nicht.
    SAFE = "safe"
    CONFIRM = "confirm"
    DANGEROUS = "dangerous"


@dataclass(frozen=True)
class ToolParameter:
    """Describes a single tool parameter."""

    # Schema-Beschreibung f?r k?nftige Planung; noch keine Laufzeitvalidierung.
    name: str
    type: str
    description: str = ""
    required: bool = False
    default: Any | None = None


@dataclass
class Tool(ABC):
    """Base class for all tools."""

    # Jedes konkrete Werkzeug hat einen Namen und muss execute implementieren.
    name: str
    description: str
    parameters: list[ToolParameter] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.SAFE

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with the supplied arguments."""


class SyncTool(Tool):
    """Convenience wrapper for synchronous tool implementations."""

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        parameters: list[ToolParameter] | None = None,
        risk_level: RiskLevel = RiskLevel.SAFE,
    ) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters or []
        self.risk_level = risk_level
        self._func = func

    async def execute(self, **kwargs: Any) -> Any:
        # Direkter synchroner Aufruf: Langsame Funktionen blockieren hier asyncio.
        # main.py nutzt f?r Spotify deshalb ausdr?cklich asyncio.to_thread().
        return self._func(**kwargs)
