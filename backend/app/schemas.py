from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


Timeframe = Literal["daily", "weekly", "monthly"]


class SummaryRequest(BaseModel):
    user_id: str = Field(default="demo-user")
    topics: List[str] = Field(default_factory=list)
    timeframe: Timeframe = "daily"
    region: str = "global"


class PreferencesRequest(BaseModel):
    user_id: str = Field(default="demo-user")
    topics: List[str] = Field(default_factory=list)
    region: str = "global"
    default_timeframe: Timeframe = "daily"


class SaveUsageRequest(BaseModel):
    user_id: str = Field(default="demo-user")
    topic: str
    timeframe: Timeframe = "daily"
    region: str = "global"
