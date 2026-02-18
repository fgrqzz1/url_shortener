from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


class LinkBase(BaseModel):
    long_url: HttpUrl = Field(..., description='Исходный URL')
    description: Optional[str] = Field(None, max_length=500, description="Описание ссылки")


class LinkCreate(LinkBase):
    pass


class LinkRead(LinkBase):
    id: int
    short_code: str
    is_active: bool
    click_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        'from_attributes': True,
    }


class LinkStats(BaseModel):
    short_code: str
    long_url: HttpUrl
    click_count: int
    is_active: bool

