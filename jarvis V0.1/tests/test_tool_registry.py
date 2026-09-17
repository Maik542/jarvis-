from __future__ import annotations

import pytest

from jarvis.core.exceptions import DuplicateToolError, ToolNotFoundError
from jarvis.core.tool import RiskLevel, Tool, ToolParameter


class FakeTool(Tool):
    def __init__(self, name: str = "fake.echo") -> None:
        super().__init__(
            name=name,
            description="Returns the provided payload.",
            parameters=[ToolParameter("value", "str", "Value to echo back.", required=True)],
            risk_level=RiskLevel.SAFE,
        )

    async def execute(self, **kwargs):
        return kwargs.get("value")


def test_register_and_get_tool() -> None:
    from jarvis.core.tool_registry import ToolRegistry

    registry = ToolRegistry()
    tool = FakeTool()

    registry.register(tool)

    assert registry.has("fake.echo") is True
    assert registry.get("fake.echo") is tool
    assert [item.name for item in registry.list_tools()] == ["fake.echo"]


def test_duplicate_registration_raises() -> None:
    from jarvis.core.tool_registry import ToolRegistry

    registry = ToolRegistry()
    registry.register(FakeTool())

    with pytest.raises(DuplicateToolError):
        registry.register(FakeTool())


def test_unregister_removes_tool() -> None:
    from jarvis.core.tool_registry import ToolRegistry

    registry = ToolRegistry()
    registry.register(FakeTool("fake.alpha"))

    registry.unregister("fake.alpha")

    assert registry.has("fake.alpha") is False


def test_missing_tool_raises() -> None:
    from jarvis.core.tool_registry import ToolRegistry

    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.get("missing.tool")


@pytest.mark.asyncio
async def test_execute_basic_fake_tool() -> None:
    from jarvis.core.executor import Executor
    from jarvis.core.planner import Plan, Planner, PlanStep
    from jarvis.core.tool_registry import ToolRegistry

    registry = ToolRegistry()
    registry.register(FakeTool())

    plan = Plan(goal="echo", steps=[PlanStep(tool="fake.echo", arguments={"value": "hello"})])
    result = await Executor(registry).execute(plan)

    assert result.success is True
    assert result.steps[0].result == "hello"

    planner = Planner()
    custom_plan = planner.create_plan(
        "echo",
        [PlanStep(tool="fake.echo", arguments={"value": "hello"})],
    )
    assert custom_plan.steps[0].tool == "fake.echo"
