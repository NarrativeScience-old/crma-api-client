"""Contains shared functional test fixtures"""

import asyncio

import pytest
from secret import get_secret

from crma_api_client.client import ConnectionInfo, CRMAAPIClient


@pytest.fixture(scope="session")
def event_loop():
    """Returns the event loop so we can define async, session-scoped fixtures"""
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def client():
    """Create an authenticated client object"""
    conn = await ConnectionInfo.generate(**get_secret())
    return CRMAAPIClient(conn)
