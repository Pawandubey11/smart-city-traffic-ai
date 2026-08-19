import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.heat_map import SpatialTrafficHeatmap

def test_spatial_heatmap():
    print("==================================================")
    print("PHASE 22 SPATIAL TRAFFIC DENSITY HEATMAP TEST")
    print("==================================================")
    
    heatmap = SpatialTrafficHeatmap(grid_size=(8, 8), frame_size=(640, 640))
    
    mock_vehicles = [
        {"track_id": 1, "center": (100, 100)},
        {"track_id": 2, "center": (105, 105)},
        {"track_id": 3, "center": (110, 110)}
    ]
    
    for _ in range(5):
        heatmap.update(mock_vehicles)
        
    norm_matrix = heatmap.get_normalized_heatmap()
    hotspots = heatmap.get_hotspot_cells(threshold=0.50)
    
    print(f"Normalized Heatmap Cell (1, 1) Value: {norm_matrix[1][1]}")
    print(f"Hotspot Cells Identified: {hotspots}")
    
    assert norm_matrix[1][1] == 1.0, "Expected cell (1, 1) to be maximum density hotspot"
    assert len(hotspots) > 0, "Expected at least 1 hotspot cell"
    
    print("\n==================================================")
    print("PHASE 22 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_spatial_heatmap()
