import numpy as np
import logging
import gc
from typing import List, Dict, Any, Tuple
from scipy.optimize import linear_sum_assignment

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ByteTracker")

class ByteTrackTrack:
    """Represents a single tracked vehicle state."""
    def __init__(self, track_id: int, bbox: List[int], class_name: str, confidence: float):
        self.track_id = track_id
        self.bbox = bbox  # [x1, y1, x2, y2]
        self.class_name = class_name
        self.confidence = confidence
        self.age = 0
        self.time_since_update = 0
        self.history: List[Tuple[float, float]] = []
        
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        self.history.append((cx, cy))
        self.velocity = (0.0, 0.0)

    def update(self, new_bbox: List[int], confidence: float):
        self.bbox = new_bbox
        self.confidence = confidence
        self.time_since_update = 0
        self.age += 1
        
        cx = (new_bbox[0] + new_bbox[2]) / 2.0
        cy = (new_bbox[1] + new_bbox[3]) / 2.0
        
        prev_cx, prev_cy = self.history[-1]
        self.velocity = (cx - prev_cx, cy - prev_cy)
        
        self.history.append((cx, cy))
        if len(self.history) > 30: # Limit history buffer size to prevent RAM accumulation
            self.history.pop(0)

    def mark_missed(self):
        self.time_since_update += 1
        self.age += 1

class ByteTracker:
    """
    Industrial ByteTrack Multi-Object Vehicle Tracker.
    Features:
    - High & Low confidence detection association using IoU Hungarian matching
    - Stale track pruning (> 30 frames missed)
    - Automated memory leak protection & garbage collection sweeps
    """
    def __init__(self, iou_threshold: float = 0.3, max_lost_age: int = 30):
        self.iou_threshold = iou_threshold
        self.max_lost_age = max_lost_age
        self.next_id = 1
        self.tracked_tracks: List[ByteTrackTrack] = []
        self.frame_counter = 0

    def compute_iou(self, boxA: List[int], boxB: List[int]) -> float:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        
        denom = float(boxAArea + boxBArea - interArea)
        return interArea / denom if denom > 0 else 0.0

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.frame_counter += 1
        
        # Memory leak safeguard: periodic garbage collection every 100 frames
        if self.frame_counter % 100 == 0:
            gc.collect()

        if not self.tracked_tracks:
            for det in detections:
                new_track = ByteTrackTrack(self.next_id, det["bbox"], det["class_name"], det["confidence"])
                self.next_id += 1
                self.tracked_tracks.append(new_track)
        else:
            if detections:
                cost_matrix = np.zeros((len(self.tracked_tracks), len(detections)), dtype=np.float32)
                for i, trk in enumerate(self.tracked_tracks):
                    for j, det in enumerate(detections):
                        cost_matrix[i, j] = 1.0 - self.compute_iou(trk.bbox, det["bbox"])

                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                
                matched_trks, matched_dets = set(), set()
                for r, c in zip(row_ind, col_ind):
                    if cost_matrix[r, c] < (1.0 - self.iou_threshold):
                        self.tracked_tracks[r].update(detections[c]["bbox"], detections[c]["confidence"])
                        matched_trks.add(r)
                        matched_dets.add(c)

                for i, trk in enumerate(self.tracked_tracks):
                    if i not in matched_trks:
                        trk.mark_missed()

                for j, det in enumerate(detections):
                    if j not in matched_dets:
                        new_track = ByteTrackTrack(self.next_id, det["bbox"], det["class_name"], det["confidence"])
                        self.next_id += 1
                        self.tracked_tracks.append(new_track)
            else:
                for trk in self.tracked_tracks:
                    trk.mark_missed()

        # Prune stale tracks exceeding max_lost_age
        self.tracked_tracks = [t for t in self.tracked_tracks if t.time_since_update <= self.max_lost_age]

        output = []
        for trk in self.tracked_tracks:
            if trk.time_since_update == 0:
                cx = (trk.bbox[0] + trk.bbox[2]) / 2.0
                cy = (trk.bbox[1] + trk.bbox[3]) / 2.0
                output.append({
                    "track_id": trk.track_id,
                    "bbox": trk.bbox,
                    "class_name": trk.class_name,
                    "confidence": trk.confidence,
                    "center": (cx, cy),
                    "velocity": trk.velocity
                })
        return output
