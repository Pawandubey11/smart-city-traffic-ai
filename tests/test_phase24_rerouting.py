import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.rerouting_engine import AutomatedIncidentReroutingEngine

def test_rerouting_engine():
    print("==================================================")
    print("PHASE 24 AUTOMATED INCIDENT REROUTING & VMS TEST")
    print("==================================================")
    
    engine = AutomatedIncidentReroutingEngine()
    
    # Test Normal Traffic Flow
    res_normal = engine.evaluate_rerouting_strategy("CAM-NORTH-001", congestion_index=45.0, accident_detected=False)
    print(f"Normal Flow Strategy: {res_normal['action_status']} | VMS: {res_normal['vms_billboard']['active_message']}")
    assert res_normal["reroute_required"] == False, "Expected no rerouting required"
    
    # Test Critical Accident Rerouting Strategy
    res_accident = engine.evaluate_rerouting_strategy("CAM-EAST-003", congestion_index=91.2, accident_detected=True)
    print(f"\nIncident Rerouting Strategy: {res_accident['action_status']}")
    print(f"   - Corridor: {res_accident['corridor_name']}")
    print(f"   - Detour Route: {res_accident['detour_strategy']}")
    print(f"   - Estimated Time Saved: {res_accident['estimated_time_saved_minutes']} mins")
    print(f"   - VMS Digital Billboard Message: {res_accident['vms_billboard']['active_message']}")
    
    assert res_accident["reroute_required"] == True, "Expected rerouting required for accident"
    assert "Knowledge Park II" in res_accident["detour_strategy"], "Expected Greater Noida detour route"
    
    print("\n==================================================")
    print("PHASE 24 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_rerouting_engine()
