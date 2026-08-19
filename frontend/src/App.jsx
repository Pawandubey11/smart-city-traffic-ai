import React, { useState, useEffect } from 'react';
import './App.css';

export default function App() {
  const [metrics, setMetrics] = useState({
    activeCameras: 3,
    totalVehicles: 85,
    cityCongestion: 'HIGH',
    congestionIndex: 78.4,
    recommendedGreenSec: 45,
    activeAccidents: 1
  });

  const [cameras, setCameras] = useState([
    {
      id: 'CAM-NORTH-001',
      name: 'North Junction & 5th Ave',
      count: 28,
      speed: 8.5,
      density: 'HIGH',
      congestion: 'HIGH',
      congestionIndex: 72.0,
      recommendedGreenSec: 45,
      minTtcSec: 4.2,
      status: 'ACTIVE'
    },
    {
      id: 'CAM-SOUTH-002',
      name: 'South Expressway Exit 12',
      count: 12,
      speed: 32.0,
      density: 'MEDIUM',
      congestion: 'LOW',
      congestionIndex: 18.5,
      recommendedGreenSec: 20,
      minTtcSec: 12.8,
      status: 'ACTIVE'
    },
    {
      id: 'CAM-EAST-003',
      name: 'East Bridge Toll Plaza',
      count: 45,
      speed: 3.2,
      density: 'HIGH',
      congestion: 'SEVERE',
      congestionIndex: 91.2,
      recommendedGreenSec: 60,
      minTtcSec: 0.8,
      status: 'ACTIVE'
    }
  ]);

  const [accidents, setAccidents] = useState([
    {
      id: 'ACC-9842',
      cameraId: 'CAM-EAST-003',
      location: 'East Bridge Toll Plaza',
      time: '10:43:12 UTC',
      confidence: 0.945,
      severity: 'CRITICAL',
      snapshotUrl: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600'
    }
  ]);

  return (
    <div className="dashboard-container">
      {/* Header Navbar */}
      <header className="navbar glass-panel">
        <div className="brand-title">
          <span>🚦</span> SMART CITY TRAFFIC & ACCIDENT AI CONTROL ROOM
        </div>
        <div className="status-badge">
          <span className="pulse-dot"></span> AWS Greengrass Edge Compute Engine Active
        </div>
      </header>

      {/* Emergency Accident Alert Banner */}
      {accidents.length > 0 && (
        <div className="alert-banner">
          <div>
            <h3 style={{ color: '#fff', fontSize: '1.1rem', marginBottom: '0.25rem' }}>
              🚨 CRITICAL ACCIDENT DETECTED — {accidents[0].location} [{accidents[0].cameraId}]
            </h3>
            <p style={{ color: '#fca5a5', fontSize: '0.875rem' }}>
              AI Spatial-Temporal Confidence: {(accidents[0].confidence * 100).toFixed(1)}% | Time-To-Collision: 0.8s | Severity: {accidents[0].severity}
            </p>
          </div>
          <button 
            style={{
              background: '#ef4444',
              color: '#fff',
              border: 'none',
              padding: '0.6rem 1.2rem',
              borderRadius: '8px',
              fontWeight: '700',
              cursor: 'pointer'
            }}
            onClick={() => alert(`View S3 Evidence Snapshot URL: ${accidents[0].snapshotUrl}`)}
          >
            Inspect S3 Evidence
          </button>
        </div>
      )}

      {/* Real-Time Metrics Overview Grid */}
      <div className="metrics-grid">
        <div className="glass-panel metric-card">
          <span className="metric-label">Monitored Junctions</span>
          <span className="metric-value" style={{ color: '#38bdf8' }}>{metrics.activeCameras}</span>
        </div>
        <div className="glass-panel metric-card">
          <span className="metric-label">Tracked Vehicles</span>
          <span className="metric-value" style={{ color: '#818cf8' }}>{metrics.totalVehicles}</span>
        </div>
        <div className="glass-panel metric-card">
          <span className="metric-label">Congestion Index</span>
          <span className="metric-value" style={{ color: '#f59e0b' }}>{metrics.congestionIndex}/100</span>
        </div>
        <div className="glass-panel metric-card">
          <span className="metric-label">Active Accidents</span>
          <span className="metric-value" style={{ color: '#ef4444' }}>{metrics.activeAccidents}</span>
        </div>
      </div>

      {/* Live Camera Grid Section */}
      <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontFamily: 'Outfit, sans-serif' }}>
        🎥 Live Edge Video Feeds & Adaptive Signal Timing
      </h2>
      <div className="camera-grid">
        {cameras.map((cam) => (
          <div key={cam.id} className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: '700', fontSize: '1rem' }}>{cam.name}</span>
              <span className={`badge badge-${cam.congestion.toLowerCase()}`}>{cam.congestion} ({cam.congestionIndex})</span>
            </div>
            
            <div className="video-frame-placeholder">
              <div style={{ position: 'absolute', top: '10px', left: '10px', background: 'rgba(0,0,0,0.6)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>
                REC • 30 FPS | YOLOv8 + ByteTrack + CNN-LSTM
              </div>
              <div style={{ textAlign: 'center', color: '#94a3b8' }}>
                <span style={{ fontSize: '2.5rem', display: 'block' }}>📹</span>
                Live RTSP Stream [{cam.id}]
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.85rem' }}>
              <div><span style={{ color: '#94a3b8' }}>Vehicles:</span> <strong>{cam.count}</strong></div>
              <div><span style={{ color: '#94a3b8' }}>Avg Speed:</span> <strong>{cam.speed} px/f</strong></div>
              <div><span style={{ color: '#94a3b8' }}>Min TTC:</span> <strong style={{ color: cam.minTtcSec < 2.0 ? '#ef4444' : '#10b981' }}>{cam.minTtcSec}s</strong></div>
              <div><span style={{ color: '#94a3b8' }}>Rec. Green Light:</span> <strong style={{ color: '#38bdf8' }}>{cam.recommendedGreenSec}s</strong></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
