import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TrafficAnalyzer")

class TrafficAnalyzer:
    """
    Traffic Analysis Engine.
    Computes vehicle counts, road occupancy ratio, average traffic speed,
    stopped vehicle ratios, traffic density, and congestion levels.
    """
    def __init__(
        self,
        roi_area_px: float = 640.0 * 640.0, # Default full 640x640 frame area
        stop_velocity_threshold: float = 1.0 # px/frame threshold for stopped vehicles
    ):
        self.roi_area_px = roi_area_px
        self.stop_velocity_threshold = stop_velocity_threshold

    def analyze(self, tracked_vehicles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes active tracked vehicles and returns comprehensive traffic metrics.
        """
        vehicle_count = len(tracked_vehicles)
        class_breakdown: Dict[str, int] = {}
        total_bbox_area = 0.0
        speeds: List[float] = []
        stopped_count = 0

        for vehicle in tracked_vehicles:
            cname = vehicle["class_name"]
            class_breakdown[cname] = class_breakdown.get(cname, 0) + 1
            
            x1, y1, x2, y2 = vehicle["bbox"]
            area = float(max(0, x2 - x1) * max(0, y2 - y1))
            total_bbox_area += area
            
            vx, vy = vehicle["velocity"]
            speed = float(np.sqrt(vx**2 + vy**2))
            speeds.append(speed)
            
            if speed < self.stop_velocity_threshold:
                stopped_count += 1

        # 1. Road Occupancy Ratio (0.0 to 1.0)
        occupancy_ratio = float(total_bbox_area / self.roi_area_px) if self.roi_area_px > 0 else 0.0
        occupancy_ratio = min(1.0, round(occupancy_ratio, 4))
        
        # 2. Average Speed (px / frame)
        avg_speed = round(float(np.mean(speeds)), 2) if speeds else 0.0
        
        # 3. Traffic Density Classification
        # Density measures the static physical presence/concentration of vehicles in scene.
        if vehicle_count < 5 or occupancy_ratio < 0.15:
            density_level = "LOW"
        elif vehicle_count < 15 or occupancy_ratio < 0.40:
            density_level = "MEDIUM"
        else:
            density_level = "HIGH"

        # 4. Traffic Congestion Classification
        # Congestion measures flow restriction (High Density + Low Movement Speed + Stopped Vehicles).
        if vehicle_count == 0:
            congestion_level = "LOW"
        elif occupancy_ratio >= 0.55 and (avg_speed < 1.5 or (stopped_count / vehicle_count) > 0.50):
            congestion_level = "SEVERE"
        elif occupancy_ratio >= 0.35 and (avg_speed < 3.0 or (stopped_count / vehicle_count) > 0.30):
            congestion_level = "HIGH"
        elif occupancy_ratio >= 0.20 or avg_speed < 5.0:
            congestion_level = "MEDIUM"
        else:
            congestion_level = "LOW"

        return {
            "vehicle_count": vehicle_count,
            "class_breakdown": class_breakdown,
            "road_occupancy_ratio": occupancy_ratio,
            "average_speed_px": avg_speed,
            "stopped_vehicle_count": stopped_count,
            "density_level": density_level,
            "congestion_level": congestion_level
        }
