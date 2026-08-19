import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ALPRSpeedDetector")

class ALPRSpeedDetector:
    """
    Automatic License Plate Recognition (ALPR) & Real-World Speed Estimation Engine.
    Features:
    - Homography perspective calibration mapping pixel displacements to real-world kilometers per hour (km/h)
    - Automatic overspeeding detection & threshold flagging (> 60 km/h)
    - Simulated / OCR License Plate Extraction (e.g., 'NY-894-AB', 'CA-771-XY')
    """
    def __init__(
        self,
        pixels_per_meter: float = 8.5, # Homography calibration constant
        speed_limit_kmh: float = 60.0,
        fps: float = 30.0
    ):
        self.pixels_per_meter = pixels_per_meter
        self.speed_limit_kmh = speed_limit_kmh
        self.fps = fps

    def calculate_kmh(self, vx_px: float, vy_px: float) -> float:
        """
        Converts pixel velocity (pixels/frame) to real-world speed (km/h).
        Speed (m/s) = (pixels/frame * FPS) / pixels_per_meter
        Speed (km/h) = Speed (m/s) * 3.6
        """
        pixel_speed_per_frame = np.sqrt(vx_px**2 + vy_px**2)
        speed_mps = (pixel_speed_per_frame * self.fps) / self.pixels_per_meter
        speed_kmh = speed_mps * 3.6
        return round(float(speed_kmh), 1)

    def extract_license_plate(self, vehicle_bbox: List[int], track_id: int) -> str:
        """
        Extracts license plate ROI and returns deterministic license plate string.
        (Simulates OCR engine like Tesseract/EasyOCR/PaddleOCR).
        """
        prefixes = ["NY", "CA", "TX", "FL", "IL", "NJ"]
        prefix = prefixes[track_id % len(prefixes)]
        num = (track_id * 137 + 100) % 900 + 100
        suffix = chr(65 + (track_id % 26)) + chr(65 + ((track_id * 3) % 26))
        return f"{prefix}-{num}-{suffix}"

    def process_violations(self, tracked_vehicles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes active tracked vehicles, calculates real-world km/h speeds,
        and generates overspeeding violation events.
        """
        violations = []
        
        for v in tracked_vehicles:
            vx, vy = v["velocity"]
            speed_kmh = self.calculate_kmh(vx, vy)
            v["speed_kmh"] = speed_kmh
            
            plate_number = self.extract_license_plate(v["bbox"], v["track_id"])
            v["license_plate"] = plate_number
            
            if speed_kmh > self.speed_limit_kmh:
                logger.warning(f"OVERSPEEDING VIOLATION DETECTED! Vehicle #{v['track_id']} [{plate_number}] Speed: {speed_kmh} km/h (Limit: {self.speed_limit_kmh} km/h)")
                violations.append({
                    "track_id": v["track_id"],
                    "class_name": v["class_name"],
                    "license_plate": plate_number,
                    "speed_kmh": speed_kmh,
                    "speed_limit_kmh": self.speed_limit_kmh,
                    "bbox": v["bbox"]
                })

        return violations
