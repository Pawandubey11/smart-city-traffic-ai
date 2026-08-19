import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.health_monitor import EdgeHealthMonitor

def test_edge_health():
    print("==================================================")
    print("PHASE 23 EDGE DEVICE HEALTH & DIAGNOSTICS TEST")
    print("==================================================")
    
    monitor = EdgeHealthMonitor(camera_id="TEST-CAM-DIAG")
    diagnostics = monitor.get_system_diagnostics()
    
    print(f"Diagnostics Collected: {diagnostics}")
    
    assert diagnostics["camera_id"] == "TEST-CAM-DIAG", "Expected camera_id to match"
    assert diagnostics["status"] in ["HEALTHY", "WARNING", "CRITICAL"], "Expected valid status"
    assert "cpu_utilization_pct" in diagnostics["hardware"], "Expected CPU metrics"
    
    print("\n==================================================")
    print("PHASE 23 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_edge_health()
