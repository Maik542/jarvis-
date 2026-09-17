from __future__ import annotations


class JarvisError(Exception):
    """Base exception for Jarvis application errors."""


class ToolExecutionError(JarvisError):
    """Raised when a tool cannot execute successfully."""


class ToolNotFoundError(JarvisError):
    """Raised when a requested tool is not registered."""


class DuplicateToolError(JarvisError):
    """Raised when a tool name is registered twice without replacement."""
