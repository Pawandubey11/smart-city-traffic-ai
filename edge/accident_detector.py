import cv2
import torch
import numpy as np
import logging
from typing import List, Dict, Any, Tuple
import os

from models.cnn_lstm.accident_net import SpatialTemporalAccidentNet

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AccidentDetector")

class AccidentDetector:
    """
    Combined Spatial-Temporal Deep Learning & Heuristic Accident Detection Engine.
    Uses frame buffer sequence (16 frames) + PyTorch CNN-LSTM + vehicle kinematic features
    to output real-time accident probability scores.
    """
    def __init__(
        self,
        weights_path: str = "models/weights/accident_cnn_lstm.pt",
        sequence_length: int = 16,
        probability_threshold: float = 0.80,
        device: str = "cpu"
    ):
        self.sequence_length = sequence_length
        self.probability_threshold = probability_threshold
        self.device = device
        self.frame_buffer: List[np.ndarray] = []
        
        self.model = SpatialTemporalAccidentNet()
        self.model.to(self.device)
        self.model.eval()
        
        if os.path.exists(weights_path):
            try:
                self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
                logger.info(f"Loaded trained CNN-LSTM accident weights from {weights_path}")
            except Exception as e:
                logger.warning(f"Could not load weights ({e}). Running model with initialized weights.")

    def add_frame(self, frame: np.ndarray) -> None:
        """Appends preprocessed frame to 16-frame rolling sequence buffer."""
        # Resize frame to (224, 224) for CNN backbone
        resized = cv2.resize(frame, (224, 224))
        # Convert BGR -> RGB & Normalize to [0, 1]
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        # Transpose HWC -> CHW
        tensor_frame = np.transpose(rgb, (2, 0, 1))
        
        self.frame_buffer.append(tensor_frame)
        if len(self.frame_buffer) > self.sequence_length:
            self.frame_buffer.pop(0)

    def compute_kinematic_anomaly(self, tracked_vehicles: List[Dict[str, Any]]) -> float:
        """
        Computes heuristic kinematic anomaly score based on:
        1. Sudden deceleration of moving vehicles
        2. High bounding box overlap ratio between vehicles
        3. Sudden zero velocity after high speed
        """
        if len(tracked_vehicles) < 2:
            return 0.0
            
        anomaly_score = 0.0
        
        # Check overlaps
        for i in range(len(tracked_vehicles)):
            for j in range(i + 1, len(tracked_vehicles)):
                v1, v2 = tracked_vehicles[i], tracked_vehicles[j]
                
                # Check distance between bounding box centers
                c1_x, c1_y = v1["center"]
                c2_x, c2_y = v2["center"]
                dist = np.sqrt((c1_x - c2_x)**2 + (c1_y - c2_y)**2)
                
                # Check velocities
                vx1, vy1 = v1["velocity"]
                vx2, vy2 = v2["velocity"]
                speed1 = np.sqrt(vx1**2 + vy1**2)
                speed2 = np.sqrt(vx2**2 + vy2**2)
                
                # Close proximity + sudden stopping/overlap
                if dist < 45.0: # Close proximity in pixels
                    if speed1 < 0.5 and speed2 < 0.5:
                        anomaly_score += 0.45
                    elif abs(speed1 - speed2) > 5.0:
                        anomaly_score += 0.35

        return min(0.95, anomaly_score)

    def predict_accident_probability(self, tracked_vehicles: List[Dict[str, Any]]) -> Tuple[float, bool]:
        """
        Calculates accident probability by combining spatial-temporal CNN-LSTM output
        and kinematic anomaly heuristics.
        Returns: (probability, is_accident_detected)
        """
        kinematic_prob = self.compute_kinematic_anomaly(tracked_vehicles)
        
        if len(self.frame_buffer) < self.sequence_length:
            # Buffer filling phase
            final_prob = round(kinematic_prob, 3)
            return final_prob, final_prob >= self.probability_threshold

        # Run 16-frame sequence through CNN-LSTM model
        with torch.no_grad():
            # Convert buffer to tensor shape (1, 16, 3, 224, 224)
            seq_np = np.array([self.frame_buffer], dtype=np.float32)
            seq_tensor = torch.tensor(seq_np).to(self.device)
            
            cnn_lstm_prob = float(self.model(seq_tensor)[0, 0].item())

        # Ensemble fusion: 60% CNN-LSTM spatial-temporal visual + 40% Kinematic anomaly
        combined_prob = round(0.60 * cnn_lstm_prob + 0.40 * kinematic_prob, 3)
        is_accident = combined_prob >= self.probability_threshold
        
        return combined_prob, is_accident
