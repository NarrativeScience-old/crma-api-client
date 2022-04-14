"""Contains definitions for the Query resource"""


from enum import Enum
from functools import cached_property
from typing import Any, Dict, List

from pydantic import BaseModel

from .util import to_camel


class QueryLanguage(str, Enum):
    """Query language"""

    saql = "SAQL"
    sql = "SQL"


class ProjectionField(BaseModel):
    """Field projected in the query result"""

    id: str
    type: str

    @cached_property
    def name(self) -> str:
        """Return field name that omits stream reference"""
        return self.id.split(".")[-1]

    class Config:
        """Model configuration"""

        keep_untouched = (cached_property,)


class LineageProjection(BaseModel):
    """Field projection metadata container"""

    field: ProjectionField


class QueryLineage(BaseModel):
    """Lineage that describes field projections in a query result"""

    type: str
    projections: List[LineageProjection]


class QueryResultsMetadata(BaseModel):
    """Query results metadata"""

    lineage: QueryLineage
    query_language: QueryLanguage

    class Config:
        """Model configuration"""

        alias_generator = to_camel


class QueryResults(BaseModel):
    """Query results model"""

    metadata: List[QueryResultsMetadata]
    records: List[Dict[str, Any]]


class QueryResponse(BaseModel):
    """Response model for the query resource

    See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_query.htm
    """

    action: str
    response_id: str
    results: QueryResults
    query: str
    response_time: int

    @cached_property
    def fields(self) -> List[ProjectionField]:
        """Return the fields from the query response metadata

        This assumes there is only one metadata object and one lineage object.
        """
        return [p.field for p in self.results.metadata[0].lineage.projections]

    class Config:
        """Model configuration"""

        alias_generator = to_camel
        keep_untouched = (cached_property,)
