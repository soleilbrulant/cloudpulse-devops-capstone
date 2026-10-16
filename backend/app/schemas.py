from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AssetBase(BaseModel):
    name: str
    asset_type: str
    provider: str = "AWS"
    region: str = "ap-south-1"
    status: str = "RUNNING"
    cost_monthly: float = 0.0
    owner_team: str = "Platform Engineering"
    ip_address: str = "10.0.1.100"

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[str] = None
    provider: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    cost_monthly: Optional[float] = None
    owner_team: Optional[str] = None
    ip_address: Optional[str] = None

class AssetOut(AssetBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StatsOut(BaseModel):
    total_assets: int
    running: int
    maintenance: int
    stopped: int
    total_monthly_spend: float
    aws_count: int
    gcp_count: int
    azure_count: int
