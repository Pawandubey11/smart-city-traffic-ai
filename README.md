# CNN-Based Real-Time Traffic Congestion and Accident Detection System for Smart Cities

Production-grade Smart City AI platform combining Edge Computing (OpenCV, YOLOv8, ByteTrack, PyTorch CNN-LSTM) and AWS Cloud (IoT Greengrass, IoT Core, Kinesis, Lambda, DynamoDB, RDS PostgreSQL, S3, SageMaker, API Gateway, CloudFront, SNS, CloudWatch).

## System Architecture Overview

```
CAMERA -> EDGE DEVICE (Greengrass) -> YOLOv8 + ByteTrack + CNN-LSTM -> AWS IoT CORE -> KINESIS -> LAMBDA
                                                                                               |
                                                                         +---------------------+---------------------+
                                                                         |                     |                     |
                                                                     DynamoDB                 RDS                   S3 (Evidence)
                                                                  (Telemetry)             (App State)                 + SNS Alert
                                                                         |                     |
                                                                         +---------------------+
                                                                                               |
                                                                                          API Gateway -> CloudFront (React Dashboard)
```

## Directory Structure

- `edge/` - Local edge computing AI pipeline (video ingestion, YOLOv8 detection, ByteTrack tracking, traffic density/congestion, accident detection).
- `models/` - Spatial-temporal CNN-LSTM neural network architecture and AWS SageMaker cloud training scripts.
- `cloud/` - AWS Lambda handlers, S3 Data Lake manager, IoT Core provisioner, Greengrass recipe, DynamoDB/RDS schemas, and SNS dispatcher.
- `frontend/` - React 18 control room dashboard with dark-mode glassmorphic aesthetics, Leaflet maps, dynamic metrics, and alerts.
- `config/` - Configuration files for cameras, detection thresholds, and AWS settings.
- `tests/` - Comprehensive automated test suites (Phases 1 through 19).

---

## How to Run & Deploy

### Method A: Running via Docker (Recommended)

To run the complete containerized Edge AI Service in an isolated environment:

```bash
# 1. Build the Docker Container Image
sudo docker build -t smartcity-edge-ai:latest -f edge/Dockerfile .

# 2. Run the Docker Container
sudo docker run -it smartcity-edge-ai:latest
```

---

### Method B: Running Natively on Linux / Ubuntu Host

To run scripts directly inside a Python virtual environment:

```bash
# 1. Clone the repository
git clone https://github.com/Pawandubey11/smart-city-traffic-ai.git
cd smart-city-traffic-ai

# 2. Install System & Python Dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv libgl1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Generate Sample Traffic Video
PYTHONPATH=. python3 data/create_sample_traffic_video.py

# 4. Run Edge AI Computer Vision Pipeline
PYTHONPATH=. python3 edge/main.py --source data/sample_traffic.mp4 --camera-id CAM-NORTH-001

# 5. Run SageMaker Model Trainer
PYTHONPATH=. python3 models/train_sagemaker.py --epochs 3 --batch-size 2
```

---

### Method C: Running the React Dashboard

To launch the Smart City Control Room web dashboard UI:

```bash
cd frontend
npm install
npm start
```
Access the web dashboard at `http://localhost:3000`.

---

## Automated Test Suites

Run any phase verification test:

```bash
PYTHONPATH=. python3 tests/test_phase7_local_prototype.py
PYTHONPATH=. python3 tests/test_phase8_s3.py
PYTHONPATH=. python3 tests/test_phase9_sagemaker.py
PYTHONPATH=. python3 tests/test_phase15_api.py
```
