import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.main import run_edge_pipeline

def test_local_prototype():
    print("==================================================")
    print("PHASE 7 INTEGRATED LOCAL EDGE AI PROTOTYPE TEST")
    print("==================================================")
    
    video_path = "data/sample_traffic.mp4"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    
    # Run full integrated local edge pipeline for 30 frames
    run_edge_pipeline(video_source=video_path, camera_id="TEST-CAM-001", max_frames=30)
    
    print("\n==================================================")
    print("PHASE 7 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_local_prototype()
