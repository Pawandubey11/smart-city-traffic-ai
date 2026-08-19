import os
import sys
import numpy as np

# Ensure project root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader

def test_video_pipeline():
    print("==================================================")
    print("PHASE 2 VIDEO PIPELINE TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Sample video not found at {video_path}"
    
    roi_poly = [[100, 100], [1180, 100], [1180, 650], [100, 650]]
    reader = VideoStreamReader(
        source=video_path,
        target_size=(640, 640),
        frame_sample_rate=2,
        roi_polygon=roi_poly
    )
    
    frame_count = 0
    raw_shape = None
    prep_shape = None
    
    for idx, ts, raw_frame, prep_frame in reader.get_frames():
        frame_count += 1
        raw_shape = raw_frame.shape
        prep_shape = prep_frame.shape
        if frame_count >= 10:
            break
            
    reader.release()
    
    print(f"Processed {frame_count} sampled frames successfully.")
    print(f"Raw Frame Shape: {raw_shape}")
    print(f"Preprocessed Frame Shape: {prep_shape}")
    
    assert frame_count == 10, "Expected 10 sampled frames"
    assert prep_shape == (640, 640, 3), f"Expected (640, 640, 3), got {prep_shape}"
    
    print("\n==================================================")
    print("PHASE 2 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_video_pipeline()
