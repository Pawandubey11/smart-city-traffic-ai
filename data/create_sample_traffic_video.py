import cv2
import numpy as np
import os

def generate_sample_traffic_video(output_path: str = "data/sample_traffic.mp4", duration_sec: int = 10, fps: int = 30):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    width, height = 1280, 720
    total_frames = duration_sec * fps
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Define simulated vehicles: [x, y, speed_x, speed_y, w, h, color]
    vehicles = [
        {"id": 1, "x": 100, "y": 250, "vx": 8, "vy": 0, "w": 80, "h": 40, "color": (0, 0, 255)},   # Red car
        {"id": 2, "x": 300, "y": 250, "vx": 7, "vy": 0, "w": 90, "h": 45, "color": (255, 0, 0)},   # Blue car
        {"id": 3, "x": 50,  "y": 400, "vx": 12, "vy": 0, "w": 120, "h": 55, "color": (0, 255, 0)},  # Green truck
        {"id": 4, "x": 500, "y": 400, "vx": 6, "vy": 0, "w": 70, "h": 35, "color": (0, 255, 255)}, # Yellow car
        {"id": 5, "x": 200, "y": 550, "vx": 10, "vy": 0, "w": 85, "h": 42, "color": (255, 0, 255)}  # Purple car
    ]
    
    print(f"Generating synthetic traffic video: {output_path} ({width}x{height} @ {fps} FPS)...")
    
    for f in range(total_frames):
        # Dark gray road background with lane markings
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50
        
        # Draw road lanes
        cv2.rectangle(frame, (0, 180), (width, 650), (80, 80, 80), -1) # Asphalt road
        cv2.line(frame, (0, 330), (width, 330), (255, 255, 255), 2)  # Lane divider 1
        cv2.line(frame, (0, 480), (width, 480), (255, 255, 255), 2)  # Lane divider 2
        
        # Simulate an accident at frame 150 between vehicle 1 and vehicle 2
        if f > 140 and f < 220:
            vehicles[0]["vx"] = max(0, vehicles[0]["vx"] - 0.5) # Sudden braking
            vehicles[1]["vx"] = max(0, vehicles[1]["vx"] - 0.4)
            if abs(vehicles[0]["x"] - vehicles[1]["x"]) < 40:
                vehicles[0]["vx"] = 0
                vehicles[1]["vx"] = 0

        # Update and draw vehicles
        for v in vehicles:
            v["x"] += v["vx"]
            v["y"] += v["vy"]
            
            # Wrap around road
            if v["x"] > width:
                v["x"] = -v["w"]
                
            x, y, w, h = int(v["x"]), int(v["y"]), v["w"], v["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), v["color"], -1)
            cv2.putText(frame, f"Vehicle #{v['id']}", (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        out.write(frame)
        
    out.release()
    print(f"Successfully generated sample traffic video at {output_path}")

if __name__ == "__main__":
    generate_sample_traffic_video()
