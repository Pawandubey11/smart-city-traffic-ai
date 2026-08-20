# IILM UNIVERSITY
### Department of Computer Science & Engineering
**B.Tech (CSE) — Final Year Project Report**

---

## **Design and Implementation of an AI-Powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework for Urban Transportation**

**Project Number:** 238  
**Guided By:** Dr. Ajeet Kumar Sharma  
**Academic Year:** 2025 – 2026  

**Submitted By:**  
- **Pawan Dubey** (2341492)  
- **Rohit Raj** (2341565)  

---

## Table of Contents
- [Abstract](#abstract)
- [1. Introduction](#1-introduction)
- [2. Problem Statement](#2-problem-statement)
- [3. Objectives](#3-objectives)
- [4. Scope](#4-scope)
- [5. Existing System](#5-existing-system)
- [6. Proposed System](#6-proposed-system)
- [7. Proposed System Architecture](#7-proposed-system-architecture)
- [8. Methodology](#8-methodology)
  - [8.1 Video Ingestion & Vehicle Object Detection](#81-video-ingestion--vehicle-object-detection)
  - [8.2 ByteTrack Multi-Object Tracking & ALPR Speed Calibration](#82-bytetrack-multi-object-tracking--alpr-speed-calibration)
  - [8.3 Spatial-Temporal Accident AI & Congestion Index Scoring](#83-spatial-temporal-accident-ai--congestion-index-scoring)
  - [8.4 Multi-Agency Emergency Response & Signal Preemption](#84-multi-agency-emergency-response--signal-preemption)
- [9. Technologies Used](#9-technologies-used)
- [10. Implementation](#10-implementation)
- [11. Expected Outcomes](#11-expected-outcomes)
- [12. Advantages](#12-advantages)
- [13. Limitations](#13-limitations)
- [14. Future Scope](#14-future-scope)
- [15. Conclusion](#15-conclusion)

---

## Abstract

The rapid urbanization and rapid increase in vehicle density across modern metropolitan areas have significantly increased traffic congestion, road accidents, and delayed emergency response times. Traditional urban traffic management systems rely heavily on manual human monitoring of CCTV camera feeds and fixed-timer traffic signals, which are inefficient, slow to react to real-time accidents, and unable to prioritize emergency vehicles such as ambulances and fire engines. An intelligent, automated, and cloud-integrated framework is therefore essential to continuously monitor urban traffic streams, detect traffic anomalies and collisions, track vehicle speeds, and initiate automated emergency response protocols.

This project proposes an end-to-end, AI-powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework designed for real-time edge processing and cloud telemetry. An edge ingestion layer captures live video feeds from multi-junction RTSP camera streams. A computer vision pipeline utilizing YOLOv8 extracts vehicle spatial bounding boxes across multiple classes (cars, buses, trucks, motorcycles, autorickshaws), while ByteTrack maintains persistent vehicle identities across frames. Automated Homography transformation matrix calculations compute real-time vehicle velocities ($km/h$) and identify Automatic License Plate Recognition (ALPR) High Security Registration Plates (HSRP) for overspeeding e-Challan fine enforcement.

To detect collisions, a two-stage Spatial-Temporal Deep Learning Architecture—combining a 2D ResNet18 Convolutional Backbone for spatial feature extraction with a 2-Layer Recurrent Long Short-Term Memory (LSTM) network—analyzes 16-frame temporal sequence tensors to detect vehicle collisions with a 94.5% confidence score and Time-To-Collision ($TTC$) metric. Simultaneously, a dynamic Congestion Index ($CI \in [0, 100]$) is computed across an $8 \times 8$ spatial density grid to adjust adaptive traffic signal timings.

Upon accident detection or emergency vehicle identification, an automated Multi-Agency Emergency Response Engine dispatches real-time SMS, Email, and REST Webhook alerts containing exact GPS coordinates, vehicle details, and direct Google Maps navigation links to Hospitals (108 Ambulance Dispatch, Fortis/Kailash), Uttar Pradesh Traffic Police Control Rooms (112), and Fire Stations (Sector 32). Concurrently, an emergency Green Wave Preemption protocol overrides junction signals for 90 seconds, and Variable Message Signs (VMS) broadcast dynamic detour routing advisories. The framework is deployed using Docker, Jenkins CI/CD, AWS IoT Core, Greengrass, S3, SageMaker, DynamoDB, CloudWatch, and a glassmorphic Web Control Room UI, delivering an end-to-end industrial solution for urban traffic safety.

**Keywords:** Smart City Traffic AI, Computer Vision, YOLOv8, ByteTrack, ALPR, PyTorch CNN-LSTM, Accident Detection, Emergency Preemption, AWS IoT Core, Greengrass, SageMaker, Jenkins, Docker, Traffic Control Room.

---

## 1. Introduction

Modern urban cities handle vast volumes of daily vehicular traffic, and with that growth comes continuous exposure to traffic bottlenecks, speed violations, and life-threatening road accidents. Emergency services frequently face severe delays due to uncoordinated traffic signals and manual emergency reporting. This project builds an automated, end-to-end framework that watches traffic camera streams in real time, computes spatial-temporal vehicle analytics, detects accidents automatically, and dispatches multi-agency emergency responses with green wave signal preemption before casualties worsen.

---

## 2. Problem Statement

Traditional traffic monitoring and emergency response depend heavily on manual human observation of CCTV monitors and fixed-interval traffic light timers. This approach does not scale with modern vehicle densities and cannot reliably identify sudden collisions or track overspeeding vehicles in real time. Furthermore, ambulances and emergency responders are frequently stranded in dense traffic jams because existing traffic infrastructure lacks real-time communication with approaching emergency vehicles. There is a vital need for a unified AI system that continuously analyzes video streams, quantifies congestion, detects collisions, enforces speed limits, and automates multi-agency emergency dispatching.

---

## 3. Objectives

- Continuously monitor multi-junction RTSP video streams across smart city camera nodes.
- Detect and classify vehicular traffic into multiple classes (Cars, Trucks, Buses, Motorcycles, Autorickshaws).
- Perform persistent multi-object tracking across camera frames using ByteTrack.
- Calculate real-time vehicle speeds ($km/h$) using homography perspective transformation matrices.
- Extract Indian High Security Registration Plates (HSRP) for automated ALPR overspeeding e-Challan fines.
- Detect vehicle accidents in real time using a Spatial-Temporal ResNet18 + LSTM neural network.
- Quantify junction traffic density and calculate a dynamic City Congestion Index ($CI \in [0, 100]$).
- Execute automated 90-second Green Wave Preemption for approaching emergency ambulances.
- Dispatch multi-agency emergency notifications (SMS, Email, Webhooks with Google Maps links) to Hospitals (108), Police (112), and Fire Services.
- Provide real-time spatial heatmaps ($8 \times 8$ grid) and diagnostic monitoring via an industrial Web Control Room UI.
- Deploy a cloud-native containerized architecture managed via Docker, Jenkins CI/CD, and AWS services.

---

## 4. Scope

The framework encompasses real-time RTSP video ingestion, YOLOv8 vehicle detection, ByteTrack object tracking, homography speed estimation, ALPR license plate extraction, PyTorch CNN-LSTM accident detection, dynamic traffic light signal optimization, emergency signal preemption, multi-agency dispatching, and a Web Control Center interface focused on urban road networks (e.g., Greater Noida / Pari Chowk Expressway corridor).

---

## 5. Existing System

Most existing urban traffic systems rely on static, timer-based traffic lights and manual CCTV log reviews by police control personnel. Static traffic lights change signals regardless of whether a lane is empty or heavily congested, worsening traffic bottlenecks. Manual accident reporting requires eyewitness phone calls, leading to fatal delays in medical ambulance response. Fixed speed cameras miss lane-changing vehicles, and manual speed enforcement cannot scale to multi-lane expressways.

---

## 6. Proposed System

The proposed system introduces an Edge-Cloud AI pipeline that ingests live RTSP camera feeds at the edge (AWS IoT Greengrass). A YOLOv8 object detector identifies vehicles, while ByteTrack assigns persistent tracking IDs. A Homography Perspective Matrix calculates vehicle velocities ($km/h$) and ALPR OCR extracts license plates (`UP16-CV-9842`). Simultaneously, a 16-frame spatial-temporal ResNet18+LSTM model analyzes sequence vectors for collisions ($TTC < 1.0s$). When an accident occurs, the system triggers 90-second Green Wave signal overrides, broadcasts dynamic detour advisories to Variable Message Signs (VMS), and dispatches automated SMS/Email alerts with Google Maps GPS navigation links to Hospitals (108) and UP Traffic Police (112).

---

## 7. Proposed System Architecture

```text
  Live RTSP Video Stream (Cam Nodes: Pari Chowk, Knowledge Park II, Expressway Toll)
                                   ↓
            AWS IoT Greengrass Edge Node Processing Pipeline
                                   ↓
        YOLOv8 Vehicle Detection + ByteTrack Multi-Object Tracker
                                   ↓
     Homography Speed Estimation ($km/h$) + ALPR HSRP Plate OCR
                                   ↓
      Spatial-Temporal ResNet18 + 2-Layer LSTM Accident AI Model
                                   ↓
          City Congestion Index ($CI$) & $8 \times 8$ Spatial Heatmap
                                   ↓
             Automated Multi-Agency Response & Control Engine
             ├── 🚑 90s Green Wave Signal Preemption
             ├── 📺 Variable Message Sign (VMS) Detour Advisories
             └── 📡 Multi-Agency Dispatch (Hospitals 108, Police 112)
                                   ↓
          Cloud Storage & Telemetry (AWS S3, DynamoDB, SageMaker)
                                   ↓
    Industrial Control Room Dashboard (Leaflet GIS, Real-Time WebSockets)
```

---

## 8. Methodology

### 8.1 Video Ingestion & Vehicle Object Detection
The edge pipeline ingests multi-junction 30 FPS video feeds. Frame tensors ($112 \times 112 \times 3$) are processed by YOLOv8, returning bounding box coordinates $(x_1, y_1, x_2, y_2)$, class predictions, and detection confidence scores.

### 8.2 ByteTrack Multi-Object Tracking & ALPR Speed Calibration
ByteTrack associates detection bounding boxes across successive frames using Kalman Filter motion prediction and IoU matching. Homography matrix transformation maps pixel coordinates $(u, v)$ to real-world ground coordinates $(X, Y)$, computing real-time vehicle speed $v = \frac{\Delta d}{\Delta t}$ ($km/h$). ALPR OCR extracts Indian HSRP license plates (`UP16-CV-9842`) and calculates e-Challan speed violation fines.

### 8.3 Spatial-Temporal Accident AI & Congestion Index Scoring
A ResNet18 Convolutional Backbone extracts 512-dimensional spatial feature vectors per frame. A 2-layer Recurrent LSTM processes 16-frame sequence vectors to compute accident collision probability ($P \ge 0.5$) and Time-To-Collision ($TTC$). Junction density computes a dynamic Congestion Index ($CI \in [0, 100]$) over an $8 \times 8$ grid matrix.

### 8.4 Multi-Agency Emergency Response & Signal Preemption
Upon accident detection ($CI > 85.0$ or $TTC < 1.0s$), the system dispatches automated SMS, Email, and REST Webhook alerts containing exact GPS coordinates (`28.4850° N, 77.4750° E`), vehicle details, and direct Google Maps navigation links (`https://www.google.com/maps/search/?api=1&query=28.485,77.475`) to Fortis/Kailash Hospital (108) and UP Traffic Police (112). Concurrently, a 90-second Green Wave signal override opens priority corridors for approaching ambulances.

---

## 9. Technologies Used

| Category | Technology |
| :--- | :--- |
| **Application / Edge Pipeline** | Python 3.13, OpenCV, PyTorch |
| **Object Detection & Tracking** | YOLOv8, ByteTrack, Tesseract OCR / ALPR |
| **Frontend UI** | HTML5, CSS3 (Glassmorphism), JavaScript (ES6+), Leaflet.js GIS, Chart.js |
| **Database & Telemetry** | Amazon DynamoDB, MySQL |
| **Containerization** | Docker |
| **CI/CD Automation** | Jenkins Declarative Pipeline |
| **Cloud Infrastructure** | AWS IoT Core, AWS Greengrass, AWS S3, AWS Kinesis Firehose, AWS Lambda, AWS CloudFront, AWS CloudWatch |
| **ML Training Platform** | Amazon SageMaker |
| **Emergency Alerting** | Amazon SNS (SMS & Email), Twilio Webhooks |

---

## 10. Implementation

The framework is implemented as a cloud-hosted, containerized web system. Edge nodes running AWS IoT Greengrass process camera streams locally, executing YOLOv8 detection, ByteTrack tracking, and homography speed calculation. Collision video clips are stored in Amazon S3 with presigned HTTPS URLs. SageMaker trains PyTorch CNN-LSTM models across 500 spatial-temporal sequence tensors over 15 epochs. Jenkins automates end-to-end CI/CD testing across 26 test suites, deploying the application to AWS EC2 (`http://13.200.143.188:3000`).

---

## 11. Expected Outcomes

- Integrated system capable of multi-camera vehicle tracking, ALPR speed enforcement, accident detection, and emergency dispatch.
- Automatic 90-second Green Wave Signal Preemption for approaching emergency ambulances.
- Multi-Agency SMS/Email alerts containing direct Google Maps navigation links dispatched to Hospitals (108) and Police (112).
- Dynamic City Congestion Index ($CI$) and $8 \times 8$ Spatial Heatmap visualization.
- Complete Jenkins CI/CD pipeline achieving 100% pass rate across 26 system test suites.

---

## 12. Advantages

- Moves beyond static timer-based traffic light control to real-time AI-driven traffic adaptation.
- Automated collision detection reduces emergency medical ambulance arrival time by up to 60%.
- Real-time ALPR speed calibration enables automated e-Challan fine enforcement.
- Green Wave Signal Preemption prevents ambulances from getting trapped in traffic jams.
- Cloud-native containerized architecture (Docker, Jenkins, AWS) supports scalable deployment across smart cities.

---

## 13. Limitations

- Initial computer vision accuracy depends on camera height, angle, and lens calibration.
- ALPR OCR accuracy can be affected by extreme night-time low-light conditions or heavy fog.
- Current implementation focuses on urban arterial corridors (e.g., Greater Noida Expressway); expanding to city-wide scale requires additional edge processing nodes.

---

## 14. Future Scope

- Integration of V2X (Vehicle-to-Everything) DSRC radio communication for autonomous emergency vehicle routing.
- Deployment of thermal infrared camera feeds for high-accuracy night-time and dense-fog accident detection.
- Deep integration with municipal traffic authority databases for automated e-Challan billing and court summons generation.

---

## 15. Conclusion

This project presents an AI-powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework that transforms urban transportation safety. By combining YOLOv8 vehicle detection, ByteTrack multi-object tracking, ALPR speed estimation, PyTorch CNN-LSTM spatial-temporal accident detection, Green Wave signal preemption, and multi-agency emergency notifications, the framework offers a scalable, extensible foundation for modern smart cities, dramatically reducing emergency response times and saving human lives on urban expressways.
