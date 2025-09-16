"""Register Jenkins tools for FastMCP.

This module provides functions to register Jenkins job, view,
and build tools to the FastMCP server.
"""

from mcp.server.fastmcp import FastMCP

from tools.tool_jenkins_build import JenkinsBuildToolsRegistrar
from tools.tool_jenkins_job import JenkinsJobToolsRegistrar
from tools.tool_jenkins_view import JenkinsViewToolsRegistrar


def register_tools(mcp: FastMCP) -> None:
    """Register Jenkins job, view, and build tools to FastMCP.

    Args:
        mcp (FastMCP): The FastMCP server instance.
    """
    JenkinsBuildToolsRegistrar(mcp).register()
    JenkinsJobToolsRegistrar(mcp).register()
    JenkinsViewToolsRegistrar(mcp).register()
