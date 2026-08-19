import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EmergencyPriority")

class EmergencyVehiclePrioritySystem:
    """
    Emergency Vehicle Preemption & Priority Signal Override System.
    Detects approaching Ambulances, Fire Trucks, and Police cars in camera feeds
    and triggers instant GREEN SIGNAL OVERRIDE (90s) to clear emergency corridors.
    """
    def __init__(self, override_green_sec: int = 90):
        self.override_green_sec = override_green_sec

    def evaluate_emergency_priority(self, tracked_vehicles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans active tracked vehicles for emergency responder classes.
        Returns emergency status payload and signal preemption override recommendations.
        """
        emergency_classes = ["ambulance", "fire truck", "police car"]
        detected_emergency_vehicles = []

        for v in tracked_vehicles:
            cname = v["class_name"].lower()
            if any(e_cls in cname for e_cls in emergency_classes) or v.get("is_emergency", False):
                detected_emergency_vehicles.append(v)

        has_emergency = len(detected_emergency_vehicles) > 0
        
        if has_emergency:
            logger.critical(f"🚨 EMERGENCY VEHICLE DETECTED! Triggering Emergency Green Corridor Preemption ({self.override_green_sec} seconds).")

        return {
            "emergency_vehicle_detected": has_emergency,
            "emergency_vehicle_count": len(detected_emergency_vehicles),
            "signal_override_active": has_emergency,
            "preemption_green_duration_sec": self.override_green_sec if has_emergency else 0
        }
