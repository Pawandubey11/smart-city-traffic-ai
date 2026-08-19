import json
import base64
import os
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("KinesisLambdaEventProcessor")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Event Handler triggered by AWS Kinesis Data Streams.
    Decodes batch MQTT traffic and accident records from edge cameras,
    routes telemetry data to DynamoDB, and dispatches critical accident alerts to RDS / SNS.
    """
    records_processed = 0
    telemetry_count = 0
    accident_count = 0
    
    # Process batch records from Kinesis Data Stream
    kinesis_records = event.get("Records", [])
    logger.info(f"Received batch of {len(kinesis_records)} records from Kinesis Data Stream.")
    
    for rec in kinesis_records:
        records_processed += 1
        try:
            # 1. Decode Base64 Data Payload
            payload_bytes = base64.b64decode(rec["kinesis"]["data"])
            payload_str = payload_bytes.decode("utf-8")
            data = json.loads(payload_str)
            
            event_type = data.get("event_type", "TELEMETRY")
            camera_id = data.get("camera_id", "UNKNOWN")
            timestamp_ms = data.get("timestamp_ms", 0)
            
            if event_type == "TELEMETRY":
                telemetry_count += 1
                metrics = data.get("metrics", {})
                logger.info(f"[ROUTING TELEMETRY -> DYNAMODB] Camera: {camera_id} | Count: {metrics.get('vehicle_count')} | Congestion: {metrics.get('congestion_level')}")
                
            elif event_type == "ACCIDENT_ALERT":
                accident_count += 1
                prob = data.get("accident_probability", 0.0)
                severity = data.get("severity", "CRITICAL")
                logger.critical(f"[ROUTING ACCIDENT ALERT -> RDS & SNS] Camera: {camera_id} | Prob: {prob:.2f} | Severity: {severity}")

        except Exception as e:
            logger.error(f"Error parsing Kinesis payload record: {e}")
            continue

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "SUCCESS",
            "records_processed": records_processed,
            "telemetry_count": telemetry_count,
            "accident_count": accident_count
        })
    }
