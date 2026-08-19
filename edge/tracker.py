import numpy as np
from scipy.optimize import linear_sum_assignment
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ByteTrackTracker")

def compute_iou(box1: List[int], box2: List[int]) -> float:
    """Computes Intersection over Union (IoU) between two bounding boxes [x1, y1, x2, y2]."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0

class Tracklet:
    """Represents a single tracked vehicle over time."""
    def __init__(self, track_id: int, bbox: List[int], class_name: str, confidence: float):
        self.track_id = track_id
        self.bbox = bbox
        self.class_name = class_name
        self.confidence = confidence
        self.history: List[Tuple[float, float]] = [] # Center points [(cx, cy)]
        self.frames_seen = 1
        self.frames_lost = 0
        self.time_in_scene_sec = 0.0
        self.velocity = (0.0, 0.0) # (vx, vy) pixels/frame
        
        self.update_position(bbox)

    @property
    def center(self) -> Tuple[float, float]:
        cx = (self.bbox[0] + self.bbox[2]) / 2.0
        cy = (self.bbox[1] + self.bbox[3]) / 2.0
        return (cx, cy)

    def update_position(self, new_bbox: List[int], confidence: float = 0.0) -> None:
        """Updates tracklet state with new bounding box."""
        if len(self.history) > 0:
            prev_cx, prev_cy = self.history[-1]
            curr_cx = (new_bbox[0] + new_bbox[2]) / 2.0
            curr_cy = (new_bbox[1] + new_bbox[3]) / 2.0
            self.velocity = (curr_cx - prev_cx, curr_cy - prev_cy)

        self.bbox = new_bbox
        if confidence > 0:
            self.confidence = confidence
        self.history.append(self.center)
        if len(self.history) > 30: # Limit history window
            self.history.pop(0)
            
        self.frames_seen += 1
        self.frames_lost = 0

    def mark_lost(self) -> None:
        self.frames_lost += 1

class ByteTracker:
    """
    ByteTrack-style Multi-Object Tracker.
    Associates high-confidence detections first, then low-confidence detections,
    maintaining robust track persistent IDs across occlusions and frame noise.
    """
    def __init__(
        self,
        iou_threshold: float = 0.30,
        max_lost_frames: int = 15,
        high_conf_thresh: float = 0.50
    ):
        self.iou_threshold = iou_threshold
        self.max_lost_frames = max_lost_frames
        self.high_conf_thresh = high_conf_thresh
        
        self.next_track_id = 1
        self.tracked_vehicles: Dict[int, Tracklet] = {}

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Updates internal tracking state with new detections for current frame.
        Returns list of active tracked objects with track IDs.
        """
        # Separate detections into high confidence and low confidence
        high_dets = [d for d in detections if d["confidence"] >= self.high_conf_thresh]
        low_dets = [d for d in detections if d["confidence"] < self.high_conf_thresh]
        
        active_ids = list(self.tracked_vehicles.keys())
        
        # 1. Match active tracklets with high-confidence detections
        matched_track_indices, unmatched_det_indices, unmatched_track_indices = self._match_iou(
            active_ids, high_dets, self.iou_threshold
        )
        
        # Update matched tracks
        for t_idx, d_idx in matched_track_indices:
            track_id = active_ids[t_idx]
            det = high_dets[d_idx]
            self.tracked_vehicles[track_id].update_position(det["bbox"], det["confidence"])
            
        # 2. Match remaining unmatched tracks with low-confidence detections
        unmatched_track_ids = [active_ids[i] for i in unmatched_track_indices]
        if unmatched_track_ids and low_dets:
            matched_low, _, remaining_tracks = self._match_iou(
                unmatched_track_ids, low_dets, self.iou_threshold - 0.1
            )
            for t_idx, d_idx in matched_low:
                track_id = unmatched_track_ids[t_idx]
                det = low_dets[d_idx]
                self.tracked_vehicles[track_id].update_position(det["bbox"], det["confidence"])
            unmatched_track_ids = [unmatched_track_ids[i] for i in remaining_tracks]

        # Mark remaining unmatched tracklets as lost
        for tid in unmatched_track_ids:
            self.tracked_vehicles[tid].mark_lost()
            if self.tracked_vehicles[tid].frames_lost > self.max_lost_frames:
                del self.tracked_vehicles[tid]
                
        # 3. Create new tracklets for unmatched high-confidence detections
        for d_idx in unmatched_det_indices:
            det = high_dets[d_idx]
            new_track = Tracklet(
                track_id=self.next_track_id,
                bbox=det["bbox"],
                class_name=det["class_name"],
                confidence=det["confidence"]
            )
            self.tracked_vehicles[self.next_track_id] = new_track
            self.next_track_id += 1

        # Format output active tracks
        results = []
        for tid, tracklet in self.tracked_vehicles.items():
            if tracklet.frames_lost == 0: # Only return actively matched tracks
                results.append({
                    "track_id": tid,
                    "class_name": tracklet.class_name,
                    "confidence": tracklet.confidence,
                    "bbox": tracklet.bbox,
                    "center": tracklet.center,
                    "velocity": tracklet.velocity,
                    "history": tracklet.history
                })

        return results

    def _match_iou(
        self,
        track_ids: List[int],
        detections: List[Dict[str, Any]],
        iou_thresh: float
    ) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
        """Hungarian algorithm IOU matching between tracklets and detections."""
        if not track_ids or not detections:
            return [], list(range(len(detections))), list(range(len(track_ids)))
            
        cost_matrix = np.zeros((len(track_ids), len(detections)), dtype=np.float32)
        
        for i, tid in enumerate(track_ids):
            track_box = self.tracked_vehicles[tid].bbox
            for j, det in enumerate(detections):
                iou = compute_iou(track_box, det["bbox"])
                cost_matrix[i, j] = 1.0 - iou # Hungarian minimizes cost
                
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        matched = []
        unmatched_dets = set(range(len(detections)))
        unmatched_tracks = set(range(len(track_ids)))
        
        for r, c in zip(row_ind, col_ind):
            if cost_matrix[r, c] <= (1.0 - iou_thresh):
                matched.append((r, c))
                unmatched_dets.discard(c)
                unmatched_tracks.discard(r)

        return matched, list(unmatched_dets), list(unmatched_tracks)
