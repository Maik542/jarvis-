from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jarvis.utils.logging import get_logger

from .planner import Plan, PlanStep
from .tool_registry import ToolRegistry

logger = get_logger("core.executor")


@dataclass(frozen=True)
class StepResult:
    """Execution result for a single plan step."""

    step: PlanStep
    success: bool
    result: Any = None
    error: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    """Result of a full plan execution."""

    goal: str
    steps: list[StepResult] = field(default_factory=list)
    success: bool = True
    message: str = ""


class Executor:
    """Executes tool-based plans sequentially."""

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self.tool_registry = tool_registry

    async def execute(self, plan: Plan) -> ExecutionResult:
        step_results: list[StepResult] = []
        for step in plan.steps:
            tool = self.tool_registry.get(step.tool)
            logger.info("Running tool %s with args %s", tool.name, step.arguments)
            try:
                result = await tool.execute(**step.arguments)
                step_results.append(
                    StepResult(step=step, success=True, result=result, error=None)
                )
            except Exception as exc:  # pragma: no cover - defensive execution path
                logger.exception("Tool %s failed during execution", tool.name)
                step_results.append(
                    StepResult(step=step, success=False, result=None, error=str(exc))
                )
                return ExecutionResult(
                    goal=plan.goal,
                    steps=step_results,
                    success=False,
                    message=f"Failed while executing '{tool.name}': {exc}",
                )

        return ExecutionResult(
            goal=plan.goal,
            steps=step_results,
            success=True,
            message=f"Completed plan for goal: {plan.goal}",
        )
