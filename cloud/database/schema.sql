-- Smart City Traffic & Accident Platform Database Schema

CREATE TABLE IF NOT EXISTS cameras (
    camera_id VARCHAR(50) PRIMARY KEY,
    location_name VARCHAR(150) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    rtsp_url VARCHAR(255),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accidents (
    accident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id VARCHAR(50) REFERENCES cameras(camera_id),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    confidence_score DECIMAL(4, 3) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    s3_snapshot_key VARCHAR(255),
    s3_video_clip_key VARCHAR(255),
    status VARCHAR(30) DEFAULT 'UNRESOLVED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    accident_id UUID REFERENCES accidents(accident_id),
    alert_type VARCHAR(30) NOT NULL,
    recipient VARCHAR(100) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_status VARCHAR(20) DEFAULT 'SENT'
);

-- Seed Default Cameras
INSERT INTO cameras (camera_id, location_name, latitude, longitude, status)
VALUES 
    ('CAM-NORTH-001', 'North Junction & 5th Ave', 40.712776, -74.005974, 'ACTIVE'),
    ('CAM-SOUTH-002', 'South Expressway Exit 12', 40.705000, -74.011000, 'ACTIVE')
ON CONFLICT (camera_id) DO NOTHING;
