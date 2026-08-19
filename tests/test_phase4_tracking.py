import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader
from edge.detector import VehicleDetector
from edge.tracker import ByteTracker

def test_tracking():
    print("==================================================")
    print("PHASE 4 VEHICLE TRACKING TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    
    reader = VideoStreamReader(source=video_path, target_size=(640, 640))
    detector = VehicleDetector(confidence_threshold=0.30)
    tracker = ByteTracker(iou_threshold=0.25)
    
    unique_track_ids = set()
    frame_count = 0
    
    for idx, ts, raw_frame, prep_frame in reader.get_frames():
        frame_count += 1
        detections = detector.detect(prep_frame)
        tracks = tracker.update(detections)
        
        for t in tracks:
            unique_track_ids.add(t["track_id"])
            
        if frame_count in [1, 5, 10]:
            print(f"Frame {frame_count:02d}: Active Tracks ({len(tracks)}):")
            for t in tracks:
                vx, vy = t["velocity"]
                print(f"   - Vehicle #{t['track_id']} ({t['class_name']}) @ BBox {t['bbox']} | Velocity ({vx:.1f}, {vy:.1f}) px/frame")
                
        if frame_count >= 20:
            break
            
    reader.release()
    
    print(f"\nProcessed {frame_count} frames.")
    print(f"Unique tracked vehicles assigned distinct Track IDs: {sorted(list(unique_track_ids))}")
    assert len(unique_track_ids) > 0, "Expected persistent track IDs to be assigned"
    
    print("\n==================================================")
    print("PHASE 4 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_tracking()
