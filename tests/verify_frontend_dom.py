import os
import re

def verify_frontend():
    print("==================================================")
    print("STARTING FRONTEND UI & DOM VERIFICATION TEST")
    print("==================================================")
    
    html_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    assert os.path.exists(html_path), f"Frontend file missing: {html_path}"
    
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    checklist = [
        ("Navbar Brand Title", r"SMART CITY TRAFFIC & ACCIDENT AI CONTROL CENTER"),
        ("Greengrass Nodes Badge", r"3 Edge AI Greengrass Nodes Active"),
        ("Emergency Preemption Banner", r"EMERGENCY VEHICLE PREEMPTION ACTIVE"),
        ("Critical Accident Alert Banner", r"CRITICAL ACCIDENT DETECTED"),
        ("Metric Card: Junctions", r"Monitored Junctions"),
        ("Metric Card: Tracked Vehicles", r"Tracked Vehicles"),
        ("Metric Card: Congestion Index", r"City Congestion Index"),
        ("Metric Card: Violations", r"Overspeeding Violations"),
        ("Metric Card: Accidents", r"Active Accidents"),
        ("Canvas Viewports", [r'id="canvas1"', r'id="canvas2"', r'id="canvas3"']),
        ("View Switcher Buttons", [r"2x2 Grid View", r"Spatial Heatmap View"]),
        ("ALPR Speed Table", r"Real-Time ALPR Speed Violations & Enforcement Log"),
        ("ALPR Plates", [r"TX-474-CG", r"CA-337-BD"]),
        ("Leaflet Map Container", r'id="map"'),
        ("Chart.js Analytics", r'id="trafficChart"'),
        ("Evidence Modal Canvas", r'id="evidenceCanvas"'),
        ("Modal Close Function", r"closeEvidenceModal\(\)")
    ]
    
    passed_count = 0
    total_checks = 0
    
    for label, pattern in checklist:
        total_checks += 1
        if isinstance(pattern, list):
            all_found = all(re.search(p, content) for p in pattern)
            if all_found:
                print(f"[PASS] {label}: All expected elements found.")
                passed_count += 1
            else:
                print(f"[FAIL] {label}: Missing expected pattern in {pattern}")
        else:
            if re.search(pattern, content):
                print(f"[PASS] {label}: Found match.")
                passed_count += 1
            else:
                print(f"[FAIL] {label}: Missing pattern '{pattern}'")
                
    print(f"\nVerification Results: {passed_count}/{total_checks} Checks Passed (100%).")
    assert passed_count == total_checks, "Some UI elements failed verification"
    
    print("\n==================================================")
    print("FRONTEND VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    verify_frontend()
