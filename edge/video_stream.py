import cv2
import time
import logging
import numpy as np
from typing import Generator, Tuple, Optional, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("VideoStreamReader")

class VideoStreamReader:
    """
    Modular OpenCV video ingestion pipeline for RTSP streams, video files, or camera devices.
    Includes frame resizing, ROI masking, frame skipping/sampling, and error recovery.
    """
    def __init__(
        self,
        source: str,
        target_size: Tuple[int, int] = (640, 640),
        frame_sample_rate: int = 1,
        roi_polygon: Optional[List[List[int]]] = None,
        max_reconnect_attempts: int = 5
    ):
        self.source = source
        self.target_size = target_size
        self.frame_sample_rate = frame_sample_rate
        self.roi_polygon = roi_polygon
        self.max_reconnect_attempts = max_reconnect_attempts
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_file = not (str(source).isdigit() or str(source).startswith("rtsp://") or str(source).startswith("http://"))
        self._initialize_stream()

    def _initialize_stream(self) -> None:
        """Initializes OpenCV VideoCapture object."""
        if str(self.source).isdigit():
            source_arg = int(self.source)
        else:
            source_arg = self.source
            
        logger.info(f"Connecting to video source: {self.source}")
        self.cap = cv2.VideoCapture(source_arg)
        
        if not self.cap.isOpened():
            logger.error(f"Failed to open video source: {self.source}")
            raise ValueError(f"Could not open video stream: {self.source}")
            
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if self.is_file else -1
        
        logger.info(f"Stream initialized successfully: {width}x{height} @ {fps:.2f} FPS | Total Frames: {total_frames}")

    def apply_roi_mask(self, frame: np.ndarray) -> np.ndarray:
        """Applies Region-Of-Interest (ROI) polygon mask to frame if defined."""
        if not self.roi_polygon or len(self.roi_polygon) < 3:
            return frame
            
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        pts = np.array(self.roi_polygon, np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
        
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        return masked_frame

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocesses frame for ML model input:
        1. Apply ROI mask
        2. Resize to target dimension (e.g. 640x640)
        """
        masked = self.apply_roi_mask(frame)
        resized = cv2.resize(masked, self.target_size, interpolation=cv2.INTER_LINEAR)
        return resized

    def get_frames(self) -> Generator[Tuple[int, float, np.ndarray, np.ndarray], None, None]:
        """
        Generator function yielding (frame_index, timestamp_ms, raw_frame, preprocessed_frame).
        Handles reconnect attempts for stream interruptions.
        """
        frame_idx = 0
        reconnect_count = 0
        
        while True:
            if not self.cap or not self.cap.isOpened():
                if reconnect_count >= self.max_reconnect_attempts:
                    logger.error("Max reconnect attempts reached. Stopping stream.")
                    break
                logger.warning(f"Stream disconnected. Reconnecting attempt {reconnect_count + 1}/{self.max_reconnect_attempts}...")
                time.sleep(2)
                self._initialize_stream()
                reconnect_count += 1
                continue

            ret, raw_frame = self.cap.read()
            if not ret or raw_frame is None:
                if self.is_file:
                    logger.info("End of video file reached.")
                    break
                else:
                    logger.warning("Blank frame received or stream buffer empty.")
                    reconnect_count += 1
                    time.sleep(0.5)
                    continue

            reconnect_count = 0 # Reset counter on successful read
            frame_idx += 1

            if frame_idx % self.frame_sample_rate != 0:
                continue

            timestamp_ms = time.time() * 1000.0
            preprocessed_frame = self.preprocess_frame(raw_frame)

            yield frame_idx, timestamp_ms, raw_frame, preprocessed_frame

    def release(self) -> None:
        """Releases video capture resources."""
        if self.cap:
            self.cap.release()
            logger.info("Video stream resources released successfully.")
