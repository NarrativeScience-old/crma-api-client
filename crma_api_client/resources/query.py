"""Contains definitions for the Query resource"""


from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from .util import to_camel


class QueryLanguage(str, Enum):
    """Query language"""

    saql = "SAQL"
    sql = "SQL"


class QueryRequest(BaseModel):
    """Request model for the query resource"""

    name: str = Field(default_factory=lambda: str(uuid4()))
    query: str
    query_language: QueryLanguage = QueryLanguage.saql
    timezone: Optional[str] = None

    class Config:
        """Model configuration"""

        alias_generator = to_camel


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
