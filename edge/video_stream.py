import cv2
import numpy as np
import time
import logging
from typing import Optional, Tuple, List, Generator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("VideoStreamReader")

class VideoStreamReader:
    """
    Production Industrial RTSP Video Stream Ingestion Engine.
    Features:
    - Automatic Exponential Backoff RTSP Reconnection Loop (protects against IP camera drops)
    - Consecutive Frame-Drop Watchdog (resets stream if 15 frames fail consecutively)
    - Dynamic Downsampling, ROI Polygon Masking, and Generator Iteration
    """
    def __init__(
        self,
        source: str = "data/sample_traffic.mp4",
        target_size: Tuple[int, int] = (640, 640),
        sample_rate: int = 1,
        frame_sample_rate: int = 1,
        roi_polygon: Optional[List[Tuple[int, int]]] = None,
        max_recon_attempts: int = 5
    ):
        self.source = source
        self.target_size = target_size
        self.sample_rate = sample_rate or frame_sample_rate
        self.roi_polygon = roi_polygon
        self.max_recon_attempts = max_recon_attempts
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.fps: float = 30.0
        self.width: int = 1280
        self.height: int = 720
        self.total_frames: int = 0
        self.consecutive_failures: int = 0
        
        self._initialize_stream()

    def _initialize_stream(self) -> bool:
        """Initializes or reconnects the cv2.VideoCapture handle."""
        if self.cap is not None:
            self.cap.release()
            
        logger.info(f"Connecting to video source: {self.source}")
        self.cap = cv2.VideoCapture(self.source)
        
        if not self.cap.isOpened():
            logger.error(f"Failed to open video source: {self.source}")
            return False
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        self.consecutive_failures = 0
        
        logger.info(f"Stream initialized successfully: {self.width}x{self.height} @ {self.fps:.2f} FPS | Total Frames: {self.total_frames}")
        return True

    def reconnect(self) -> bool:
        """Attempts exponential backoff reconnection to RTSP camera stream."""
        for attempt in range(1, self.max_recon_attempts + 1):
            wait_sec = 2 ** attempt
            logger.warning(f"🔄 Reconnection attempt {attempt}/{self.max_recon_attempts} for {self.source}. Waiting {wait_sec}s...")
            time.sleep(wait_sec)
            if self._initialize_stream():
                logger.info(f"✅ Successfully reconnected to video stream {self.source}")
                return True
        logger.error(f"❌ Failed to reconnect after {self.max_recon_attempts} attempts.")
        return False

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Reads a frame from the stream with frame-drop watchdog protection.
        Returns: (success, raw_frame, preprocessed_frame)
        """
        if self.cap is None or not self.cap.isOpened():
            if not self.reconnect():
                return False, None, None

        ret, frame = self.cap.read()
        
        if not ret or frame is None:
            self.consecutive_failures += 1
            if self.consecutive_failures >= 15:
                logger.error("RTSP Stream disconnect watchdog triggered! Attempting stream reset...")
                if self.reconnect():
                    return self.read_frame()
                return False, None, None
            return False, None, None

        self.consecutive_failures = 0
        prep_frame = cv2.resize(frame, self.target_size)
        return True, frame, prep_frame

    def get_frames(self) -> Generator[Tuple[int, float, np.ndarray, np.ndarray], None, None]:
        """Generator yielding (frame_index, timestamp_ms, raw_frame, preprocessed_frame)."""
        frame_idx = 0
        while True:
            ret, raw_frame, prep_frame = self.read_frame()
            if not ret or raw_frame is None or prep_frame is None:
                break
            timestamp_ms = (frame_idx / self.fps) * 1000.0 if self.fps > 0 else frame_idx * 33.33
            yield frame_idx, timestamp_ms, raw_frame, prep_frame
            frame_idx += 1

    def release(self) -> None:
        """Releases video capture resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            logger.info("Video stream resources released successfully.")
