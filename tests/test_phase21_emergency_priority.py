import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.emergency_priority import EmergencyVehiclePrioritySystem

def test_emergency_priority_system():
    print("==================================================")
    print("PHASE 21 EMERGENCY VEHICLE CORRIDOR PRIORITY TEST")
    print("==================================================")
    
    priority_sys = EmergencyVehiclePrioritySystem(override_green_sec=90)
    
    mock_traffic = [
        {"track_id": 1, "class_name": "car"},
        {"track_id": 2, "class_name": "ambulance", "is_emergency": True}
    ]
    
    status = priority_sys.evaluate_emergency_priority(mock_traffic)
    print(f"Emergency Priority Status: {status}")
    
    assert status["emergency_vehicle_detected"], "Expected emergency vehicle to be detected"
    assert status["signal_override_active"], "Expected green signal override to be active"
    assert status["preemption_green_duration_sec"] == 90, "Expected 90s preemption duration"
    
    print("\n==================================================")
    print("PHASE 21 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_emergency_priority_system()
