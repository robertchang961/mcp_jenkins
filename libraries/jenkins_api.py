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
            logging.info(f"[Job] {job_name} found in all jobs.")
        else:
            logging.warning(f"[Job] {job_name} not found in all jobs.")
        return is_exists

    def is_job_queued_or_running(self, job_name: str) -> bool:
        """Check if a job is queued or running on the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            True if the job is queued or running, False otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            logging.info(f"[Job] {job_name} is queued or running.")
            return job.is_queued_or_running()
        logging.info(f"[Job] {job_name} not queued or running.")
        return False

    def get_job(self, job_name: str) -> jenkinsapi.job.Job | None:
        """Get a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            A jenkinsapi.job.Job instance if found, None otherwise.
        """
        if self.is_job_exists(job_name):
            job = self.jenkins_server.get_job(job_name)
            return job

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
            logging.info(f"[Job] {job_name} default parameters retrieved {params}.")
            return params
        logging.info(f"[Job] {job_name} default parameters not found.")

    def get_job_baseurl(self, job_name: str) -> str | None:
        """Get the base URL of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The base URL of the job if found, None otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            logging.info(f"[Job] {job_name} base URL retrieved: {job.baseurl}.")
            return job.baseurl
        logging.info(f"[Job] {job_name} base URL not found.")

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
            logging.info(f'[Job] Searching jobs with string "{search_string}" in view: {view_name}')
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
            logging.info(f'[Job] Searching jobs with string "{search_string}" in all jobs.')
            all_jobs = self.jenkins_server.get_jobs_list()

        escaped_search_string = re.escape(search_string)
        if is_case_sensitive:
            matching_jobs = [job for job in all_jobs if re.search(rf"{escaped_search_string}", job)]
        else:
            matching_jobs = [job for job in all_jobs if re.search(rf"{escaped_search_string}", job, re.IGNORECASE)]

        if matching_jobs:
            logging.info(f"[Job] Found {len(matching_jobs)} matching jobs.")
        else:
            logging.info("[Job] No matching jobs found.")
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
            logging.info(f"[Job] {job_name} created successfully.")
            return job
        except Exception as e:
            logging.error(f"[Job] Failed to create job {job_name}: {e}")

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
                logging.info(f"[Job] {job_name} cloned to {new_job_name}.")
                return job
            except Exception as e:
                logging.error(f"[Job] Failed to clone job {job_name} to {new_job_name}: {e}")

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
                logging.info(f"[Job] {job_name} renamed to {new_job_name}.")
                return job
            except Exception as e:
                logging.error(f"[Job] Failed to rename job {job_name} to {new_job_name}: {e}")

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
                logging.info(f"[Job] {job_name} deleted successfully.")
                return True
            except Exception as e:
                logging.error(f"[Job] Failed to delete job {job_name}: {e}")
        return False

    def build_job(self, job_name: str, params: dict = None) -> bool:
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
                logging.info(f"[Job] Build triggered for job {job_name}.")
                return True
            except Exception as e:
                logging.error(f"[Job] Failed to trigger build for job {job_name}: {e}")
                return False

    # ==================== View ====================
    def get_views(self) -> list[str]:
        """Get all views with global view from the Jenkins server.

        Returns:
            A list of view names.
        """
        views = self.jenkins_server.views.keys()
        logging.info("[View] Retrieving all views from Jenkins server.")
        return views

    def get_view(self, view_name: str) -> jenkinsapi.view.View | None:
        """Get a specific view from the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            A jenkinsapi.view.View instance, or None if not found.
        """
        if view_name in self.get_views():
            logging.info(f"[View] {view_name} found in all views.")
            return self.jenkins_server.views[view_name]
        else:
            logging.warning(f"[View] {view_name} not found in all views.")

    def get_jobs_from_view(self, view_name: str) -> list[str] | None:
        """Get all jobs from a global view or personal view on the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            A list of job names, or None if the view was not found.
        """
        view = self.get_view(view_name)
        if view is not None:
            logging.info(f"[View] Retrieved jobs from all views within {view_name}.")
            return list(view.keys())
        else:
            url = f"{self.base_url}/user/{self.username}/my-views/view/{view_name}/api/json"
            try:
                response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password_or_token.get_secret_value()))
                response.raise_for_status()
                data = response.json()
                logging.info(f"[View] Retrieved jobs from my-views within {view_name}.")
                return [job["name"] for job in data.get("jobs", {}) if "name" in job]
            except requests.HTTPError as e:
                logging.error(f"[View] Failed to get jobs from my-views within {view_name}: {e}")

    def get_view_baseurl(self, view_name: str) -> str | None:
        """Get the base URL of a global view from the Jenkins server.

        Args:
            view_name (str): The name of the view.

        Returns:
            The base URL of the view, or None if not found.
        """
        view = self.get_view(view_name)
        if view is not None:
            logging.info(f"[View] {view_name} base URL retrieved: {view.baseurl}.")
            return view.baseurl
        logging.info(f"[View] {view_name} base URL not found.")

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
            logging.info(f"[View] Job {job_name} added to view {view_name}.")
            return True
        logging.error(f"[View] Job {job_name} not added to view {view_name}.")
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
            logging.info(f"[View] Job {job_name} removed from view {view_name}.")
            return True
        logging.error(f"[View] Job {job_name} not removed from view {view_name}.")
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
            logging.info(f"[Build] Stopping last build of job {job_name}.")
            return build.stop()

    def get_last_build(self, job_name: str) -> jenkinsapi.build.Build | None:
        """Get the last build of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build of the job if found, None otherwise.
        """
        job = self.get_job(job_name)
        if job is not None:
            build = job.get_last_build_or_none()
            return build

    def get_last_build_number(self, job_name: str) -> int | None:
        """Get the last build number of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            logging.info(f"[Build] Last build number retrieved for job {job_name}.")
            return build.get_number()

    def get_last_build_start_time(self, job_name: str) -> datetime | None:
        """Get the last build start time of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build start time of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            utc_time = build.get_timestamp()
            local_time = utc_time.astimezone()
            logging.info(f"[Build] Last build start time retrieved for job {job_name}.")
            return local_time

    def get_last_build_duration(self, job_name: str) -> int | None:
        """Get the last build duration of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build duration of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            logging.info(f"[Build] Last build duration retrieved for job {job_name}.")
            return build.get_duration()

    def get_last_build_status(self, job_name: str) -> str | None:
        """Get the last build status of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build status (SUCCESS, FAILURE, ABORTED) of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            logging.info(f"[Build] Last build status retrieved for job {job_name}.")
            return build.get_status()

    def get_last_build_params(self, job_name: str) -> dict | None:
        """Get the last build parameters of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build parameters of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            logging.info(f"[Build] Last build parameters retrieved for job {job_name}.")
            return build.get_params()

    def get_last_build_console(self, job_name: str) -> str | None:
        """Get the last build console output of a job from the Jenkins server.

        Args:
            job_name (str): The name of the job.

        Returns:
            The last build console output of the job if found, None otherwise.
        """
        build = self.get_last_build(job_name)
        if build is not None:
            logging.info(f"[Build] Last build console output retrieved for job {job_name}.")
            return build.get_console()
