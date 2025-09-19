"""Jenkins build management tool registration for FastMCP.

This module provides a registrar class to register Jenkins build-related tools
to the FastMCP server.
"""

import json

from mcp.server.fastmcp import FastMCP

from libraries.jenkins_api import JenkinsAPI
from tools.tool_common import mcp_tool


class JenkinsBuildToolsRegistrar:
    """Registrar for Jenkins build management tools.

    This class registers build-related tools to the FastMCP server.
    """

    def __init__(self, mcp: FastMCP) -> None:
        """Initialize JenkinsBuildToolsRegistrar and register all build tools.

        Args:
            mcp (FastMCP): The FastMCP server instance.
        """
        self.mcp = mcp

    def register(self) -> None:
        """Register all build management tools to FastMCP."""
        self.tool_stop_last_build()
        self.tool_get_last_build_number()
        self.tool_get_build_information()
        self.tool_get_build_params()
        self.tool_get_build_console()

    def tool_stop_last_build(self) -> None:
        """Register stop_last_build tool."""
        @mcp_tool(self.mcp)
        def stop_last_build(job_name: str) -> str:
            """Stop the last build of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message indicating build stop success or failure.
            """
            is_stopped = JenkinsAPI().stop_last_build(job_name)
            if is_stopped:
                return f"Successfully stopped the last build for job {job_name}."
            return f"Failed to stop the last build for job {job_name}."

    def tool_get_last_build_number(self) -> None:
        """Register get_last_build_number tool."""
        @mcp_tool(self.mcp)
        def get_last_build_number(
            job_name: str,
        ) -> str:
            """Get the last build number of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build number or failure reason.
            """
            num = JenkinsAPI().get_last_build_number(job_name)
            if num is not None:
                return f"Successfully retrieved last build number for job {job_name}: {num}"
            return f"Failed to retrieve last build number for job {job_name}."

    def tool_get_build_information(self) -> None:
        """Register get_build_information tool."""
        @mcp_tool(self.mcp)
        def get_build_information(
            job_name: str,
            build_number: int = None,
        ) -> str | None:
            """Get the build information of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.
                build_number (int): The build number to retrieve. If None, retrieves the last build.

            Returns:
                Message with the build information or failure reason.
            """
            api = JenkinsAPI()
            info = {
                "build_number": build_number or api.get_last_build_number(job_name),
                "start_time": api.get_build_start_time(job_name, build_number),
                "duration": api.get_build_duration(job_name, build_number),
                "status": api.get_build_status(job_name, build_number),
            }
            if info:
                return f"Successfully retrieved build information for job {job_name}: {info}"
            return f"Failed to retrieve build information for job {job_name}."

    def tool_get_build_params(self) -> None:
        """Register get_build_params tool."""
        @mcp_tool(self.mcp)
        def get_build_params(
            job_name: str,
            build_number: int = None,
        ) -> str | None:
            """Get the build parameters of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.
                build_number (int): The build number to retrieve. If None, retrieves the last build.

            Returns:
                Message with the build parameters or failure reason.
            """
            build_params = JenkinsAPI().get_build_params(job_name, build_number)
            if build_params is not None:
                return (
                    f"Successfully retrieved build parameters for job {job_name}: "
                    f"{json.dumps(build_params, ensure_ascii=False)}"
                )
            return f"Failed to retrieve build parameters for job {job_name}."

    def tool_get_build_console(self) -> None:
        """Register get_build_console tool."""
        @mcp_tool(self.mcp)
        def get_build_console(
            job_name: str,
            build_number: int = None,
        ) -> str:
            """Get the build console output of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.
                build_number (int): The build number to retrieve. If None, retrieves the last build.

            Returns:
                Message with the build console output or failure reason.
            """
            console = JenkinsAPI().get_build_console(job_name, build_number)
            if console is not None:
                return f"Successfully retrieved build console output for job {job_name}: {console}"
            return f"Failed to retrieve build console output for job {job_name}."
