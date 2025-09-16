"""Common utilities for Jenkins tools."""

import logging
from functools import wraps
from typing import Callable

from mcp.server.fastmcp import FastMCP


def mcp_tool(mcp: FastMCP) -> Callable:
    """Return a decorator for MCP tool registration logging.

    Returns:
        A decorator that logs the function name when called.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            logging.info(f"[Tool] {func.__name__}")
            return func(*args, **kwargs)
        return mcp.tool()(wrapper)
    return decorator
