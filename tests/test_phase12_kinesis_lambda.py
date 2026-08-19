import os
import sys
import json
import base64
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.lambdas.event_processor.lambda_function import lambda_handler

def test_kinesis_lambda_pipeline():
    print("==================================================")
    print("PHASE 12 AWS KINESIS + LAMBDA PIPELINE TEST")
    print("==================================================")
    
    # Construct mock Kinesis records batch
    telemetry_payload = {
        "event_type": "TELEMETRY",
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "metrics": {"vehicle_count": 22, "density": "HIGH", "congestion_level": "HIGH"}
    }
    
    accident_payload = {
        "event_type": "ACCIDENT_ALERT",
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "severity": "CRITICAL",
        "accident_probability": 0.96
    }
    
    encoded_telemetry = base64.b64encode(json.dumps(telemetry_payload).encode("utf-8")).decode("utf-8")
    encoded_accident = base64.b64encode(json.dumps(accident_payload).encode("utf-8")).decode("utf-8")
    
    mock_kinesis_event = {
        "Records": [
            {"kinesis": {"data": encoded_telemetry}},
            {"kinesis": {"data": encoded_accident}}
        ]
    }
    
    res = lambda_handler(mock_kinesis_event, None)
    print(f"Lambda Handler Execution Result: {res}")
    
    assert res["statusCode"] == 200
    body = json.loads(res["body"])
    assert body["records_processed"] == 2
    assert body["telemetry_count"] == 1
    assert body["accident_count"] == 1
    
    print("\n==================================================")
    print("PHASE 12 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_kinesis_lambda_pipeline()
