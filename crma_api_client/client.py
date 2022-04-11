"""Contains the CRMA API client"""

import logging
from typing import Any, Dict, Optional

import backoff
import httpx
from pydantic import BaseModel

from crma_api_client.resources.dataset import DatasetVersionsResponse
from crma_api_client.resources.query import QueryRequest, QueryResponse
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
            DatasetVersionsResponse object

        """
        response = await self.request(f"/wave/datasets/{identifier}/versions", "GET")
        return DatasetVersionsResponse.parse_obj(response.json())

    async def query(self, req: QueryRequest) -> QueryResponse:
        """Execute a query

        Args:
            req: Query request object

        Returns:
            QueryResponse object

        """
        response = await self.request(
            "/wave/query", "POST", req.dict(by_alias=True, exclude_none=True)
        )
        return QueryResponse.parse_obj(response.json())
