"""Contains definitions for the Query resource"""


from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel

from .util import to_camel


class QueryLanguage(str, Enum):
    """Query language"""

    saql = "SAQL"
    sql = "SQL"


class QueryResults(BaseModel):
    """Query results model"""

    records: List[Dict[str, Any]]


class QueryResponse(BaseModel):
    """Response model for the query resource"""

    action: str
    response_id: str
    results: QueryResults
    query: str
    response_time: int

    class Config:
        """Model configuration"""

        alias_generator = to_camel
