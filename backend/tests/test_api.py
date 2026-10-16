import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "CloudPulse" in data["service"]
    assert data["status"] == "OPERATIONAL"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP", "health": "HEALTHY"}

def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "READY"
    assert response.json()["database"] == "CONNECTED"

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "# HELP" in response.text

def test_create_asset():
    payload = {
        "name": "prod-eks-cluster-core",
        "asset_type": "KUBERNETES_CLUSTER",
        "provider": "AWS",
        "region": "ap-south-1",
        "status": "RUNNING",
        "cost_monthly": 145.50,
        "owner_team": "DevOps Core",
        "ip_address": "10.0.10.15"
    }
    response = client.post("/api/assets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "prod-eks-cluster-core"
    assert data["asset_type"] == "KUBERNETES_CLUSTER"
    assert data["cost_monthly"] == 145.50
    assert "id" in data

def test_list_assets():
    response = client.get("/api/assets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_filter_assets_by_provider():
    # Add a GCP asset
    client.post("/api/assets", json={
        "name": "gcp-bigquery-warehouse",
        "asset_type": "DATABASE",
        "provider": "GCP",
        "cost_monthly": 210.00
    })
    response = client.get("/api/assets?provider=GCP")
    assert response.status_code == 200
    items = response.json()
    assert any(x["provider"] == "GCP" for x in items)

def test_get_asset_by_id():
    create_res = client.post("/api/assets", json={
        "name": "azure-blob-backup",
        "asset_type": "STORAGE",
        "provider": "AZURE",
        "cost_monthly": 42.00
    })
    asset_id = create_res.json()["id"]

    response = client.get(f"/api/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json()["id"] == asset_id
    assert response.json()["name"] == "azure-blob-backup"

def test_update_asset():
    create_res = client.post("/api/assets", json={
        "name": "temp-redis-node",
        "asset_type": "CACHE",
        "provider": "AWS",
        "status": "RUNNING"
    })
    asset_id = create_res.json()["id"]

    update_payload = {"status": "MAINTENANCE", "cost_monthly": 65.00}
    response = client.put(f"/api/assets/{asset_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "MAINTENANCE"
    assert response.json()["cost_monthly"] == 65.00

def test_stats_aggregation():
    response = client.get("/api/assets/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_assets"] >= 3
    assert stats["total_monthly_spend"] > 0
    assert stats["aws_count"] >= 1

def test_get_asset_not_found():
    response = client.get("/api/assets/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"

def test_delete_asset():
    create_res = client.post("/api/assets", json={
        "name": "obsolete-instance",
        "asset_type": "COMPUTE_VM",
        "provider": "AWS"
    })
    asset_id = create_res.json()["id"]

    del_res = client.delete(f"/api/assets/{asset_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/assets/{asset_id}")
    assert get_res.status_code == 404
