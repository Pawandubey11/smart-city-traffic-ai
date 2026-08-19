import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.alpr_speed_detector import ALPRSpeedDetector

def test_alpr_speed_detection():
    print("==================================================")
    print("PHASE 20 ALPR LICENSE PLATE & SPEED ESTIMATION TEST")
    print("==================================================")
    
    alpr = ALPRSpeedDetector(speed_limit_kmh=60.0)
    
    mock_vehicles = [
        {"track_id": 1, "class_name": "car", "bbox": [100, 200, 180, 240], "velocity": (2.0, 0.0)},
        {"track_id": 2, "class_name": "car", "bbox": [300, 200, 380, 240], "velocity": (15.0, 0.0)} # Overspeeding vehicle
    ]
    
    violations = alpr.process_violations(mock_vehicles)
    
    print(f"Tracked Vehicle #1 Speed: {mock_vehicles[0]['speed_kmh']} km/h | License Plate: {mock_vehicles[0]['license_plate']}")
    print(f"Tracked Vehicle #2 Speed: {mock_vehicles[1]['speed_kmh']} km/h | License Plate: {mock_vehicles[1]['license_plate']}")
    print(f"Overspeeding Violations Flagged: {len(violations)}")
    
    assert len(violations) == 1, "Expected 1 overspeeding violation"
    assert violations[0]["speed_kmh"] > 60.0, "Violation speed should exceed limit"
    
    print("\n==================================================")
    print("PHASE 20 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_alpr_speed_detection()
