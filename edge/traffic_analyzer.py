import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TrafficAnalyzer")

class TrafficAnalyzer:
    """
    Advanced Traffic Analysis & Adaptive Signal Timing Engine.
    Computes:
    - Vehicle Counts & Class Breakdown
    - Road Occupancy Ratio (Omega)
    - Average Traffic Velocity & Queue Length
    - Quantitative Congestion Index Score (0 to 100)
    - Traffic Density & Congestion Levels
    - Adaptive Green Light Signal Duration Recommendation (seconds)
    """
    def __init__(
        self,
        roi_area_px: float = 640.0 * 640.0,
        stop_velocity_threshold: float = 1.0,
        base_green_time_sec: int = 20
    ):
        self.roi_area_px = roi_area_px
        self.stop_velocity_threshold = stop_velocity_threshold
        self.base_green_time_sec = base_green_time_sec

    def analyze(self, tracked_vehicles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes active tracked vehicles and computes comprehensive flow, congestion, and signal timing metrics.
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
        
        # 3. Quantitative Congestion Index (0 to 100)
        # Formulated combining occupancy, stopped vehicles ratio, and speed reduction ratio
        stopped_ratio = (stopped_count / vehicle_count) if vehicle_count > 0 else 0.0
        speed_factor = max(0.0, 1.0 - (avg_speed / 10.0)) # Normalized speed reduction factor
        
        congestion_index = round(min(100.0, (occupancy_ratio * 40.0) + (stopped_ratio * 35.0) + (speed_factor * 25.0)), 1)

        # 4. Density & Congestion Classification
        if vehicle_count < 5 or occupancy_ratio < 0.15:
            density_level = "LOW"
        elif vehicle_count < 15 or occupancy_ratio < 0.40:
            density_level = "MEDIUM"
        else:
            density_level = "HIGH"

        if vehicle_count == 0:
            congestion_level = "LOW"
        elif congestion_index >= 70.0:
            congestion_level = "SEVERE"
        elif congestion_index >= 45.0:
            congestion_level = "HIGH"
        elif congestion_index >= 20.0:
            congestion_level = "MEDIUM"
        else:
            congestion_level = "LOW"

        # 5. Adaptive Signal Control Recommendation (Green Light Time in Seconds)
        # Dynamically allocates longer green time for congested queues
        if congestion_level == "SEVERE":
            recommended_green_sec = self.base_green_time_sec + 40 # 60s green
        elif congestion_level == "HIGH":
            recommended_green_sec = self.base_green_time_sec + 25 # 45s green
        elif congestion_level == "MEDIUM":
            recommended_green_sec = self.base_green_time_sec + 10 # 30s green
        else:
            recommended_green_sec = self.base_green_time_sec # 20s default green

        return {
            "vehicle_count": vehicle_count,
            "class_breakdown": class_breakdown,
            "road_occupancy_ratio": occupancy_ratio,
            "average_speed_px": avg_speed,
            "stopped_vehicle_count": stopped_count,
            "congestion_index": congestion_index,
            "density_level": density_level,
            "congestion_level": congestion_level,
            "recommended_green_signal_sec": recommended_green_sec
        }
