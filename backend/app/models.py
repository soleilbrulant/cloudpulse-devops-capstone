from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class CloudAsset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(30), default="AWS")
    region: Mapped[str] = mapped_column(String(50), default="ap-south-1")
    status: Mapped[str] = mapped_column(String(30), default="RUNNING")
    cost_monthly: Mapped[float] = mapped_column(Float, default=0.0)
    owner_team: Mapped[str] = mapped_column(String(100), default="Platform Engineering")
    ip_address: Mapped[str] = mapped_column(String(60), default="10.0.1.100")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
