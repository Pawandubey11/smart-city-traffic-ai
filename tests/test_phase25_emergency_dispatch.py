import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.multi_agency_dispatch import MultiAgencyEmergencyDispatchSystem

def test_emergency_dispatch():
    print("==================================================")
    print("PHASE 25 MULTI-AGENCY EMERGENCY DISPATCH TEST")
    print("==================================================")
    
    system = MultiAgencyEmergencyDispatchSystem()
    
    res = system.dispatch_emergency_alert(
        camera_id="CAM-EAST-003",
        location_name="Noida-Greater Noida Expressway Toll",
        lat=28.4850,
        lng=77.4750,
        vehicle_plate="UP16-CV-9842",
        vehicle_class="Car",
        confidence=0.945
    )
    
    print(f"Incident ID: {res['incident_id']}")
    print(f"Location: {res['location_name']} ({res['gps_coordinates']['lat']} N, {res['gps_coordinates']['lng']} E)")
    print(f"Google Maps Link: {res['google_maps_url']}")
    print(f"Involved Vehicle: {res['vehicle_details']['vehicle_class']} [{res['vehicle_details']['license_plate']}]")
    print(f"SNS Broadcast Status: {res['sns_broadcast_status']}\n")
    
    print("Agency Dispatches:")
    for d in res["agency_dispatches"]:
        print(f"   - {d['agency_name']}: {d['status']} (ETA: {d['estimated_eta_minutes']} mins)")
        
    assert res["sns_broadcast_status"] == "SUCCESS", "Expected SNS Broadcast Status SUCCESS"
    assert len(res["agency_dispatches"]) == 3, "Expected 3 agency dispatches"
    assert "google.com/maps" in res["google_maps_url"], "Expected Google Maps URL"
    
    print("\n==================================================")
    print("PHASE 25 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_emergency_dispatch()
