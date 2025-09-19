"""Jenkins job management tool registration for FastMCP.

This module provides a registrar class to register Jenkins job-related tools
to the FastMCP server.
"""

import json

from mcp.server.fastmcp import FastMCP

from libraries.jenkins_api import JenkinsAPI
from tools.tool_common import mcp_tool


class JenkinsJobToolsRegistrar:
    """Registrar for Jenkins job management tools.

    This class registers job-related tools to the FastMCP server.
    """

    def __init__(self, mcp: FastMCP) -> None:
        """Initialize JobToolsRegistrar and register all job tools.

        Args:
            mcp (FastMCP): The FastMCP server instance.
        """
        self.mcp = mcp

    def register(self) -> None:
        """Register all Jenkins job management tools to FastMCP.

        This method decorates and registers job-related tools.
        """
        self.tool_is_job_exists()
        self.tool_is_job_queued_or_running()
        self.tool_get_job_default_params()
        self.tool_get_job_baseurl()
        self.tool_search_job()
        self.tool_create_job()
        self.tool_clone_job()
        self.tool_rename_job()
        self.tool_delete_job()
        self.tool_build_job()

    def tool_is_job_exists(self) -> None:
        """Register is_job_exists tool."""
        @mcp_tool(self.mcp)
        def is_job_exists(job_name: str) -> str:
            """Check if a job exists on the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message indicating whether the job exists.
            """
            is_exists = JenkinsAPI().is_job_exists(job_name)
            if is_exists:
                return f"Job {job_name} exists."
            return f"Job {job_name} does not exist."

    def tool_is_job_queued_or_running(self) -> None:
        """Register is_job_queued_or_running tool."""
        @mcp_tool(self.mcp)
        def is_job_queued_or_running(job_name: str) -> str:
            """Check if a job is queued or running on the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message indicating whether the job is queued or running.
            """
            is_queued_or_running = JenkinsAPI().is_job_queued_or_running(job_name)
            if is_queued_or_running:
                return f"Job {job_name} is queued or running."
            return f"Job {job_name} is not queued or running."

    def tool_get_job_default_params(self) -> None:
        """Register get_job_default_params tool."""
        @mcp_tool(self.mcp)
        def get_job_default_params(job_name: str) -> str:
            """Get default parameters for a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the default parameters or failure reason.
            """
            params = JenkinsAPI().get_job_default_params(job_name)
            if params is not None:
                return (
                    f"Job {job_name} default parameters: "
                    f"{json.dumps(params, ensure_ascii=False)}"
                )
            return f"Failed to get default parameters for job {job_name}."

    def tool_get_job_baseurl(self) -> None:
        """Register get_job_baseurl tool."""
        @mcp_tool(self.mcp)
        def get_job_baseurl(job_name: str) -> str:
            """Get the base URL of a job from the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message with the job base URL or failure reason.
            """
            url = JenkinsAPI().get_job_baseurl(job_name)
            if url:
                return f"Job {job_name} base URL: {url}"
            return f"Failed to get base URL for job {job_name}."

    def tool_search_job(self) -> None:
        """Register search_job tool."""
        @mcp_tool(self.mcp)
        def search_job(
            search_string: str,
            view_name: str = None,
            is_case_sensitive: bool = True,
        ) -> str:
            """Search for jobs by name on the Jenkins server.

            Args:
                search_string (str): The pattern to search for in job names.
                view_name (str): The name of the view to search within.
                is_case_sensitive (bool): Whether the search should be case sensitive.

            Returns:
                Message with the search results or failure reason.
            """
            matching_jobs = JenkinsAPI().search_job(
                search_string=search_string,
                view_name=view_name,
                is_case_sensitive=is_case_sensitive,
            )
            if matching_jobs:
                return (
                    f"Found {len(matching_jobs)} jobs: "
                    f"{json.dumps(matching_jobs, ensure_ascii=False)}"
                )
            return "No matching jobs found."

    def tool_create_job(self) -> None:
        """Register create_job tool."""
        @mcp_tool(self.mcp)
        def create_job(
            job_name: str,
            config_xml: str = None,
        ) -> str:
            """Create a new job on the Jenkins server.

            Args:
                job_name (str): The name of the job.
                config_xml (str): The XML configuration for the job.

            Returns:
                Message indicating job creation success or failure.
            """
            job = JenkinsAPI().create_job(job_name, config_xml)
            if job is not None:
                return f"Successfully created job {job_name}."
            return f"Failed to create job {job_name}."

    def tool_clone_job(self) -> None:
        """Register clone_job tool."""
        @mcp_tool(self.mcp)
        def clone_job(
            job_name: str,
            new_job_name: str,
        ) -> str:
            """Clone or copy an existing job on the Jenkins server.

            Args:
                job_name (str): The name of the job.
                new_job_name (str): The name of the new cloned job.

            Returns:
                Message indicating job clone success or failure.
            """
            job = JenkinsAPI().clone_job(job_name, new_job_name)
            if job is not None:
                return f"Successfully cloned job {job_name} to {new_job_name}."
            return f"Failed to clone job {job_name} to {new_job_name}."

    def tool_rename_job(self) -> None:
        """Register rename_job tool."""
        @mcp_tool(self.mcp)
        def rename_job(
            job_name: str,
            new_job_name: str,
        ) -> str:
            """Rename an existing job on the Jenkins server.

            Args:
                job_name (str): The name of the job.
                new_job_name (str): The new name for the job.

            Returns:
                Message indicating job rename success or failure.
            """
            job = JenkinsAPI().rename_job(job_name, new_job_name)
            if job is not None:
                return f"Successfully renamed job {job_name} to {new_job_name}."
            return f"Failed to rename job {job_name} to {new_job_name}."

    def tool_delete_job(self) -> None:
        """Register delete_job tool."""
        @mcp_tool(self.mcp)
        def delete_job(job_name: str) -> str:
            """Delete a specific job on the Jenkins server.

            Args:
                job_name (str): The name of the job.

            Returns:
                Message indicating job deletion success or failure.
            """
            is_deleted = JenkinsAPI().delete_job(job_name)
            if is_deleted:
                return f"Successfully deleted job {job_name}."
            return f"Failed to delete job {job_name}."

    def tool_build_job(self) -> None:
        """Register build_job tool."""
        @mcp_tool(self.mcp)
        def build_job(job_name: str, params: dict = None) -> str:
            """Trigger a build for a specific job on the Jenkins server.

            Args:
                job_name (str): The name of the job to build.
                params (dict): Build parameters to pass to the job.

            Returns:
                Message indicating build trigger success or failure.
            """
            is_builded = JenkinsAPI().build_job(job_name, params)
            if is_builded:
                return f"Successfully triggered build for job {job_name}."
            return f"Failed to trigger build for job {job_name}."
