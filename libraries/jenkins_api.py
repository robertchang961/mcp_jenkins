"""Jenkins API wrapper for job, view, and build management."""

import logging
import re
from datetime import datetime

import jenkinsapi
import requests
from jenkins import EMPTY_CONFIG_XML
from requests.auth import HTTPBasicAuth

from libraries.jenkins_server import JenkinsServer


class JenkinsAPI:
    """Jenkins API wrapper for job, view, and build management."""

    def __init__(self) -> None:
        """Initialize the Jenkins server instance."""
        self.server = JenkinsServer()
        self.base_url = self.server.base_url
        self.username = self.server.username
        self.password_or_token = self.server.password_or_token
        self.jenkins_server = self.server.jenkins_server

    # ==================== Job ====================
    def is_job_exists(self, job_name: str) -> bool:
        """Check if a job exists on the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            True if the job exists, False otherwise.
        """
        is_exists = self.jenkins_server.has_job(job_name)
        if is_exists:
            logging.info(f"[Job][{job_name}] found in all jobs.")
        else:
            logging.warning(f"[Job][{job_name}] not found in all jobs.")
        return is_exists

    def is_job_queued_or_running(self, job_name: str) -> bool:
        """Check if a job is queued or running on the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            True if the job is queued or running, False otherwise.
        """
        job = self.get_job(job_name)
        is_queued_or_running = job.is_queued_or_running()
        if is_queued_or_running:
            logging.info(f"[Job][{job_name}] is queued or running.")
        else:
            logging.info(f"[Job][{job_name}] is not queued or running.")
        return is_queued_or_running

    def get_job(self, job_name: str) -> jenkinsapi.job.Job | None:
        """Get a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            A jenkinsapi.job.Job instance if found, None otherwise.
        """
        if self.is_job_exists(job_name):
            job = self.jenkins_server.get_job(job_name)
            logging.info(f"[Job][{job_name}] successfully get job.")
            return job
        logging.error(f"[Job][{job_name}] failed to get job.")

    def get_job_default_params(self, job_name: str) -> dict | None:
        """Get default parameters for a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            A dictionary of default parameters if found, None otherwise.
        """
        params = {}
        if self.is_job_exists(job_name):
            job = self.jenkins_server.get_job(job_name)
            for param in job.get_params():
                params[param["defaultParameterValue"]["name"]] = param["defaultParameterValue"]["value"]
            logging.info(f"[Job][{job_name}] successfully get default parameters: {params}.")
            return params
        logging.error(f"[Job][{job_name}] failed to get default parameters.")

    def get_job_baseurl(self, job_name: str) -> str | None:
        """Get the base URL of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The base URL of the job if found, None otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            logging.info(f"[Job][{job_name}] successfully get base URL: {job.baseurl}.")
            return job.baseurl
        logging.error(f"[Job][{job_name}] failed to get base URL.")

    def search_job(
        self,
        search_string: str,
        view_name: str = None,
        is_case_sensitive: bool = True,
    ) -> list[str]:
        """Search job by name.

        Args:
            search_string (str): The string to search for in job names.
            view_name (str): The name of the view to search within.
            is_case_sensitive (bool): Whether the search should be case sensitive.

        Returns:
            A list of job names that match the search string.
        """
        if view_name:
            logging.info(f'[Job] searching jobs with string "{search_string}" in view: {view_name}')
            view = self.get_view(view_name)
            if view is not None:
                all_jobs = list(view.keys())
            else:
                view = self.get_jobs_from_view(view_name)
                if view is not None:
                    all_jobs = view
                else:
                    return []
        else:
            logging.info(f'[Job] searching jobs with string "{search_string}" in all jobs.')
            all_jobs = self.jenkins_server.get_jobs_list()

        escaped_search_string = re.escape(search_string)
        if is_case_sensitive:
            matching_jobs = [job for job in all_jobs if re.search(rf"{escaped_search_string}", job)]
        else:
            matching_jobs = [job for job in all_jobs if re.search(rf"{escaped_search_string}", job, re.IGNORECASE)]

        if matching_jobs:
            logging.info(f"[Job] found {len(matching_jobs)} matching jobs.")
        else:
            logging.info("[Job] no matching jobs found.")
        return matching_jobs

    def create_job(
        self,
        job_name: str,
        config_xml: str = None,
    ) -> jenkinsapi.job.Job | None:
        """Create a new job on the Jenkins server.

        Args:
            job_name (str): The name of the job.
            config_xml (str): The XML configuration for the job.

        Returns:
            A jenkinsapi.job.Job instance, or None if the job creation failed.
        """
        try:
            if config_xml is None:
                config_xml = EMPTY_CONFIG_XML
            job = self.jenkins_server.create_job(job_name, config_xml)
            logging.info(f"[Job][{job_name}] successfully created job.")
            return job
        except Exception as e:
            logging.error(f"[Job][{job_name}] failed to create job: {e}")

    def clone_job(
        self,
        job_name: str,
        new_job_name: str,
    ) -> jenkinsapi.job.Job | None:
        """Clone or copy an existing job on the Jenkins server.

        Args:
            job_name (str): The name of the job.
            new_job_name (str): The name of the new cloned job.

        Returns:
            A jenkinsapi.job.Job instance, or None if the job cloning failed.
        """
        if self.is_job_exists(job_name):
            try:
                job = self.jenkins_server.copy_job(job_name, new_job_name)
                logging.info(f"[Job][{job_name}] successfully cloned to {new_job_name}.")
                return job
            except Exception as e:
                logging.error(f"[Job][{job_name}] failed to clone job to {new_job_name}: {e}")

    def rename_job(
        self,
        job_name: str,
        new_job_name: str,
    ) -> jenkinsapi.job.Job | None:
        """Rename an existing job on the Jenkins server.

        Args:
            job_name (str): The name of the job.
            new_job_name (str): The new name for the job.

        Returns:
            A jenkinsapi.job.Job instance, or None if the job was renamed failed.
        """
        if self.is_job_exists(job_name):
            try:
                job = self.jenkins_server.rename_job(job_name, new_job_name)
                logging.info(f"[Job][{job_name}] successfully renamed to {new_job_name}.")
                return job
            except Exception as e:
                logging.error(f"[Job][{job_name}] failed to rename job to {new_job_name}: {e}")

    def delete_job(self, job_name: str) -> bool:
        """Delete a specific job on the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            True if the job was deleted successfully, False otherwise.
        """
        if self.is_job_exists(job_name):
            try:
                self.jenkins_server.delete_job(job_name)
                logging.info(f"[Job][{job_name}] successfully deleted job.")
                return True
            except Exception as e:
                logging.error(f"[Job][{job_name}] failed to delete job: {e}")
        return False

    def build_job(
        self,
        job_name: str,
        params: dict = None,
    ) -> bool:
        """Trigger a build for a specific job on the Jenkins server.

        Args:
            job_name (str): The name of the job to build.
            params (dict): Build parameters to pass to the job.

        Returns:
            True if the build was triggered successfully, False otherwise.
        """
        if self.is_job_exists(job_name):
            try:
                self.jenkins_server.build_job(job_name, params)
                logging.info(f"[Job][{job_name}] successfully triggered build.")
                return True
            except Exception as e:
                logging.error(f"[Job][{job_name}] failed to trigger build: {e}")
                return False
        return False

    # ==================== View ====================
    def get_views(self) -> list[str]:
        """Get all views with global view from the Jenkins server.

        Returns:
            A list of view names.
        """
        views = self.jenkins_server.views.keys()
        logging.info("[View] get all views from Jenkins server.")
        return views

    def get_view(self, view_name: str) -> jenkinsapi.view.View | None:
        """Get a specific view from the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            A jenkinsapi.view.View instance, or None if not found.
        """
        if view_name in self.get_views():
            logging.info(f"[View][{view_name}] successfully get view in all views.")
            return self.jenkins_server.views[view_name]
        else:
            logging.error(f"[View][{view_name}] failed to get view in all views.")

    def get_jobs_from_view(self, view_name: str) -> list[str] | None:
        """Get all jobs from a global view or personal view on the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            A list of job names, or None if the view was not found.
        """
        view = self.get_view(view_name)
        if view is not None:
            logging.info(f"[View][{view_name}] successfully get jobs from all views.")
            return list(view.keys())
        else:
            url = f"{self.base_url}/user/{self.username}/my-views/view/{view_name}/api/json"
            try:
                response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password_or_token.get_secret_value()))
                response.raise_for_status()
                data = response.json()
                logging.info(f"[View][{view_name}] successfully get jobs from my-views.")
                return [job["name"] for job in data.get("jobs", {}) if "name" in job]
            except requests.HTTPError as e:
                logging.error(f"[View][{view_name}] failed to get jobs from my-views: {e}")

    def get_view_baseurl(self, view_name: str) -> str | None:
        """Get the base URL of a global view from the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            The base URL of the view, or None if not found.
        """
        view = self.get_view(view_name)
        if view is not None:
            logging.info(f"[View][{view_name}] successfully get base URL: {view.baseurl}.")
            return view.baseurl
        logging.error(f"[View][{view_name}] failed to get base URL.")

    def add_job_to_view(self, view_name: str, job_name: str) -> bool:
        """Add a job to a global view on the Jenkins server.

        Args:
            view_name (str): The name of the view.
            job_name (str): The name of the job.

        Returns:
            True if the job was added successfully, False otherwise.
        """
        view = self.get_view(view_name)
        if view is not None and self.is_job_exists(job_name):
            view.add_job(job_name)
            logging.info(f"[View][{view_name}] successfully add job {job_name}.")
            return True
        logging.error(f"[View][{view_name}] failed to add job {job_name}.")
        return False

    def remove_job_from_view(self, view_name: str, job_name: str) -> bool:
        """Remove a job from a global view on the Jenkins server.

        Args:
            view_name (str): The name of the view.
            job_name (str): The name of the job.

        Returns:
            True if the job was removed successfully, False otherwise.
        """
        view = self.get_view(view_name)
        if view is not None and self.is_job_exists(job_name):
            view.remove_job(job_name)
            logging.info(f"[View][{view_name}] successfully remove job {job_name}.")
            return True
        logging.error(f"[View][{view_name}] failed to remove job {job_name}.")
        return False

    # ==================== Build ====================
    def stop_last_build(self, job_name: str) -> bool:
        """Stop the last build of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            True if the build was stopped successfully, False otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            build = job.get_last_build_or_none()
            if build is not None:
                logging.info(f"[Build][{job_name}] successfully stop the last build of job.")
                return build.stop()
            else:
                logging.warning(f"[Build][{job_name}] no last build found for job.")
                return False
        logging.error(f"[Build][{job_name}] failed to stop the last build of job.")
        return False

    def get_build(
        self,
        job_name: str,
        build_number: int = None,
    ) -> jenkinsapi.build.Build | None:
        """Get the build of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The build of the job if found, None otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            if build_number is None:
                build = job.get_last_build_or_none()
                logging.info(f"[Build][{job_name}] successfully get last build of job.")
            else:
                build = job.get_build(build_number)
                logging.info(f"[Build][{job_name}] successfully get build {build_number} of job.")
            return build
        logging.error(f"[Build][{job_name}] failed to get build {build_number} of job.")

    def get_last_build_number(self, job_name: str) -> int | None:
        """Get the last build number of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build of the job if found, None otherwise.
        """
        build = self.get_build(job_name)
        if build is not None:
            logging.info(f"[Build][{job_name}] successfully get last build number.")
            return build.get_number()
        logging.error(f"[Build][{job_name}] failed to get last build number.")

    def get_build_start_time(
        self,
        job_name: str,
        build_number: int = None,
    ) -> datetime | None:
        """Get the build start time of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The build start time of the job if found, None otherwise.
        """
        build = self.get_build(job_name, build_number)
        if build is not None:
            utc_time = build.get_timestamp()
            local_time = utc_time.astimezone()
            logging.info(f"[Build][{job_name}] successfully get build {build_number} start time.")
            return local_time
        logging.error(f"[Build][{job_name}] failed to get build {build_number} start time.")

    def get_build_duration(
        self,
        job_name: str,
        build_number: int = None,
    ) -> int | None:
        """Get the build duration of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The build duration of the job if found, None otherwise.
        """
        build = self.get_build(job_name, build_number)
        if build is not None:
            logging.info(f"[Build][{job_name}] successfully get build {build_number} duration.")
            return build.get_duration()
        logging.error(f"[Build][{job_name}] failed to get build {build_number} duration.")

    def get_build_status(
        self,
        job_name: str,
        build_number: int = None,
    ) -> str | None:
        """Get the build status of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The build status (SUCCESS, FAILURE, ABORTED) of the job if found, None otherwise.
        """
        build = self.get_build(job_name, build_number)
        if build is not None:
            logging.info(f"[Build][{job_name}] successfully get build {build_number} status.")
            return build.get_status()
        logging.error(f"[Build][{job_name}] failed to get build {build_number} status.")

    def get_build_params(
        self,
        job_name: str,
        build_number: int = None,
    ) -> dict | None:
        """Get the last build parameters of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The last build parameters of the job if found, None otherwise.
        """
        build = self.get_build(job_name, build_number)
        if build is not None:
            logging.info(f"[Build][{job_name}] successfully get build {build_number} parameters.")
            return build.get_params()
        logging.error(f"[Build][{job_name}] failed to get build {build_number} parameters.")

    def get_build_console(
        self,
        job_name: str,
        build_number: int = None,
    ) -> str | None:
        """Get the last build console output of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.
            build_number (int): The build number to retrieve. If None, retrieves the last build.

        Returns:
            The last build console output of the job if found, None otherwise.
        """
        build = self.get_build(job_name, build_number)
        if build is not None:
            logging.info(f"[Build][{job_name}] successfully get build {build_number} console output.")
            return build.get_console()
        logging.error(f"[Build][{job_name}] failed to get build {build_number} console output.")
