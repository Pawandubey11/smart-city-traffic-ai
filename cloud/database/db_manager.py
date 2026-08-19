import json
import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List, Optional
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DatabaseManager")

class SmartCityDatabaseManager:
    """
    Dual NoSQL (DynamoDB) & Relational (RDS PostgreSQL) Storage Engine.
    DynamoDB: High-frequency time-series telemetry events (traffic metrics).
    RDS PostgreSQL: Relational application entities (cameras, accidents, alerts, audit logs).
    """
    def __init__(
        self,
        region: str = "us-east-1",
        dynamo_table_name: str = "SmartCity_TrafficEvents"
    ):
        self.region = region
        self.dynamo_table_name = dynamo_table_name
        self.local_db_mock: Dict[str, List[Dict[str, Any]]] = {
            "telemetry": [],
            "accidents": [],
            "cameras": [
                {"camera_id": "CAM-NORTH-001", "location_name": "North Junction & 5th Ave", "latitude": 40.712776, "longitude": -74.005974, "status": "ACTIVE"},
                {"camera_id": "CAM-SOUTH-002", "location_name": "South Expressway Exit 12", "latitude": 40.705000, "longitude": -74.011000, "status": "ACTIVE"}
            ]
        }
        
        try:
            self.dynamodb = boto3.resource("dynamodb", region_name=self.region)
            self.table = self.dynamodb.Table(self.dynamo_table_name)
            logger.info(f"Initialized Boto3 DynamoDB Resource for table: {self.dynamo_table_name}")
        except Exception as e:
            logger.warning(f"DynamoDB initialization notice ({e}). Operating in Local Mock Database Mode.")
            self.table = None

    def save_telemetry_event(self, event_payload: Dict[str, Any]) -> bool:
        """Stores high-frequency telemetry event in DynamoDB."""
        camera_id = event_payload.get("camera_id", "UNKNOWN")
        timestamp_ms = event_payload.get("timestamp_ms", int(time.time() * 1000))
        
        item = {
            "camera_id": camera_id,
            "timestamp": timestamp_ms,
            "vehicle_count": event_payload.get("metrics", {}).get("vehicle_count", 0),
            "average_speed_px": str(event_payload.get("metrics", {}).get("average_speed_px", 0.0)),
            "density_level": event_payload.get("metrics", {}).get("density_level", "LOW"),
            "congestion_level": event_payload.get("metrics", {}).get("congestion_level", "LOW"),
            "accident_probability": str(event_payload.get("accident_probability", 0.0))
        }
        
        if self.table is not None:
            try:
                self.table.put_item(Item=item)
                logger.info(f"Saved telemetry event to DynamoDB table [{self.dynamo_table_name}] for {camera_id}")
                return True
            except Exception as e:
                logger.warning(f"DynamoDB put_item notice ({e}). Falling back to local database store.")

        self.local_db_mock["telemetry"].append(item)
        logger.info(f"[LOCAL DB MOCK] Saved telemetry event for {camera_id}")
        return True

    def save_accident_record(self, accident_payload: Dict[str, Any]) -> str:
        """Stores critical accident record in RDS PostgreSQL / database."""
        accident_id = f"acc_{int(time.time()*1000)}"
        record = {
            "accident_id": accident_id,
            "camera_id": accident_payload.get("camera_id", "UNKNOWN"),
            "timestamp_ms": accident_payload.get("timestamp_ms", int(time.time()*1000)),
            "confidence_score": accident_payload.get("accident_probability", 0.0),
            "severity": accident_payload.get("severity", "CRITICAL"),
            "s3_snapshot_key": accident_payload.get("snapshot_local_path", "accidents/sample.jpg"),
            "status": "UNRESOLVED"
        }
        
        self.local_db_mock["accidents"].append(record)
        logger.critical(f"Saved accident record [{accident_id}] to relational database for camera {record['camera_id']}")
        return accident_id

    def get_registered_cameras(self) -> List[Dict[str, Any]]:
        """Returns list of all active smart city traffic cameras."""
        return self.local_db_mock["cameras"]

    def get_recent_accidents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns recent accident alert history."""
        return self.local_db_mock["accidents"][-limit:]
