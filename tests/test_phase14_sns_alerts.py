import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.sns_alert_dispatcher import SNSAlertDispatcher

def test_sns_alerting():
    print("==================================================")
    print("PHASE 14 AMAZON SNS ACCIDENT ALERT DISPATCH TEST")
    print("==================================================")
    
    dispatcher = SNSAlertDispatcher()
    
    presigned_url = "https://smart-city-traffic-evidence-demo.s3.amazonaws.com/accidents/CAM-NORTH-001/snapshot.jpg?token=abc"
    alert_ok = dispatcher.dispatch_accident_alert(
        camera_id="CAM-NORTH-001",
        location_name="North Junction & 5th Ave",
        confidence_score=0.955,
        presigned_s3_url=presigned_url,
        severity="CRITICAL"
    )
    
    print(f"SNS Accident Notification Dispatch Status: {'SUCCESS' if alert_ok else 'FAILED'}")
    assert alert_ok, "SNS alert dispatch failed"
    
    print("\n==================================================")
    print("PHASE 14 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_sns_alerting()
