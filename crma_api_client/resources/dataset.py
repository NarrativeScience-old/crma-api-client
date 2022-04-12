"""Contains definitions for the dataset resource"""

from datetime import datetime
from typing import List

from pydantic import BaseModel

from .user import User
from .util import to_camel


class Dataset(BaseModel):
    """Dataset model"""

    id: str
    url: str


class DatasetVersion(BaseModel):
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

    class Config:
        """Model configuration"""

        alias_generator = to_camel


class DatasetVersionsResponse(BaseModel):
    """Response model for a list of dataset versions

    See https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/bi_responses_dataset_version_collection.htm
    """

    url: str
    versions: List[DatasetVersion]
