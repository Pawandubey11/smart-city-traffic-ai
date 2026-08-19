import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.database.db_manager import SmartCityDatabaseManager

def test_database_layer():
    print("==================================================")
    print("PHASE 13 DYNAMODB & RDS POSTGRESQL DATABASE TEST")
    print("==================================================")
    
    db = SmartCityDatabaseManager()
    
    # 1. Test Telemetry Storage (DynamoDB)
    telemetry_payload = {
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "metrics": {"vehicle_count": 34, "average_speed_px": 8.5, "density_level": "HIGH", "congestion_level": "SEVERE"},
        "accident_probability": 0.04
    }
    
    saved_telemetry = db.save_telemetry_event(telemetry_payload)
    print(f"[1] Telemetry Saved Status: {'SUCCESS' if saved_telemetry else 'FAILED'}")
    assert saved_telemetry, "Failed to save telemetry event"

    # 2. Test Accident Storage (RDS PostgreSQL)
    accident_payload = {
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "accident_probability": 0.94,
        "severity": "CRITICAL",
        "snapshot_local_path": "accidents/CAM-NORTH-001/acc_123.jpg"
    }
    
    accident_id = db.save_accident_record(accident_payload)
    print(f"[2] Accident Saved Record ID: {accident_id}")
    assert accident_id is not None, "Failed to save accident record"

    # 3. Test Camera Querying
    cameras = db.get_registered_cameras()
    print(f"[3] Active Cameras Count: {len(cameras)}")
    assert len(cameras) >= 2, "Expected at least 2 active cameras"

    print("\n==================================================")
    print("PHASE 13 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_database_layer()
