"""Jenkins view management tool registration for FastMCP.

This module provides a registrar class to register Jenkins view-related tools
to the FastMCP server.
"""

import json

from mcp.server.fastmcp import FastMCP

from libraries.jenkins_api import JenkinsAPI
from tools.tool_common import mcp_tool


class JenkinsViewToolsRegistrar:
    """Registrar for Jenkins view management tools.

    This class registers view-related tools to the FastMCP server.
    """

    def __init__(self, mcp: FastMCP) -> None:
        """Initialize JenkinsViewToolsRegistrar and register all view tools.

        Args:
            mcp (FastMCP): The FastMCP server instance.
        """
        self.mcp = mcp

    def register(self) -> None:
        """Register all view management tools to FastMCP."""
        self.tool_get_views()
        self.tool_get_jobs_from_view()
        self.tool_get_view_baseurl()
        self.tool_add_job_to_view()
        self.tool_remove_job_from_view()

    def tool_get_views(self) -> None:
        """Register get_views tool."""
        @mcp_tool(self.mcp)
        def get_views() -> str:
            """Get all views from the Jenkins server.

            Returns:
                Message with the list of views or failure reason.
            """
            views = JenkinsAPI().get_views()
            if views:
                return (
                    f"Found {len(views)} views: "
                    f"{json.dumps(list(views), ensure_ascii=False)}"
                )
            return "No views found."

    def tool_get_jobs_from_view(self) -> None:
        """Register get_jobs_from_view tool."""
        @mcp_tool(self.mcp)
        def get_jobs_from_view(view_name: str) -> str:
            """Get all jobs from a view on the Jenkins server.

            Args:
                view_name (str): The name of the view.

            Returns:
                Message with the list of jobs or failure reason.
            """
            jobs = JenkinsAPI().get_jobs_from_view(view_name)
            if jobs:
                return (
                    f"View {view_name} contains {len(jobs)} jobs: "
                    f"{json.dumps(jobs, ensure_ascii=False)}"
                )
            return f"No jobs found in view {view_name}."

    def tool_get_view_baseurl(self) -> None:
        """Register get_view_baseurl tool."""
        @mcp_tool(self.mcp)
        def get_view_baseurl(view_name: str) -> str:
            """Get the base URL of a specific view from the Jenkins server.

            Args:
                view_name (str): The name of the view.

            Returns:
                Message with the view base URL or failure reason.
            """
            url = JenkinsAPI().get_view_baseurl(view_name)
            if url:
                return f"Successfully retrieved base URL for view {view_name}: {url}"
            return f"Failed to retrieve base URL for view {view_name}."

    def tool_add_job_to_view(self) -> None:
        """Register add_job_to_view tool."""
        @mcp_tool(self.mcp)
        def add_job_to_view(
            view_name: str,
            job_name: str,
        ) -> str:
            """Add a job to a specific view on the Jenkins server.

            Args:
                view_name (str): The name of the view.
                job_name (str): The name of the job.

            Returns:
                Message indicating job add success or failure.
            """
            is_added = JenkinsAPI().add_job_to_view(view_name, job_name)
            if is_added:
                return f"Successfully added job {job_name} to view {view_name}."
            return f"Failed to add job {job_name} to view {view_name}."

    def tool_remove_job_from_view(self) -> None:
        """Register remove_job_from_view tool."""
        @mcp_tool(self.mcp)
        def remove_job_from_view(
            view_name: str,
            job_name: str,
        ) -> str:
            """Remove a job from a specific view on the Jenkins server.

            Args:
                view_name (str): The name of the view.
                job_name (str): The name of the job.

            Returns:
                Message indicating job removal success or failure.
            """
            is_removed = JenkinsAPI().remove_job_from_view(view_name, job_name)
            if is_removed:
                return f"Successfully removed job {job_name} from view {view_name}."
            return f"Failed to remove job {job_name} from view {view_name}."
