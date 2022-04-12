"""Contains the CRMA API client"""

import logging
from typing import Any, Dict, Optional
from uuid import uuid4

import backoff
import httpx
from pydantic import BaseModel

from crma_api_client.resources.dataset import DatasetVersionsResponse
from crma_api_client.resources.query import QueryLanguage, QueryResponse
from .encoder import json_dumps_common

logger = logging.getLogger(__name__)


class ConnectionInfo(BaseModel):
    """Model with info for making API requests to a Salesforce instance"""

    instance_url: str
    access_token: str
    token_type: str = "Bearer"

    @property
    def authorization(self) -> str:
        """Returns authorization header value"""
        return f"{self.token_type} {self.access_token}"

    @classmethod
    async def generate(
        cls,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        grant_type: str = "password",
    ) -> "ConnectionInfo":
        """Create a connection info object by generating a fresh token

        See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_rest_authentication.htm

        Args:
            client_id: OAuth app client ID
            client_secret: OAuth app client secret
            username: Username for the user calling the API
            password: Password for the user calling the API
            grant_type: OAuth grant type

        Returns:
            new ConnectionInfo object

        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://login.salesforce.com/services/oauth2/token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "username": username,
                    "password": password,
                    "grant_type": grant_type,
                },
                headers={"Accept": "application/json"},
            )
            return cls.parse_obj(response.json())


class CRMAAPIClient:
    """CRM Analytics REST API client"""

    def __init__(
        self,
        conn: ConnectionInfo,
        version: str = "v54.0",
        timeout: float = 60.0,
        connect_timeout: float = 5.0,
        logger: logging.Logger = logger,
    ) -> None:
        """Initialize the CRMAAPIClient

        Args:
            conn: Object containing for making API requests to a Salesforce instance.
            version: CRMA REST API version
            timeout: Default timeout for requests and non-connect operations, in seconds
            connect_timeout: Default timeout for establishing an HTTP connection, in
                seconds
            logger: Custom logger instance to use instead of the stdlib

        """
        self.logger = logger
        self._client = httpx.AsyncClient(
            base_url=conn.instance_url.rstrip("/") + f"/services/data/{version}",
            headers={"Authorization": conn.authorization},
            timeout=httpx.Timeout(timeout, connect=connect_timeout),
        )

    async def _get_headers(
        self,
    ) -> Dict[str, str]:
        """Get a headers dict from the calling context

        Returns:
            Dict containing headers to include in requests

        """
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
        }

        return headers

    @backoff.on_exception(
        backoff.expo,
        httpx.HTTPStatusError,
        max_tries=3,
        giveup=lambda e: e.response.status_code != 502,
    )
    async def request(
        self,
        path: str,
        method: str,
        json_data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Generic method to send a JSON request to the service

        Args:
            path: Path to the API resource. This path will be appended to the base url.
            method: HTTP method
            json_data: Request payload (for POST/PUT/PATCH requests)
            params: Request query params

        Returns:
            response object

        """
        path = "/" + path.strip("/")
        if json_data:
            json_data = json_dumps_common(json_data).encode()
        headers = await self._get_headers()
        self.logger.debug(f"Service request starting path={path} method={method}")
        response = await self._client.request(
            method.upper(),
            path,
            headers=headers,
            content=json_data,
            params=params,
            **kwargs,
        )
        self.logger.debug(
            f"Service request completed status_code={response.status_code}"
        )
        response.raise_for_status()
        return response

    async def list_dataset_versions(self, identifier: str) -> DatasetVersionsResponse:
        """List the versions for a dataset

        Args:
            identifier: Dataset name or ID

        Returns:
            list of all versions for the dataset

        """
        response = await self.request(f"/wave/datasets/{identifier}/versions", "GET")
        return DatasetVersionsResponse.parse_obj(response.json())

    async def query(
        self,
        query: str,
        query_language: QueryLanguage = QueryLanguage.saql,
        name: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> QueryResponse:
        """Execute a query

        Args:
            query: Query string
            query_language: Query language. One of: SAQL (default), SQL
            name: Query name. Defaults to a UUID
            timezone: Timezone for the query

        Returns:
            query results containing records and metadata

        """
        json_data = {
            "query": query,
            "name": name or str(uuid4()),
            "queryLanguage": query_language.value,
        }
        if timezone:
            json_data["timezone"] = timezone

        response = await self.request("/wave/query", "POST", json_data=json_data)

        return QueryResponse.parse_obj(response.json())
