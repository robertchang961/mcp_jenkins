"""Provides classes and settings for connecting to and authenticating with a Jenkins server."""

import logging
from typing import Annotated

import requests
from jenkinsapi.jenkins import Jenkins
from pydantic import (
    BaseModel,
    Field,
    InstanceOf,
    SecretStr,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class JenkinsSettings(BaseSettings):
    """Read Jenkins settings from dotenv file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",    # ["allow", "ignore", "forbid"]
    )

    JENKINS_USERNAME: str
    JENKINS_PASSWORD_OR_TOKEN: SecretStr


class JenkinsServer(BaseModel):
    """Connects to Jenkins server and authenticates with username and password."""

    base_url: Annotated[str, Field(default="http://10.64.101.253:8080")]
    username: Annotated[str, Field(default=JenkinsSettings().JENKINS_USERNAME)]
    password_or_token: Annotated[SecretStr, Field(default=JenkinsSettings().JENKINS_PASSWORD_OR_TOKEN)]
    jenkins_server: Annotated[InstanceOf[Jenkins] | None, Field(default=None)]

    def model_post_init(self, __context: object) -> None:
        """Initialize the Jenkins server instance and attempt to log in."""
        jenkins_api = Jenkins(
            baseurl=self.base_url,
            username=self.username,
            password=self.password_or_token.get_secret_value(),
            timeout=10,
        )
        try:
            logging.info(f"[Auth] Welcome {self.username} login to Jenkins server {self.base_url}.")
            self.jenkins_server = jenkins_api
        except requests.HTTPError:
            logging.error(f"[Auth] Failed to login to Jenkins server {self.base_url}!")
            self.jenkins_server = None
