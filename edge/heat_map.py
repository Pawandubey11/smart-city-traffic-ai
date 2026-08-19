import numpy as np
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SpatialHeatmap")

class SpatialTrafficHeatmap:
    """
    Advanced Spatial Traffic Density & Hotspot Heatmap Engine.
    Divides the camera viewport into an N x N spatial grid and accumulates
    temporal vehicle occupancy to identify city bottleneck hotspots.
    """
    def __init__(self, grid_size: Tuple[int, int] = (8, 8), frame_size: Tuple[int, int] = (640, 640)):
        self.grid_rows, self.grid_cols = grid_size
        self.frame_w, self.frame_h = frame_size
        self.cell_w = self.frame_w / self.grid_cols
        self.cell_h = self.frame_h / self.grid_rows
        self.heatmap_matrix = np.zeros((self.grid_rows, self.grid_cols), dtype=np.float32)

    def update(self, tracked_vehicles: List[Dict[str, Any]]) -> None:
        """Accumulates vehicle position counts into the 2D spatial grid matrix."""
        for v in tracked_vehicles:
            cx, cy = v["center"]
            col = int(min(self.grid_cols - 1, max(0, cx // self.cell_w)))
            row = int(min(self.grid_rows - 1, max(0, cy // self.cell_h)))
            self.heatmap_matrix[row, col] += 1.0

    def get_normalized_heatmap(self) -> List[List[float]]:
        """Returns normalized 0.0 to 1.0 spatial density heatmap matrix."""
        max_val = np.max(self.heatmap_matrix)
        if max_val > 0:
            norm_matrix = self.heatmap_matrix / max_val
        else:
            norm_matrix = self.heatmap_matrix
        return norm_matrix.round(3).tolist()

    def get_hotspot_cells(self, threshold: float = 0.70) -> List[Dict[str, Any]]:
        """Identifies top spatial congestion hotspot coordinates."""
        norm_matrix = self.get_normalized_heatmap()
        hotspots = []
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if norm_matrix[r][c] >= threshold:
                    hotspots.append({
                        "grid_cell": (r, c),
                        "density_score": norm_matrix[r][c],
                        "bbox": [int(c * self.cell_w), int(r * self.cell_h), int((c + 1) * self.cell_w), int((r + 1) * self.cell_h)]
                    })
        return hotspots
