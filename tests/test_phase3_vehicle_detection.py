import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader
from edge.detector import VehicleDetector

def test_vehicle_detection():
    print("==================================================")
    print("PHASE 3 VEHICLE DETECTION TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Video not found at {video_path}"
    
    reader = VideoStreamReader(source=video_path, target_size=(640, 640))
    detector = VehicleDetector(confidence_threshold=0.10)
    
    total_detections = 0
    frame_count = 0
    
    for idx, ts, raw_frame, prep_frame in reader.get_frames():
        frame_count += 1
        detections = detector.detect(prep_frame)
        annotated = detector.draw_detections(prep_frame, detections)
        total_detections += len(detections)
        
        if frame_count == 1:
            print(f"Sample Detections on Frame 1 ({len(detections)} vehicles found):")
            for d in detections[:3]:
                print(f"   - Class: {d['class_name']} | Conf: {d['confidence']} | BBox: {d['bbox']}")
                
        if frame_count >= 15:
            break
            
    reader.release()
    
    print(f"\nProcessed {frame_count} frames.")
    print(f"Total vehicle detections across frames: {total_detections}")
    assert frame_count >= 15, "Expected 15 frames to be processed"
    
    print("\n==================================================")
    print("PHASE 3 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_vehicle_detection()
