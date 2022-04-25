"""Contains functional tests for the dataset resource"""

import pytest

from crma_api_client.client import CRMAAPIClient


@pytest.mark.asyncio
async def test_query(client: CRMAAPIClient):
    """Should get the metadata for a particular dataset"""
    dataset_id = "Sample_Superstore_xls_Orders"
    versions_response = await client.list_dataset_versions(dataset_id)
    version = versions_response.versions[0]
    await client.get_dataset_version(dataset_id, version.id)
