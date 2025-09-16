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
        self.register_stop_last_build_tool()
        self.register_get_last_build_number_tool()
        self.register_get_last_build_start_time_tool()
        self.register_get_last_build_duration_tool()
        self.register_get_last_build_status_tool()
        self.register_get_last_build_params_tool()
        self.register_get_last_build_console_tool()

    def register_stop_last_build_tool(self) -> None:
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

    def register_get_last_build_number_tool(self) -> None:
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

    def register_get_last_build_start_time_tool(self) -> None:
        """Register get_last_build_start_time tool."""
        @mcp_tool(self.mcp)
        def get_last_build_start_time(job_name: str) -> str | None:
            """Get the last build start time of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build start time or failure reason.
            """
            local_time = JenkinsAPI().get_last_build_start_time(job_name)
            if local_time is not None:
                return f"Successfully retrieved last build start time for job {job_name}: {local_time}"
            return f"Failed to retrieve last build start time for job {job_name}."

    def register_get_last_build_duration_tool(self) -> None:
        """Register get_last_build_duration tool."""
        @mcp_tool(self.mcp)
        def get_last_build_duration(
            job_name: str,
        ) -> str:
            """Get the last build duration of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build duration or failure reason.
            """
            duration = JenkinsAPI().get_last_build_duration(job_name)
            if duration is not None:
                return f"Successfully retrieved last build duration for job {job_name}: {duration} ms"
            return f"Failed to retrieve last build duration for job {job_name}."

    def register_get_last_build_status_tool(self) -> None:
        """Register get_last_build_status tool."""
        @mcp_tool(self.mcp)
        def get_last_build_status(
            job_name: str,
        ) -> str:
            """Get the last build status of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build status or failure reason.
            """
            status = JenkinsAPI().get_last_build_status(job_name)
            if status is not None:
                return f"Successfully retrieved last build status for job {job_name}: {status}"
            return f"Failed to retrieve last build status for job {job_name}."

    def register_get_last_build_params_tool(self) -> None:
        """Register get_last_build_params tool."""
        @mcp_tool(self.mcp)
        def get_last_build_params(job_name: str) -> str | None:
            """Get the last build parameters of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build parameters or failure reason.
            """
            build_params = JenkinsAPI().get_last_build_params(job_name)
            if build_params is not None:
                return (
                    f"Successfully retrieved last build parameters for job {job_name}: "
                    f"{json.dumps(build_params, ensure_ascii=False)}"
                )
            return f"Failed to retrieve last build parameters for job {job_name}."

    def register_get_last_build_console_tool(self) -> None:
        """Register get_last_build_console tool."""
        @mcp_tool(self.mcp)
        def get_last_build_console(
            job_name: str,
        ) -> str:
            """Get the last build console output of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the last build console output or failure reason.
            """
            console = JenkinsAPI().get_last_build_console(job_name)
            if console is not None:
                return f"Successfully retrieved last build console output for job {job_name}: {console}"
            return f"Failed to retrieve last build console output for job {job_name}."
