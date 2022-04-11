# crma-api-client
[![](https://img.shields.io/pypi/v/crma_api_client.svg)](https://pypi.org/pypi/crma_api_client/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

CRM Analytics REST API Client

Features:

- <!-- list of features -->

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

<!-- Subsections explaining how to use the package -->

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
