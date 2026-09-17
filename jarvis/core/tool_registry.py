from __future__ import annotations

from .exceptions import DuplicateToolError, ToolNotFoundError
from .tool import Tool


class ToolRegistry:
    """Registry for runtime tool discovery and execution."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool, replace: bool = False) -> None:
        """Register a tool. Set replace=True to overwrite an existing tool."""
        if tool.name in self._tools and not replace:
            raise DuplicateToolError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """Unregister a tool by name."""
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool '{name}' was not found.")
        del self._tools[name]

    def get(self, name: str) -> Tool:
        """Return a registered tool by name."""
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool '{name}' was not found.")
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        """Return all registered tools sorted by name."""
        return sorted(self._tools.values(), key=lambda tool: tool.name)

    def has(self, name: str) -> bool:
        """Return whether a tool is already registered."""
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, item: str) -> bool:
        return item in self._tools

    def __iter__(self) -> list[Tool]:
        return list(self._tools.values())
