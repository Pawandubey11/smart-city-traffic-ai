import os
import sys
import json
import logging
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.video_stream import VideoStreamReader
from edge.decision_engine import LocalDecisionEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EdgeMain")

def run_edge_pipeline(video_source: str, camera_id: str, max_frames: int = 100):
    logger.info("==================================================")
    logger.info(f"STARTING SMART CITY EDGE AI SERVICE [{camera_id}]")
    logger.info("==================================================")
    
    # Auto-generate sample video if missing
    if not os.path.exists(video_source) and video_source.endswith(".mp4"):
        logger.warning(f"Video file {video_source} not found. Auto-generating sample traffic video...")
        try:
            from data.create_sample_traffic_video import generate_sample_traffic_video
            generate_sample_traffic_video(output_path=video_source)
        except Exception as e:
            logger.error(f"Could not auto-generate sample video: {e}")

    stream = VideoStreamReader(source=video_source, target_size=(640, 640), frame_sample_rate=1)
    engine = LocalDecisionEngine(camera_id=camera_id, telemetry_interval_sec=1.0)
    
    frame_processed = 0
    telemetry_events_count = 0
    accident_events_count = 0
    
    try:
        for idx, ts, raw_frame, prep_frame in stream.get_frames():
            frame_processed += 1
            
            telemetry_event, accident_event = engine.process_frame(idx, ts, raw_frame, prep_frame)
            
            if telemetry_event:
                telemetry_events_count += 1
                logger.info(f"[MQTT TELEMETRY] {json.dumps(telemetry_event)}")
                
            if accident_event:
                accident_events_count += 1
                logger.warning(f"[MQTT ACCIDENT ALERT] {json.dumps(accident_event)}")
                
            if max_frames > 0 and frame_processed >= max_frames:
                logger.info(f"Reached max target frames limit ({max_frames}). Halting loop.")
                break

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down edge service...")
    finally:
        stream.release()
        logger.info("==================================================")
        logger.info(f"EDGE SERVICE SUMMARY:")
        logger.info(f"   - Frames Processed: {frame_processed}")
        logger.info(f"   - Telemetry Events Generated: {telemetry_events_count}")
        logger.info(f"   - Accident Alerts Dispatched: {accident_events_count}")
        logger.info("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart City Traffic & Accident Detection Edge Engine")
    parser.add_argument("--source", type=str, default="data/sample_traffic.mp4", help="Video file or RTSP stream URL")
    parser.add_argument("--camera-id", type=str, default="CAM-NORTH-001", help="Camera ID identifier")
    parser.add_argument("--max-frames", type=int, default=50, help="Maximum frames to process (0 for infinite)")
    
    args = parser.parse_args()
    run_edge_pipeline(args.source, args.camera_id, args.max_frames)
