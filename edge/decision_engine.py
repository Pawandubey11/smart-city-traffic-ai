import cv2
import json
import time
import os
import logging
import numpy as np
from typing import Dict, Any, Optional, Tuple

from edge.detector import VehicleDetector
from edge.tracker import ByteTracker
from edge.traffic_analyzer import TrafficAnalyzer
from edge.accident_detector import AccidentDetector
from edge.alpr_speed_detector import ALPRSpeedDetector
from edge.emergency_priority import EmergencyVehiclePrioritySystem

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DecisionEngine")

class LocalDecisionEngine:
    """
    State-of-the-Art Edge Decision & Smart City Event Engine.
    Combines:
    - YOLOv8 Object Detection & ByteTrack Multi-Object Tracking
    - Quantitative Congestion Index Scoring & Adaptive Traffic Signal Timing
    - Real-World km/h Speed Estimation & Automatic License Plate Recognition (ALPR)
    - Emergency Vehicle Corridor Preemption & Priority Override Signal Control
    - PyTorch CNN-LSTM 16-Frame Spatial-Temporal Model & Time-To-Collision (TTC) Physics
    """
    def __init__(
        self,
        camera_id: str = "CAM-NORTH-001",
        evidence_dir: str = "data/evidence_snapshots",
        telemetry_interval_sec: float = 5.0,
        accident_threshold: float = 0.75
    ):
        self.camera_id = camera_id
        self.evidence_dir = evidence_dir
        self.telemetry_interval_sec = telemetry_interval_sec
        self.accident_threshold = accident_threshold
        
        self.detector = VehicleDetector()
        self.tracker = ByteTracker()
        self.analyzer = TrafficAnalyzer()
        self.accident_engine = AccidentDetector(probability_threshold=accident_threshold)
        self.alpr_speed_engine = ALPRSpeedDetector(speed_limit_kmh=60.0)
        self.emergency_system = EmergencyVehiclePrioritySystem()
        
        self.last_telemetry_time = 0.0
        os.makedirs(self.evidence_dir, exist_ok=True)

    def process_frame(self, frame_idx: int, timestamp_ms: float, raw_frame: np.ndarray, prep_frame: np.ndarray) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Processes a single video frame through the unified AI vision pipeline.
        Returns: (telemetry_event, accident_event)
        """
        # 1. Detection & Multi-Object Tracking
        detections = self.detector.detect(prep_frame)
        tracks = self.tracker.update(detections)
        
        # 2. ALPR License Plate & Real-World km/h Speed Violations
        speed_violations = self.alpr_speed_engine.process_violations(tracks)
        
        # 3. Emergency Vehicle Priority Corridor Evaluation
        emergency_status = self.emergency_system.evaluate_emergency_priority(tracks)
        
        # 4. Traffic Flow & Adaptive Signal Timing Analysis
        traffic_metrics = self.analyzer.analyze(tracks)
        if emergency_status["signal_override_active"]:
            traffic_metrics["recommended_green_signal_sec"] = emergency_status["preemption_green_duration_sec"]
            traffic_metrics["emergency_preemption_active"] = True
            
        # 5. Spatial-Temporal & Physics TTC Accident Detection
        self.accident_engine.add_frame(prep_frame)
        accident_prob, is_accident, min_ttc_sec = self.accident_engine.predict_accident_probability(tracks)
        
        telemetry_event = None
        accident_event = None
        
        current_time = time.time()
        
        # 6. Periodic Routine Telemetry Payload Emission
        if (current_time - self.last_telemetry_time) >= self.telemetry_interval_sec:
            self.last_telemetry_time = current_time
            telemetry_event = {
                "event_type": "TELEMETRY",
                "camera_id": self.camera_id,
                "timestamp_ms": int(timestamp_ms),
                "metrics": traffic_metrics,
                "accident_probability": accident_prob,
                "min_time_to_collision_sec": min_ttc_sec,
                "speed_violations": speed_violations,
                "emergency_corridor_active": emergency_status["signal_override_active"]
            }

        # 7. High-Priority Emergency Accident Event Emission
        if is_accident:
            snapshot_filename = f"accident_{self.camera_id}_{int(timestamp_ms)}.jpg"
            snapshot_path = os.path.join(self.evidence_dir, snapshot_filename)
            
            # Draw detections and alert banner on evidence snapshot
            annotated_frame = self.detector.draw_detections(prep_frame, detections)
            cv2.putText(
                annotated_frame,
                f"CRITICAL ACCIDENT DETECTED ({int(accident_prob*100)}%)",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                3
            )
            cv2.imwrite(snapshot_path, annotated_frame)
            logger.critical(f"CRITICAL ACCIDENT DETECTED! Saved snapshot to {snapshot_path}")
            
            accident_event = {
                "event_type": "ACCIDENT_ALERT",
                "camera_id": self.camera_id,
                "timestamp_ms": int(timestamp_ms),
                "severity": "CRITICAL" if accident_prob >= 0.85 else "MODERATE",
                "accident_probability": accident_prob,
                "min_time_to_collision_sec": min_ttc_sec,
                "snapshot_local_path": snapshot_path,
                "traffic_snapshot": traffic_metrics
            }

        return telemetry_event, accident_event
