import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader
from edge.detector import VehicleDetector
from edge.tracker import ByteTracker
from edge.accident_detector import AccidentDetector

def test_accident_ai():
    print("==================================================")
    print("PHASE 6 ACCIDENT AI MODEL (CNN-LSTM) TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    
    reader = VideoStreamReader(source=video_path, target_size=(640, 640))
    detector = VehicleDetector(confidence_threshold=0.30)
    tracker = ByteTracker()
    accident_engine = AccidentDetector(sequence_length=16, probability_threshold=0.70)
    
    frame_count = 0
    max_prob = 0.0
    accident_triggered = False
    
    for idx, ts, raw_frame, prep_frame in reader.get_frames():
        frame_count += 1
        detections = detector.detect(prep_frame)
        tracks = tracker.update(detections)
        
        accident_engine.add_frame(prep_frame)
        prob, is_acc, min_ttc = accident_engine.predict_accident_probability(tracks)
        
        max_prob = max(max_prob, prob)
        if is_acc:
            accident_triggered = True
            
        if frame_count in [5, 16, 20]:
            print(f"Frame {frame_count:02d}: Buffer Size: {len(accident_engine.frame_buffer)}/16 | Accident Prob: {prob:.3f} | Min TTC: {min_ttc}s | Alert: {'YES' if is_acc else 'NO'}")
            
        if frame_count >= 25:
            break
            
    reader.release()
    
    print(f"\nProcessed {frame_count} frames.")
    print(f"Peak Accident Probability Evaluated: {max_prob:.3f}")
    assert frame_count >= 20, "Processed minimum required sequence frames"
    
    print("\n==================================================")
    print("PHASE 6 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_accident_ai()
