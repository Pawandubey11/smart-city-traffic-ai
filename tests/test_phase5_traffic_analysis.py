import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader
from edge.detector import VehicleDetector
from edge.tracker import ByteTracker
from edge.traffic_analyzer import TrafficAnalyzer

def test_traffic_analysis():
    print("==================================================")
    print("PHASE 5 TRAFFIC CONGESTION & DENSITY TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    
    reader = VideoStreamReader(source=video_path, target_size=(640, 640))
    detector = VehicleDetector(confidence_threshold=0.30)
    tracker = ByteTracker()
    analyzer = TrafficAnalyzer()
    
    frame_count = 0
    
    for idx, ts, raw_frame, prep_frame in reader.get_frames():
        frame_count += 1
        detections = detector.detect(prep_frame)
        tracks = tracker.update(detections)
        metrics = analyzer.analyze(tracks)
        
        if frame_count in [5, 12, 20]:
            print(f"\nFrame {frame_count:02d} Traffic Metrics:")
            print(f"   - Vehicle Count: {metrics['vehicle_count']} ({metrics['class_breakdown']})")
            print(f"   - Road Occupancy Ratio: {metrics['road_occupancy_ratio'] * 100:.1f}%")
            print(f"   - Average Speed: {metrics['average_speed_px']} px/frame")
            print(f"   - Density Level: {metrics['density_level']}")
            print(f"   - Congestion Level: {metrics['congestion_level']}")
            
        if frame_count >= 25:
            break
            
    reader.release()
    
    assert "vehicle_count" in metrics
    assert "density_level" in metrics
    assert "congestion_level" in metrics
    
    print("\n==================================================")
    print("PHASE 5 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_traffic_analysis()
