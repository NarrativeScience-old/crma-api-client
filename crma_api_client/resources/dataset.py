"""Contains definitions for the dataset resource"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, TypeVar

from pydantic import BaseModel, validator

from .user import User
from .util import to_camel

T = TypeVar("T")


class CRMAModel(BaseModel):
    """Base class for all models from the CRMA API

    Has logic for converting camel case to snake case
    """

    class Config:
        """Model configuration"""

        alias_generator = to_camel


class Dataset(CRMAModel):
    """Dataset model"""

    id: str
    url: str


class DateType(Enum):
    """The type of date field"""

    date = "Date"
    date_only = "DateOnly"
    date_time = "DateTime"


class XmdDateFields(CRMAModel):
    """Date fields in the extended metadata format

    See https://developer.salesforce.com/docs/atlas.en-us.230.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_xmd_main.htm#XmdDateFieldRepresentation
    """

    day: str
    epoch_day: str
    epoch_second: str
    fiscal_month: Optional[str]
    fiscal_quarter: Optional[str]
    fiscal_week: Optional[str]
    fiscal_year: Optional[str]
    full_field: str
    hour: str
    minute: str
    month: str
    quarter: str
    second: str
    week: str
    year: str

    @validator("fiscal_month", "fiscal_quarter", "fiscal_week", "fiscal_year")
    def not_none(cls, v: T) -> T:
        """Validates that the given value is not None

        This is needed since the Optional type doesn't distinguish between a field
        being None and being missing.

        Args:
            v: the value to check

        Raises:
            ValueError: if the value is None

        Returns:
            the value if it's not None

        """
        if v is None:
            raise ValueError("Fiscal fields may not be None")
        return v


class XmdDate(CRMAModel):
    """Date in the extended metadata format

    See https://developer.salesforce.com/docs/atlas.en-us.230.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_xmd_main.htm#XmdDateRepresentation
    """

    alias: str
    fields: XmdDateFields
    first_day_of_week: int
    fiscal_month_offset: int
    fully_qualified_name: str
    is_year_end_fiscal_year: bool
    label: str
    type: DateType


class XmdDimension(CRMAModel):
    """Dimension in the Xmd format

    See https://developer.salesforce.com/docs/atlas.en-us.230.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_xmd_main.htm#XmdDimensionRepresentation
    """

    field: str
    label: str


class XmdMeasure(CRMAModel):
    """Measure in the Xmd format

    See https://developer.salesforce.com/docs/atlas.en-us.230.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_xmd_main.htm#XmdMeasureRepresentation
    """

    field: str
    label: str


class DatasetXmd(CRMAModel):
    """Extended metadata for a dataset

    See https://developer.salesforce.com/docs/atlas.en-us.230.0.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_resources_xmd_main.htm
    """

    created_by: User
    created_date: datetime
    dates: List[XmdDate]
    derived_dimensions: List[XmdDimension]
    derived_measures: List[XmdMeasure]
    dimensions: List[XmdDimension]
    last_modified_by: User
    last_modified_date: datetime
    measures: List[XmdMeasure]
    type: str
    url: str


class DatasetVersion(CRMAModel):
    """Dataset version model

    See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_responses_dataset_version.htm
    """

    created_by: User
    created_date: datetime
    dataset: Dataset
    id: str
    last_modified_by: User
    last_modified_date: datetime
    total_row_count: int
    type: str
    url: str


class DatasetVersionResponse(DatasetVersion):
    """Dataset version model

    See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_responses_dataset_version.htm
    """

    xmd_main: DatasetXmd


class DatasetVersionsResponse(CRMAModel):
    """Response model for a list of dataset versions

    See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_responses_dataset_version_collection.htm
    """

    url: str
    versions: List[DatasetVersion]
