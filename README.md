# crma-api-client
[![](https://img.shields.io/pypi/v/crma_api_client.svg)](https://pypi.org/pypi/crma_api_client/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

CRM Analytics REST API Client

Features:

- Execute SAQL queries
- List dataset versions

Table of Contents:

- [Installation](#installation)
- [Guide](#guide)
- [Development](#development)

## Installation

crma-api-client requires Python 3.9 or above.

```bash
pip install crma-api-client
# or
poetry add crma-api-client
```

## Guide

First, you need to create a new client instance. To do that, you either need to have credentials for an OAuth app or an existing access token handy:

```python
from crma_api_client.client import ConnectionInfo, CRMAAPIClient

# Generate connection info if you don't already have an access token
conn = await ConnectionInfo.generate(
    client_id="abc123",
    client_secret="***",
    username="me@salesforce.com",
    password="***"
)

# If you already have an instance URL and access token, you can instantiate directly
conn = ConnectionInfo(instance_url="https://company.my.salesforce.com", access_token="XYZ123")

# Create the client, passing in the connection object
client = CRMAAPIClient(conn)
```

Next, you can use methods on the client to make requests:

```python
from crma_api_client.resources.query import QueryRequest

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
response = await client.query(QueryRequest(query=query))
assert response.results.records == [
    {"Category": "Furniture", "Sales": 741999.7953},
    {"Category": "Office Supplies", "Sales": 719047.032},
    {"Category": "Technology", "Sales": 836154.033},
]
```

## Development

To develop crma-api-client, install dependencies and enable the pre-commit hook:

```bash
pip install pre-commit poetry
poetry install
pre-commit install -t pre-commit -t pre-push
```

To run tests:

```bash
poetry run pytest
```
