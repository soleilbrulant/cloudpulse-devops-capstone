from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .db import Base, engine, get_db
from .models import CloudAsset
from .schemas import AssetCreate, AssetOut, AssetUpdate, StatsOut

app = FastAPI(
    title=settings.app_name,
    description="CloudPulse Infrastructure & Asset Management DevOps Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument Prometheus metrics endpoint at /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "status": "OPERATIONAL",
        "docs": "/docs",
        "metrics": "/metrics"
    }

@app.get("/health", tags=["System"])
def health():
    return {"status": "UP", "health": "HEALTHY"}

@app.get("/ready", tags=["System"])
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(select(func.count(CloudAsset.id)))
        return {"status": "READY", "database": "CONNECTED"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(exc)}"
        )

@app.get("/api/assets", response_model=list[AssetOut], tags=["Assets"])
def list_assets(
    provider: Optional[str] = Query(None, description="Filter by cloud provider"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name or owner"),
    db: Session = Depends(get_db)
):
    stmt = select(CloudAsset)
    if provider and provider != "ALL":
        stmt = stmt.where(CloudAsset.provider == provider)
    if status and status != "ALL":
        stmt = stmt.where(CloudAsset.status == status)
    if search:
        stmt = stmt.where(CloudAsset.name.ilike(f"%{search}%") | CloudAsset.owner_team.ilike(f"%{search}%"))
    stmt = stmt.order_by(CloudAsset.id.desc())
    return list(db.scalars(stmt))

@app.get("/api/assets/stats", response_model=StatsOut, tags=["Assets"])
def get_stats(db: Session = Depends(get_db)):
    assets = list(db.scalars(select(CloudAsset)))
    total = len(assets)
    running = sum(1 for a in assets if a.status == "RUNNING")
    maintenance = sum(1 for a in assets if a.status == "MAINTENANCE")
    stopped = sum(1 for a in assets if a.status == "STOPPED")
    total_cost = sum(a.cost_monthly for a in assets)
    aws = sum(1 for a in assets if a.provider == "AWS")
    gcp = sum(1 for a in assets if a.provider == "GCP")
    azure = sum(1 for a in assets if a.provider == "AZURE")

    return StatsOut(
        total_assets=total,
        running=running,
        maintenance=maintenance,
        stopped=stopped,
        total_monthly_spend=round(total_cost, 2),
        aws_count=aws,
        gcp_count=gcp,
        azure_count=azure,
    )

@app.get("/api/assets/{asset_id}", response_model=AssetOut, tags=["Assets"])
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.get(CloudAsset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@app.post("/api/assets", response_model=AssetOut, status_code=status.HTTP_201_CREATED, tags=["Assets"])
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = CloudAsset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@app.put("/api/assets/{asset_id}", response_model=AssetOut, tags=["Assets"])
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    asset = db.get(CloudAsset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, val in payload.model_dump(exclude_unset=True).items():
        setattr(asset, key, val)
    db.commit()
    db.refresh(asset)
    return asset

@app.delete("/api/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Assets"])
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.get(CloudAsset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
