"""Contains definitions for the user resource"""

from pydantic import BaseModel

from .util import to_camel


class User(BaseModel):
    """User model"""

    id: str
    name: str
    profile_photo_url: str

    class Config:
        """Model configuration"""

        alias_generator = to_camel
