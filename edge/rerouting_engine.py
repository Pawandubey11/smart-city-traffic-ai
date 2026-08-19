import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ReroutingEngine")

class AutomatedIncidentReroutingEngine:
    """
    Automated Incident Response & Intelligent Traffic Rerouting Engine.
    Evaluates real-time camera congestion metrics and accident alerts,
    generates optimal detour routing strategies, and controls Variable Message Signs (VMS).
    """
    def __init__(self):
        self.city_corridors = {
            "CAM-EAST-003": {
                "name": "Noida-Greater Noida Expressway Toll",
                "primary_route": "Expressway Main Line",
                "detour_route": "Knowledge Park II Arterial Road -> Pari Chowk Bypass",
                "estimated_time_saving_min": 14.5,
                "vms_billboard_id": "VMS-GREATER-NOIDA-01"
            },
            "CAM-NORTH-001": {
                "name": "Pari Chowk Junction",
                "primary_route": "Pari Chowk Central Roundabout",
                "detour_route": "Sector 150 Flyover Outer Ring Road",
                "estimated_time_saving_min": 9.2,
                "vms_billboard_id": "VMS-GREATER-NOIDA-02"
            }
        }

    def evaluate_rerouting_strategy(self, camera_id: str, congestion_index: float, accident_detected: bool) -> Dict[str, Any]:
        """Evaluates whether incident rerouting & VMS billboards should be activated."""
        corridor = self.city_corridors.get(camera_id, {
            "name": f"Junction {camera_id}",
            "primary_route": "Main Arterial",
            "detour_route": "Outer Ring Bypass",
            "estimated_time_saving_min": 10.0,
            "vms_billboard_id": "VMS-GENERIC-01"
        })

        reroute_required = accident_detected or congestion_index > 85.0
        
        if reroute_required:
            action_status = "ACTIVE_REROUTING"
            vms_message = f"[INCIDENT DETOUR] AT {corridor['name'].upper()}! USE DETOUR: {corridor['detour_route'].upper()}"
            logger.warning(f"[REROUTING ACTIVATED] {corridor['vms_billboard_id']} -> Message: {vms_message}")
        else:
            action_status = "NORMAL_FLOW"
            vms_message = f"[NORMAL FLOW] {corridor['name'].upper()}: TRAFFIC FLOW NORMAL"

        response_payload = {
            "camera_id": camera_id,
            "corridor_name": corridor["name"],
            "action_status": action_status,
            "reroute_required": reroute_required,
            "detour_strategy": corridor["detour_route"],
            "estimated_time_saved_minutes": corridor["estimated_time_saving_min"],
            "vms_billboard": {
                "id": corridor["vms_billboard_id"],
                "active_message": vms_message
            },
            "emergency_services_notified": reroute_required
        }
        
        return response_payload
