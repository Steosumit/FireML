# Code for defining the standard request and response models

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, AnyHttpUrl

class PredictRequestModel(BaseModel):
    url: AnyHttpUrl = Field(..., alias='check_url', description='URL to evaluate')
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PredictResponseModel(BaseModel):
    decision: Literal['safe', 'suspicious']
    url: AnyHttpUrl
    source: Literal['model', 'cache', 'rule'] = 'model'
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LogEventModel(BaseModel):
    url: AnyHttpUrl
    decision: Literal['safe', 'suspicious']
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = None
