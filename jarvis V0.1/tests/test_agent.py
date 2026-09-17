from __future__ import annotations

import pytest

from jarvis.core.agent import JarvisAgent


@pytest.mark.asyncio
async def test_agent_starts_and_handles_help() -> None:
    agent = JarvisAgent()

    response = await agent.handle("help")

    assert "help" in response
    assert "tools" in response
    assert "status" in response
    assert agent.context.session_id == "jarvis-v0.1"


@pytest.mark.asyncio
async def test_agent_status_report() -> None:
    agent = JarvisAgent()

    status = agent.status()

    assert "jarvis_version" in status
    assert "python_version" in status
    assert "registered_tools" in status
    assert "llm_configured" in status
    assert "spotify_configured" in status
