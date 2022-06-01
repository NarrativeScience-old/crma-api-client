"""Contains definitions for the Query resource"""


from enum import Enum
from functools import cached_property
from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

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


class ForeachLineage(BaseModel):
    """Lineage that describes field projections in a query result"""

    type: Literal["foreach"] = "foreach"
    projections: List[LineageProjection]


class UnionLineage(BaseModel):
    """Lineage that describes the union of field projections in a query result"""

    type: Literal["union"] = "union"
    inputs: List[ForeachLineage]


# Define a submodel for lineage values
QueryLineage = Annotated[
    Union[UnionLineage, ForeachLineage], Field(discriminator="type")
]


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
        lineage = self.results.metadata[0].lineage
        if isinstance(lineage, UnionLineage):
            # Unions require that all inputs have the same structure, so we only
            # need the projections from the first input
            projections = lineage.inputs[0].projections
        else:
            projections = lineage.projections

        return [p.field for p in projections]

    class Config:
        """Model configuration"""

        alias_generator = to_camel
        keep_untouched = (cached_property,)
