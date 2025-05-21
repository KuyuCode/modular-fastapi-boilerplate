from .. import util
from typing import Annotated
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict, PlainSerializer, Field


datetime_pd = Annotated[
    datetime,
    PlainSerializer(
        lambda x: x and int(util.datetime.utc_timestamp(x)),
        return_type=int,
    ),
]

timedelta_pd = Annotated[
    timedelta,
    PlainSerializer(
        lambda x: int(x.total_seconds()),
        return_type=int,
    ),
]


class Schema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        validate_default=True,
    )


class Object(Schema):
    id: int

    created: datetime_pd = Field(
        description="Date when object was created", validation_alias="created_at"
    )
    updated: datetime_pd | None = Field(
        None, description="Date when object was last updated", validation_alias="updated_at"
    )
