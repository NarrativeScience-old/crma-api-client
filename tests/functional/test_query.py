"""Contains functional tests for the query resource"""

import pytest
from secret import get_secret

from crma_api_client.client import ConnectionInfo, CRMAAPIClient
from crma_api_client.resources.query import QueryRequest


@pytest.fixture()
async def conn():
    """Get a connection info object for making requests using the API client"""
    return await ConnectionInfo.generate(**get_secret())


@pytest.mark.asyncio
async def test_query(conn):
    """Should run a simple query"""
    client = CRMAAPIClient(conn)
    response = await client.list_dataset_versions("Sample_Superstore_xls_Orders")
    version = response.versions[0]
    query = "\n".join(
        [
            f"""q = load "{version.dataset.id}/{version.id}";""",
            """q = group q by 'Category';""",
            """q = foreach q generate q.'Category' as 'Category', sum(q.'Sales') as 'Sales';""",
            """q = order q by 'Category' asc;""",
        ]
    )
    response = await client.query(QueryRequest(name="test", query=query))
    assert response.results.records == [
        {"Category": "Furniture", "Sales": 741999.7953},
        {"Category": "Office Supplies", "Sales": 719047.032},
        {"Category": "Technology", "Sales": 836154.033},
    ]
