import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.cloudwatch_monitor import CloudWatchMonitor

def test_cloudwatch_monitoring():
    print("==================================================")
    print("PHASE 18 AWS CLOUDWATCH MONITORING & METRICS TEST")
    print("==================================================")
    
    monitor = CloudWatchMonitor()
    
    m1 = monitor.put_metric("EdgeInferenceLatencyMs", 34.5, "Milliseconds", "CAM-NORTH-001")
    m2 = monitor.put_metric("AccidentAlertCount", 1.0, "Count", "CAM-NORTH-001")
    m3 = monitor.put_metric("VehicleThroughputPerMinute", 48.0, "Count", "CAM-NORTH-001")
    
    assert m1 and m2 and m3
    
    print("\n==================================================")
    print("PHASE 18 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_cloudwatch_monitoring()
