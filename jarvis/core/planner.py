from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlanStep:
    """A single step within an execution plan."""

    # tool ist der Name im ToolRegistry; arguments werden an execute ?bergeben.
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Plan:
    """A high-level plan describing task execution."""

    # Ein Ziel kann aus mehreren nacheinander auszuf?hrenden Schritten bestehen.
    goal: str
    steps: list[PlanStep] = field(default_factory=list)


class Planner:
    """Simple planner abstraction for V0.1."""

    def create_plan(
        self,
        goal: str,
        steps: list[PlanStep] | None = None,
        *extra_steps: PlanStep,
    ) -> Plan:
        # Die Schritte kommen vom Aufrufer; hier findet noch keine LLM-Planung statt.
        plan_steps: list[PlanStep] = []
        if steps:
            plan_steps.extend(steps)
        if extra_steps:
            plan_steps.extend(extra_steps)
        # Noch keine Pr?fung, ob die genannten Werkzeuge existieren.
        return Plan(goal=goal, steps=plan_steps)

    def create_help_plan(self) -> Plan:
        return self.create_plan(
            goal="help",
            steps=[PlanStep(tool="system.help", arguments={})],
        )
