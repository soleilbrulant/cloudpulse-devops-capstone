import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API_BASE = '/api';

function App() {
  const [assets, setAssets] = useState([]);
  const [stats, setStats] = useState({
    total_assets: 0,
    running: 0,
    maintenance: 0,
    stopped: 0,
    total_monthly_spend: 0,
    aws_count: 0,
    gcp_count: 0,
    azure_count: 0,
  });
  const [providerFilter, setProviderFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState('');

  const fetchAssets = async () => {
    try {
      setApiError('');
      const [resAssets, resStats] = await Promise.all([
        fetch(`${API_BASE}/assets`),
        fetch(`${API_BASE}/assets/stats`)
      ]);

      if (!resAssets.ok || !resStats.ok) {
        throw new Error('API server returned error status');
      }

      const assetsData = await resAssets.json();
      const statsData = await resStats.json();
      setAssets(assetsData);
      setStats(statsData);
    } catch (err) {
      setApiError(err.message || 'Failed to connect to CloudPulse API');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  const handleCreateAsset = async (e) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const payload = {
      name: form.get('name'),
      asset_type: form.get('asset_type'),
      provider: form.get('provider'),
      region: form.get('region'),
      status: form.get('status'),
      cost_monthly: parseFloat(form.get('cost_monthly')) || 0.0,
      owner_team: form.get('owner_team'),
      ip_address: form.get('ip_address') || '10.0.1.50',
    };

    try {
      const res = await fetch(`${API_BASE}/assets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Failed to register asset');
      setShowModal(false);
      fetchAssets();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleAdvanceStatus = async (asset) => {
    const nextStatus =
      asset.status === 'RUNNING'
        ? 'MAINTENANCE'
        : asset.status === 'MAINTENANCE'
        ? 'STOPPED'
        : 'RUNNING';

    try {
      await fetch(`${API_BASE}/assets/${asset.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      });
      fetchAssets();
    } catch (err) {
      alert(`Failed to update asset: ${err.message}`);
    }
  };

  const handleDeleteAsset = async (id) => {
    if (!window.confirm('Are you sure you want to deprovision this asset?')) return;
    try {
      const res = await fetch(`${API_BASE}/assets/${id}`, { method: 'DELETE' });
      if (res.status === 204) fetchAssets();
    } catch (err) {
      alert(`Failed to delete asset: ${err.message}`);
    }
  };

  const filteredAssets = assets.filter((asset) => {
    const matchesProvider =
      providerFilter === 'ALL' || asset.provider === providerFilter;
    const matchesSearch =
      asset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      asset.owner_team.toLowerCase().includes(searchQuery.toLowerCase()) ||
      asset.ip_address.includes(searchQuery);
    return matchesProvider && matchesSearch;
  });

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div>
          <div className="brand">
            <div className="brand-icon">⚡</div>
            <div>
              <h2>CloudPulse</h2>
              <small>DevOps Asset Suite</small>
            </div>
          </div>
          <nav className="nav">
            <div className="nav-item active">⊞ Infrastructure</div>
            <div className="nav-item">☸ Kubernetes Clusters</div>
            <div className="nav-item">🗄 Cloud Databases</div>
            <div className="nav-item">📦 Storage Buckets</div>
            <div className="nav-item">🛡 Security & Compliance</div>
          </nav>
        </div>

        <div className="sidebar-footer">
          <div style={{ fontSize: '13px', fontWeight: '700' }}>Production EKS Cluster</div>
          <div className="infra-status">
            <span className="pulse-dot"></span>
            <span>Cluster Healthy (ap-south-1)</span>
          </div>
        </div>
      </aside>

      {/* Main View Area */}
      <main className="main">
        <header className="header">
          <div className="header-title">
            <h1>Infrastructure & Cloud Asset Inventory</h1>
            <p>Unified multi-cloud telemetry, configuration management, and lifecycle tracking</p>
          </div>
          <button className="btn-primary" onClick={() => setShowModal(true)}>
            ＋ Register Asset
          </button>
        </header>

        {apiError && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#f87171',
            padding: '12px 18px',
            borderRadius: '10px',
            marginBottom: '20px',
            fontSize: '14px'
          }}>
            ⚠ {apiError} (Ensure PostgreSQL and Backend containers are running).
          </div>
        )}

        {/* KPI Summary Cards */}
        <div className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-header">
              <span>Total Assets</span>
              <span>⚡</span>
            </div>
            <div className="kpi-value">{stats.total_assets}</div>
            <div className="kpi-sub">Across AWS, GCP & Azure</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Active Instances</span>
              <span>🟢</span>
            </div>
            <div className="kpi-value" style={{ color: 'var(--success)' }}>
              {stats.running}
            </div>
            <div className="kpi-sub">{stats.maintenance} in maintenance</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Monthly Cloud Spend</span>
              <span>💵</span>
            </div>
            <div className="kpi-value" style={{ color: 'var(--cyan)' }}>
              ${stats.total_monthly_spend.toLocaleString()}
            </div>
            <div className="kpi-sub">Estimated monthly total</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Platform Health</span>
              <span>🛡</span>
            </div>
            <div className="kpi-value" style={{ color: 'var(--primary)' }}>
              99.98%
            </div>
            <div className="kpi-sub">SLA Uptime target achieved</div>
          </div>
        </div>

        {/* Assets Main Panel */}
        <div className="panel">
          <div className="filter-bar">
            <div className="tabs">
              {['ALL', 'AWS', 'GCP', 'AZURE'].map((provider) => (
                <button
                  key={provider}
                  className={`tab-btn ${providerFilter === provider ? 'active' : ''}`}
                  onClick={() => setProviderFilter(provider)}
                >
                  {provider}
                </button>
              ))}
            </div>

            <div className="search-box">
              <span>🔍</span>
              <input
                type="text"
                placeholder="Search asset, team, or IP..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Asset & Resource</th>
                  <th>Type</th>
                  <th>Cloud & Region</th>
                  <th>IP Address</th>
                  <th>Owner Team</th>
                  <th>Monthly Spend</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan="8" style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)' }}>
                      Loading assets from CloudPulse API...
                    </td>
                  </tr>
                ) : filteredAssets.length === 0 ? (
                  <tr>
                    <td colSpan="8" style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)' }}>
                      No assets found matching current criteria.
                    </td>
                  </tr>
                ) : (
                  filteredAssets.map((asset) => (
                    <tr key={asset.id}>
                      <td>
                        <div className="asset-info">
                          <b>{asset.name}</b>
                          <small>ID: #{asset.id}</small>
                        </div>
                      </td>
                      <td>
                        <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-muted)' }}>
                          {asset.asset_type}
                        </span>
                      </td>
                      <td>
                        <span className={`badge badge-${asset.provider.toLowerCase()}`}>
                          {asset.provider} • {asset.region}
                        </span>
                      </td>
                      <td>
                        <span className="code-ip">{asset.ip_address}</span>
                      </td>
                      <td>{asset.owner_team}</td>
                      <td>
                        <b>${asset.cost_monthly.toFixed(2)}</b>
                      </td>
                      <td>
                        <span className={`badge status-${asset.status.toLowerCase()}`}>
                          {asset.status}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <button
                            className="btn-icon"
                            onClick={() => handleAdvanceStatus(asset)}
                            title="Cycle lifecycle status"
                          >
                            ↻ Status
                          </button>
                          <button
                            className="btn-icon btn-delete"
                            onClick={() => handleDeleteAsset(asset.id)}
                            title="Deprovision asset"
                          >
                            ✕
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal for creating a new asset */}
        {showModal && (
          <div className="modal-overlay">
            <div className="modal-content">
              <div className="modal-header">
                <h3>Register Infrastructure Asset</h3>
                <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
              </div>
              <form onSubmit={handleCreateAsset}>
                <div className="form-group">
                  <label>Asset Name</label>
                  <input
                    name="name"
                    required
                    placeholder="e.g. prod-redis-cluster-01"
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Resource Type</label>
                    <select name="asset_type">
                      <option value="KUBERNETES_CLUSTER">Kubernetes Cluster</option>
                      <option value="COMPUTE_VM">Compute Instance / EC2</option>
                      <option value="RDS_DATABASE">Managed Database / RDS</option>
                      <option value="OBJECT_STORAGE">Object Storage / S3</option>
                      <option value="CACHE_REDIS">Cache / Redis</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Cloud Provider</label>
                    <select name="provider">
                      <option value="AWS">AWS</option>
                      <option value="GCP">GCP</option>
                      <option value="AZURE">Azure</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Region</label>
                    <input name="region" defaultValue="ap-south-1" />
                  </div>
                  <div className="form-group">
                    <label>Initial Status</label>
                    <select name="status">
                      <option value="RUNNING">RUNNING</option>
                      <option value="MAINTENANCE">MAINTENANCE</option>
                      <option value="STOPPED">STOPPED</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Monthly Spend ($)</label>
                    <input
                      name="cost_monthly"
                      type="number"
                      step="0.01"
                      defaultValue="85.00"
                    />
                  </div>
                  <div className="form-group">
                    <label>IP Address</label>
                    <input name="ip_address" defaultValue="10.0.1.120" />
                  </div>
                </div>

                <div className="form-group">
                  <label>Owner Team</label>
                  <input name="owner_team" defaultValue="Platform Engineering" />
                </div>

                <div className="modal-actions">
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => setShowModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Confirm & Provision
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

const root = createRoot(document.getElementById('root'));
root.render(<App />);
