"""Contains utility functions for fetching configuration secrets for tests"""

import base64
import json
from typing import Dict

import boto3
import httpx

from crma_api_client.client import ConnectionInfo

# Secret stored in the nonprod AWS account
SECRET_NAME = "dev/nexio/crma-client"


def get_secret(secret_name: str) -> Dict[str, str]:
    """Gets a secret key from AWS Secrets Manager based on the secret_name

    Args:
        secret_name: AWS secret name

    Return:
        the decoded secret dict

    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
    )

    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response:
        secret = response["SecretString"]
    else:
        secret = base64.b64decode(response["SecretBinary"])

    return json.loads(secret)


def get_connection_info(secret_name: str = SECRET_NAME) -> ConnectionInfo:
    """Get connection info for the dev Salesforce instance

    Args:
        secret_name: AWS secret name. Defaults to SECRET_NAME.

    Returns:
        ConnectionInfo object

    """
    secret = get_secret(secret_name)
    response = httpx.post(
        "https://login.salesforce.com/services/oauth2/token",
        data=secret,
        headers={"Accept": "application/json"},
    )
    return ConnectionInfo.parse_obj(response.json())
