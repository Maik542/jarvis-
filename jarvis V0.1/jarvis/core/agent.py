from __future__ import annotations

import sys
from typing import Any

from jarvis.config import settings
from jarvis.utils.logging import get_logger

from .context import ExecutionContext
from .executor import Executor
from .planner import Planner, PlanStep
from .tool import RiskLevel, Tool, ToolParameter
from .tool_registry import ToolRegistry

logger = get_logger("core.agent")


class JarvisAgent:
    """Minimal agent shell for V0.1. It keeps a context and exposed tools."""

    def __init__(self) -> None:
        self.context = ExecutionContext(session_id="jarvis-v0.1")
        self.tool_registry = ToolRegistry()
        self.planner = Planner()
        self.executor = Executor(self.tool_registry)
        self._register_system_tools()

    def _register_system_tools(self) -> None:
        self.tool_registry.register(
            _SimpleTool(
                name="system.help",
                description="Print help information for the Jarvis shell.",
                parameters=[],
                risk_level=RiskLevel.SAFE,
                func=lambda **kwargs: "Available commands: help, tools, status, exit",
            )
        )

        self.tool_registry.register(
            _SimpleTool(
                name="system.status",
                description="Return the current Jarvis status payload.",
                parameters=[],
                risk_level=RiskLevel.SAFE,
                func=lambda **kwargs: self.status(),
            )
        )

    async def handle(self, user_input: str) -> str:
        """Process a user request into a basic plan and execution result."""
        command = user_input.strip()
        self.context.add_message("user", command)

        if not command:
            return "No input received."

        if command.lower() in {"help", "status", "tools"}:
            if command.lower() == "help":
                return "Available commands: help, tools, status, exit"
            if command.lower() == "tools":
                tool_names = ", ".join(tool.name for tool in self.tool_registry.list_tools())
                return f"Registered tools: {tool_names}"
            return str(self.status())

        plan = self.planner.create_plan(
            goal=command,
            steps=[PlanStep(tool="system.help", arguments={})],
        )

        result = await self.executor.execute(plan)
        if not result.success:
            logger.warning("Tool execution failed: %s", result.message)
            return result.message

        response = result.steps[0].result if result.steps else "No result returned."
        self.context.add_message("assistant", str(response))
        return str(response)

    def status(self) -> dict[str, Any]:
        """Return status information for the CLI shell."""
        return {
            "jarvis_version": "0.1.0",
            "python_version": sys.version.split()[0],
            "registered_tools": len(self.tool_registry),
            "llm_configured": settings.has_llm_config,
            "spotify_configured": settings.has_spotify_config,
            "provider": settings.llm_provider or "not configured",
        }


class _SimpleTool(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        parameters: list[ToolParameter] | None = None,
        risk_level: RiskLevel = RiskLevel.SAFE,
        func: Any | None = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            parameters=parameters or [],
            risk_level=risk_level,
        )
        self._func = func or (lambda **kwargs: None)

    async def execute(self, **kwargs: Any) -> Any:
        return self._func(**kwargs)
