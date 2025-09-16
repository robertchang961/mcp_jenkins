"""Register prompts."""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

from prompts import template_prompts


def register_prompts(mcp: FastMCP) -> None:
    """Register prompts."""

    # ==================== Job ====================
    @mcp.prompt(title="Prompt Get Job Default Params")
    def prompt_get_job_default_params(job_name: str) -> list[base.Message]:
        """Get default parameters for a Jenkins job.

        Args:
            job_name (str): The name of the job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_get_job_default_params.format(
            job_name=job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Get Job Baseurl")
    def prompt_get_job_baseurl(job_name: str) -> list[base.Message]:
        """Get base URL for a Jenkins job.

        Args:
            job_name (str): The name of the job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_get_job_baseurl.format(
            job_name=job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Search Job")
    def prompt_search_job(
        search_string: str,
        view_name: str = "",
        is_case_sensitive: bool = False,
    ) -> list[base.Message]:
        """Search for Jenkins jobs matching the given criteria.

        Args:
            search_string (str): The string to search for in job names.
            view_name (str): The name of the view to search within.
            is_case_sensitive (bool): Whether the search should be case sensitive.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_search_job.format(
            search_string=search_string,
            view_name=view_name,
            is_case_sensitive=is_case_sensitive,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Clone Job")
    def prompt_clone_job(job_name: str, new_job_name: str) -> list[base.Message]:
        """Clone a Jenkins job.

        Args:
            job_name (str): The name of the job to clone.
            new_job_name (str): The name of the new job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_clone_job.format(
            job_name=job_name,
            new_job_name=new_job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Rename Job")
    def prompt_rename_job(job_name: str, new_job_name: str) -> list[base.Message]:
        """Rename a Jenkins job.

        Args:
            job_name (str): The name of the job to rename.
            new_job_name (str): The new name for the job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_rename_job.format(
            job_name=job_name,
            new_job_name=new_job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Delete Job")
    def prompt_delete_job(job_name: str) -> list[base.Message]:
        """Delete a Jenkins job.

        Args:
            job_name (str): The name of the job to delete.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_delete_job.format(
            job_name=job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Build Job")
    def prompt_build_job(job_name: str, params: str = "") -> list[base.Message]:
        """Build a Jenkins job.

        Args:
            job_name (str): The name of the job to build.
            params (str): The parameters for the job (if any).

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_build_job.format(
            job_name=job_name,
            params=params,
        )))
        return prompt_msg

    # ==================== View ====================
    @mcp.prompt(title="Prompt Get Views")
    def prompt_get_views() -> list[base.Message]:
        """Get all Jenkins views.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_get_views))
        return prompt_msg

    @mcp.prompt(title="Prompt Get View Baseurl")
    def prompt_get_view_baseurl(view_name: str) -> list[base.Message]:
        """Get base URL for a Jenkins view.

        Args:
            view_name (str): The name of the view.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_get_view_baseurl.format(
            view_name=view_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Add Job To View")
    def prompt_add_job_to_view(job_name: str, view_name: str) -> list[base.Message]:
        """Add a Jenkins job to a view.

        Args:
            job_name (str): The name of the job.
            view_name (str): The name of the view.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_add_job_to_view.format(
            job_name=job_name,
            view_name=view_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Remove Job From View")
    def prompt_remove_job_from_view(job_name: str, view_name: str) -> list[base.Message]:
        """Remove a Jenkins job from a view.

        Args:
            job_name (str): The name of the job.
            view_name (str): The name of the view.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_remove_job_from_view.format(
            job_name=job_name,
            view_name=view_name,
        )))
        return prompt_msg

    # ==================== Build ====================
    @mcp.prompt(title="Prompt Stop Last Build")
    def prompt_stop_last_build(job_name: str) -> list[base.Message]:
        """Stop the last build of a Jenkins job.

        Args:
            job_name (str): The name of the job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_stop_last_build.format(
            job_name=job_name,
        )))
        return prompt_msg

    @mcp.prompt(title="Prompt Get Last Build Info")
    def prompt_get_last_build_info(job_name: str) -> list[base.Message]:
        """Get last build info for a Jenkins job.

        Args:
            job_name (str): The name of the job.

        Returns:
            List of messages forming the prompt.
        """
        prompt_msg = []
        prompt_msg.append(base.UserMessage(template_prompts.persona))
        prompt_msg.append(base.UserMessage(template_prompts.prompt_get_last_build_info.format(
            job_name=job_name,
        )))
        return prompt_msg
