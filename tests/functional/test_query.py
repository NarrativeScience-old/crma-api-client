"""Contains functional tests for the query resource"""

import pytest

from crma_api_client.client import CRMAAPIClient
from crma_api_client.resources.query import ProjectionField


@pytest.mark.asyncio
async def test_query(client: CRMAAPIClient):
    """Should run a simple query"""
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
    response = await client.query(query)
    assert response.results.records == [
        {"Category": "Furniture", "Sales": 741999.7953},
        {"Category": "Office Supplies", "Sales": 719047.032},
        {"Category": "Technology", "Sales": 836154.033},
    ]
    assert response.fields == [
        ProjectionField(id="q.Category", type="string"),
        ProjectionField(id="q.Sales", type="numeric"),
    ]
    assert response.fields[0].name == "Category"
