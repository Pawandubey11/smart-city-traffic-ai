import json
import logging
import time
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("APIRouterLambda")

# Mock Database Store for REST APIs
MOCK_CAMERAS = [
    {
        "camera_id": "CAM-NORTH-001",
        "location_name": "North Junction & 5th Ave",
        "latitude": 40.712776,
        "longitude": -74.005974,
        "status": "ACTIVE",
        "fps": 30,
        "vehicle_count": 28,
        "density_level": "HIGH",
        "congestion_level": "HIGH"
    },
    {
        "camera_id": "CAM-SOUTH-002",
        "location_name": "South Expressway Exit 12",
        "latitude": 40.705000,
        "longitude": -74.011000,
        "status": "ACTIVE",
        "fps": 30,
        "vehicle_count": 12,
        "density_level": "MEDIUM",
        "congestion_level": "LOW"
    },
    {
        "camera_id": "CAM-EAST-003",
        "location_name": "East Bridge Toll Plaza",
        "latitude": 40.720000,
        "longitude": -73.995000,
        "status": "ACTIVE",
        "fps": 28,
        "vehicle_count": 45,
        "density_level": "HIGH",
        "congestion_level": "SEVERE"
    }
]

MOCK_ACCIDENTS = [
    {
        "accident_id": "acc-9842",
        "camera_id": "CAM-EAST-003",
        "location_name": "East Bridge Toll Plaza",
        "latitude": 40.720000,
        "longitude": -73.995000,
        "timestamp_str": "2026-08-19 22:45:12 UTC",
        "confidence_score": 0.94,
        "severity": "CRITICAL",
        "s3_presigned_url": "https://smart-city-traffic-evidence-demo.s3.amazonaws.com/accidents/CAM-EAST-003/acc_9842.jpg",
        "status": "UNRESOLVED"
    },
    {
        "accident_id": "acc-9841",
        "camera_id": "CAM-NORTH-001",
        "location_name": "North Junction & 5th Ave",
        "latitude": 40.712776,
        "longitude": -74.005974,
        "timestamp_str": "2026-08-19 18:30:00 UTC",
        "confidence_score": 0.88,
        "severity": "MODERATE",
        "s3_presigned_url": "https://smart-city-traffic-evidence-demo.s3.amazonaws.com/accidents/CAM-NORTH-001/acc_9841.jpg",
        "status": "RESOLVED"
    }
]

def build_response(status_code: int, body_data: Any) -> Dict[str, Any]:
    """Formats CORS-enabled API Gateway proxy HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
        "body": json.dumps(body_data)
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Amazon API Gateway Proxy Lambda Handler.
    Routes REST requests for camera status, live traffic, historical trends, and accident alerts.
    """
    path = event.get("path", "/cameras")
    method = event.get("httpMethod", "GET")
    
    logger.info(f"API Gateway Request: {method} {path}")
    
    if path == "/cameras":
        return build_response(200, {"status": "SUCCESS", "cameras": MOCK_CAMERAS})
        
    elif path == "/traffic/current":
        return build_response(200, {
            "status": "SUCCESS",
            "timestamp": int(time.time()),
            "total_active_vehicles": sum(c["vehicle_count"] for c in MOCK_CAMERAS),
            "city_congestion_summary": "HIGH",
            "camera_metrics": MOCK_CAMERAS
        })
        
    elif path == "/traffic/history":
        history_points = [
            {"time": "18:00", "count": 65, "avg_speed": 35.0},
            {"time": "19:00", "count": 82, "avg_speed": 22.5},
            {"time": "20:00", "count": 95, "avg_speed": 14.0},
            {"time": "21:00", "count": 70, "avg_speed": 28.0},
            {"time": "22:00", "count": 85, "avg_speed": 18.0},
            {"time": "23:00", "count": 55, "avg_speed": 40.0}
        ]
        return build_response(200, {"status": "SUCCESS", "history": history_points})
        
    elif path == "/accidents":
        return build_response(200, {"status": "SUCCESS", "accidents": MOCK_ACCIDENTS})
        
    elif path == "/statistics":
        stats = {
            "total_monitored_junctions": len(MOCK_CAMERAS),
            "active_ai_edge_nodes": len(MOCK_CAMERAS),
            "accidents_today": 2,
            "severe_congestion_zones": 1,
            "average_emergency_response_sec": 145,
            "system_uptime_percentage": 99.98
        }
        return build_response(200, {"status": "SUCCESS", "statistics": stats})
        
    else:
        return build_response(404, {"status": "ERROR", "message": f"Endpoint {path} not found"})
