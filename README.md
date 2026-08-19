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

- `edge/` - Local edge computing AI pipeline (capture, vehicle detection, tracking, traffic metrics, accident detection).
- `models/` - Spatial-temporal CNN-LSTM neural network architecture and training scripts.
- `cloud/` - AWS Lambda handlers, CloudFormation/SAM infrastructure templates, SQL schemas, and IoT scripts.
- `frontend/` - React control dashboard with interactive Leaflet maps, dynamic metrics, and alerts.
- `config/` - System configuration files for cameras, detection thresholds, and AWS settings.
- `tests/` - Automated unit and integration test suites.

## Getting Started

### Prerequisites

- Python 3.10+
- PyTorch & OpenCV
- Docker Desktop
- AWS CLI configured

### Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
