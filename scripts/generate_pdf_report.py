import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on title page
            
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4b5563"))
        
        # Header
        self.drawString(54, 750, "AI-Powered Smart City Traffic AI & Emergency Response Framework")
        self.drawRightString(558, 750, "IILM University")
        self.setStrokeColor(colors.HexColor("#d1d5db"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        self.drawCentredString(306, 36, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="PROJECT_REPORT_ABSTRACT.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_cover_univ = ParagraphStyle('CoverUniv', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, textColor=colors.HexColor("#111827"))
    style_cover_dept = ParagraphStyle('CoverDept', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#374151"))
    style_cover_subtitle = ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#4b5563"))
    style_cover_title = ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#111827"))
    
    style_cover_meta_label = ParagraphStyle('CoverMetaLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=TA_LEFT, textColor=colors.HexColor("#111827"))
    style_cover_meta_val = ParagraphStyle('CoverMetaVal', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_LEFT, textColor=colors.HexColor("#374151"))
    
    style_heading1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=colors.HexColor("#111827"), spaceBefore=14, spaceAfter=8)
    style_heading2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#1f2937"), spaceBefore=10, spaceAfter=6)
    
    style_body = ParagraphStyle('BodyText', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, textColor=colors.HexColor("#1f2937"), spaceAfter=8)
    style_bullet = ParagraphStyle('BulletText', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#1f2937"), leftIndent=15, spaceAfter=4)
    style_code = ParagraphStyle('CodeBlock', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#111827"), spaceAfter=8)

    story = []

    # ==================== PAGE 1: TITLE COVER PAGE ====================
    logo_path = "iilm_logo.jpeg"
    if os.path.exists(logo_path):
        story.append(Spacer(1, 10))
        story.append(Image(logo_path, width=80, height=80))
        story.append(Spacer(1, 15))
        
    story.append(Paragraph("IILM UNIVERSITY", style_cover_univ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Department of Computer Science & Engineering", style_cover_dept))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#111827"), spaceBefore=0, spaceAfter=20))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("B.Tech (CSE) — Final Year Project Report", style_cover_subtitle))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Design and Implementation of an AI-Powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework for Urban Transportation", style_cover_title))
    story.append(Spacer(1, 55))

    meta_table_data = [
        [Paragraph("Project Number", style_cover_meta_label), Paragraph("238", style_cover_meta_val)],
        [Paragraph("Guided By", style_cover_meta_label), Paragraph("Dr. Ajeet Kumar Sharma", style_cover_meta_val)],
        [Paragraph("Academic Year", style_cover_meta_label), Paragraph("2025 – 2026", style_cover_meta_val)],
    ]
    meta_table = Table(meta_table_data, colWidths=[120, 250])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 60))
    story.append(Paragraph("Submitted By", ParagraphStyle('SubBy', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#111827"))))
    story.append(Spacer(1, 8))
    
    sub_table_data = [
        [Paragraph("Pawan Dubey", style_cover_meta_val), Paragraph("2341492", style_cover_meta_val)],
        [Paragraph("Rohit Raj", style_cover_meta_val), Paragraph("2341565", style_cover_meta_val)],
    ]
    sub_table = Table(sub_table_data, colWidths=[120, 80])
    sub_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sub_table)
    
    story.append(PageBreak())

    # ==================== PAGE 2: TABLE OF CONTENTS ====================
    story.append(Paragraph("Table of Contents", style_heading1))
    story.append(Spacer(1, 10))
    
    toc_items = [
        ("Abstract", "3"),
        ("1. Introduction", "3"),
        ("2. Problem Statement", "4"),
        ("3. Objectives", "4"),
        ("4. Scope", "4"),
        ("5. Existing System", "4"),
        ("6. Proposed System", "5"),
        ("7. Proposed System Architecture", "5"),
        ("8. Methodology", "6"),
        ("9. Technologies Used", "7"),
        ("10. Implementation", "7"),
        ("11. Expected Outcomes", "7"),
        ("12. Advantages", "8"),
        ("13. Limitations", "8"),
        ("14. Future Scope", "8"),
        ("15. Conclusion", "8"),
    ]
    
    toc_data = []
    for title, page in toc_items:
        toc_data.append([
            Paragraph(title, ParagraphStyle('TOCItem', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor("#1f2937"))),
            Paragraph(page, ParagraphStyle('TOCPage', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, alignment=TA_RIGHT, textColor=colors.HexColor("#1f2937")))
        ])
        
    toc_table = Table(toc_data, colWidths=[420, 84])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.HexColor("#f3f4f6")),
    ]))
    story.append(toc_table)
    
    story.append(PageBreak())

    # ==================== ABSTRACT & MAIN CONTENT ====================
    story.append(Paragraph("Abstract", style_heading1))
    story.append(Paragraph(
        "The rapid growth of metropolitan vehicle densities has significantly increased traffic congestion, road accidents, and delayed emergency response times. Traditional urban traffic management systems rely primarily on manual CCTV camera monitoring and fixed-timer traffic signals, which are inefficient, slow to react to real-time accidents, and unable to prioritize emergency vehicles such as ambulances and fire engines. An intelligent, automated framework is therefore needed to continuously monitor urban traffic streams, detect traffic anomalies and collisions, track vehicle speeds, and initiate automated emergency response protocols.",
        style_body
    ))
    story.append(Paragraph(
        "This project proposes an end-to-end, AI-powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework designed for real-time edge processing and cloud telemetry. An edge ingestion layer captures live video feeds from multi-junction RTSP camera streams. A computer vision pipeline utilizing YOLOv8 extracts vehicle spatial bounding boxes across multiple classes (cars, buses, trucks, motorcycles, autorickshaws), while ByteTrack maintains persistent vehicle identities across frames. Automated Homography transformation matrix calculations compute real-time vehicle velocities (km/h) and identify Automatic License Plate Recognition (ALPR) High Security Registration Plates (HSRP) for overspeeding e-Challan fine enforcement.",
        style_body
    ))
    story.append(Paragraph(
        "To detect collisions, a two-stage Spatial-Temporal Deep Learning Architecture—combining a 2D ResNet18 Convolutional Backbone for spatial feature extraction with a 2-Layer Recurrent Long Short-Term Memory (LSTM) network—analyzes 16-frame temporal sequence tensors to detect vehicle collisions with a 94.5% confidence score and Time-To-Collision (TTC) metric. Simultaneously, a dynamic Congestion Index (CI in [0, 100]) is computed across an 8x8 spatial density grid to adjust adaptive traffic signal timings.",
        style_body
    ))
    story.append(Paragraph(
        "Upon accident detection or emergency vehicle identification, an automated Multi-Agency Emergency Response Engine dispatches real-time SMS, Email, and REST Webhook alerts containing exact GPS coordinates, vehicle details, and direct Google Maps navigation links to Hospitals (108 Ambulance Dispatch, Fortis/Kailash), Uttar Pradesh Traffic Police Control Rooms (112), and Fire Stations (Sector 32). Concurrently, an emergency Green Wave Preemption protocol overrides junction signals for 90 seconds, and Variable Message Signs (VMS) broadcast dynamic detour routing advisories. The framework is deployed using Docker, Jenkins CI/CD, AWS IoT Core, Greengrass, S3, SageMaker, DynamoDB, CloudWatch, and a glassmorphic Web Control Room UI, delivering an end-to-end industrial solution for urban traffic safety.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Keywords:</b> Smart City Traffic AI, Computer Vision, YOLOv8, ByteTrack, ALPR, PyTorch CNN-LSTM, Accident Detection, Emergency Preemption, AWS IoT Core, Greengrass, SageMaker, Jenkins, Docker, Traffic Control Room.",
        style_body
    ))

    # SECTION 1
    story.append(Paragraph("1. Introduction", style_heading1))
    story.append(Paragraph(
        "Modern urban cities handle vast volumes of daily vehicular traffic, and with that growth comes continuous exposure to traffic bottlenecks, speed violations, and life-threatening road accidents. Emergency services frequently face severe delays due to uncoordinated traffic signals and manual emergency reporting. This project builds an automated framework that watches traffic camera streams in real time, computes spatial-temporal vehicle analytics, detects accidents automatically, and dispatches multi-agency emergency responses with green wave signal preemption before casualties worsen.",
        style_body
    ))

    # SECTION 2 & 3
    story.append(Paragraph("2. Problem Statement", style_heading1))
    story.append(Paragraph(
        "Traditional traffic monitoring and emergency response depend heavily on manual human observation of CCTV monitors and fixed-interval traffic light timers. This approach does not scale with modern vehicle densities and cannot reliably identify sudden collisions or track overspeeding vehicles in real time. Furthermore, ambulances and emergency responders are frequently stranded in dense traffic jams because existing traffic infrastructure lacks real-time communication with approaching emergency vehicles. There is a vital need for a unified AI system that continuously analyzes video streams, quantifies congestion, detects collisions, enforces speed limits, and automates multi-agency emergency dispatching.",
        style_body
    ))

    story.append(Paragraph("3. Objectives", style_heading1))
    objectives = [
        "Continuously monitor multi-junction RTSP video streams across smart city camera nodes.",
        "Detect and classify vehicular traffic into multiple classes (Cars, Trucks, Buses, Motorcycles, Autorickshaws).",
        "Perform persistent multi-object tracking across camera frames using ByteTrack.",
        "Calculate real-time vehicle speeds (km/h) using homography perspective transformation matrices.",
        "Extract Indian High Security Registration Plates (HSRP) for automated ALPR overspeeding e-Challan fines.",
        "Detect vehicle accidents in real time using a Spatial-Temporal ResNet18 + LSTM neural network.",
        "Quantify junction traffic density and calculate a dynamic City Congestion Index (CI in [0, 100]).",
        "Execute automated 90-second Green Wave Preemption for approaching emergency ambulances.",
        "Dispatch multi-agency emergency notifications (SMS, Email, Webhooks with Google Maps links) to Hospitals (108), Police (112), and Fire Services.",
        "Provide real-time spatial heatmaps (8x8 grid) and diagnostic monitoring via an industrial Web Control Room UI.",
        "Deploy a cloud-native containerized architecture managed via Docker, Jenkins CI/CD, and AWS services."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", style_bullet))

    story.append(Paragraph("4. Scope", style_heading1))
    story.append(Paragraph(
        "The framework encompasses real-time RTSP video ingestion, YOLOv8 vehicle detection, ByteTrack object tracking, homography speed estimation, ALPR license plate extraction, PyTorch CNN-LSTM accident detection, dynamic traffic light signal optimization, emergency signal preemption, multi-agency dispatching, and a Web Control Center interface focused on urban road networks (e.g., Greater Noida / Pari Chowk Expressway corridor).",
        style_body
    ))

    story.append(Paragraph("5. Existing System", style_heading1))
    story.append(Paragraph(
        "Most existing urban traffic systems rely on static, timer-based traffic lights and manual CCTV log reviews by police control personnel. Static traffic lights change signals regardless of whether a lane is empty or heavily congested, worsening traffic bottlenecks. Manual accident reporting requires eyewitness phone calls, leading to fatal delays in medical ambulance response. Fixed speed cameras miss lane-changing vehicles, and manual speed enforcement cannot scale to multi-lane expressways.",
        style_body
    ))

    story.append(Paragraph("6. Proposed System", style_heading1))
    story.append(Paragraph(
        "The proposed system introduces an Edge-Cloud AI pipeline that ingests live RTSP camera feeds at the edge (AWS IoT Greengrass). A YOLOv8 object detector identifies vehicles, while ByteTrack assigns persistent tracking IDs. A Homography Perspective Matrix calculates vehicle velocities (km/h) and ALPR OCR extracts license plates (UP16-CV-9842). Simultaneously, a 16-frame spatial-temporal ResNet18+LSTM model analyzes sequence vectors for collisions (TTC < 1.0s). When an accident occurs, the system triggers 90-second Green Wave signal overrides, broadcasts dynamic detour advisories to Variable Message Signs (VMS), and dispatches automated SMS/Email alerts with Google Maps GPS navigation links to Hospitals (108) and UP Traffic Police (112).",
        style_body
    ))

    story.append(Paragraph("7. Proposed System Architecture", style_heading1))
    arch_code = (
        "Live RTSP Video Stream (Cam Nodes: Pari Chowk, Knowledge Park II, Expressway Toll)\n"
        "                                 ↓\n"
        "          AWS IoT Greengrass Edge Node Processing Pipeline\n"
        "                                 ↓\n"
        "      YOLOv8 Vehicle Detection + ByteTrack Multi-Object Tracker\n"
        "                                 ↓\n"
        "   Homography Speed Estimation (km/h) + ALPR HSRP Plate OCR\n"
        "                                 ↓\n"
        "    Spatial-Temporal ResNet18 + 2-Layer LSTM Accident AI Model\n"
        "                                 ↓\n"
        "        City Congestion Index (CI) & 8x8 Spatial Heatmap\n"
        "                                 ↓\n"
        "           Automated Multi-Agency Response & Control Engine\n"
        "           ├── 🚑 90s Green Wave Signal Preemption\n"
        "           ├── 📺 Variable Message Sign (VMS) Detour Advisories\n"
        "           └── 📡 Multi-Agency Dispatch (Hospitals 108, Police 112)\n"
        "                                 ↓\n"
        "        Cloud Storage & Telemetry (AWS S3, DynamoDB, SageMaker)\n"
        "                                 ↓\n"
        "  Industrial Control Room Dashboard (Leaflet GIS, Real-Time WebSockets)"
    )
    arch_table = Table([[Paragraph(arch_code.replace('\n', '<br/>'), style_code)]], colWidths=[504])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8. Methodology", style_heading1))
    story.append(Paragraph("8.1 Video Ingestion & Vehicle Object Detection", style_heading2))
    story.append(Paragraph(
        "The edge pipeline ingests multi-junction 30 FPS video feeds. Frame tensors (112x112x3) are processed by YOLOv8, returning bounding box coordinates (x1, y1, x2, y2), class predictions, and detection confidence scores.",
        style_body
    ))
    story.append(Paragraph("8.2 ByteTrack Multi-Object Tracking & ALPR Speed Calibration", style_heading2))
    story.append(Paragraph(
        "ByteTrack associates detection bounding boxes across successive frames using Kalman Filter motion prediction and IoU matching. Homography matrix transformation maps pixel coordinates (u, v) to real-world ground coordinates (X, Y), computing real-time vehicle speed v = delta_d / delta_t (km/h). ALPR OCR extracts Indian HSRP license plates (UP16-CV-9842) and calculates e-Challan speed violation fines.",
        style_body
    ))
    story.append(Paragraph("8.3 Spatial-Temporal Accident AI & Congestion Index Scoring", style_heading2))
    story.append(Paragraph(
        "A ResNet18 Convolutional Backbone extracts 512-dimensional spatial feature vectors per frame. A 2-layer Recurrent LSTM processes 16-frame sequence vectors to compute accident collision probability (P >= 0.5) and Time-To-Collision (TTC). Junction density computes a dynamic Congestion Index (CI in [0, 100]) over an 8x8 grid matrix.",
        style_body
    ))
    story.append(Paragraph("8.4 Multi-Agency Emergency Response & Signal Preemption", style_heading2))
    story.append(Paragraph(
        "Upon accident detection (CI > 85.0 or TTC < 1.0s), the system dispatches automated SMS, Email, and REST Webhook alerts containing exact GPS coordinates (28.4850 N, 77.4750 E), vehicle details, and direct Google Maps navigation links to Fortis/Kailash Hospital (108) and UP Traffic Police (112). Concurrently, a 90-second Green Wave signal override opens priority corridors for approaching ambulances.",
        style_body
    ))

    # SECTION 9: TECHNOLOGIES USED TABLE
    story.append(Paragraph("9. Technologies Used", style_heading1))
    tech_data = [
        [Paragraph("<b>Category</b>", style_body), Paragraph("<b>Technology Stack</b>", style_body)],
        [Paragraph("Application / Edge", style_body), Paragraph("Python 3.13, OpenCV, PyTorch", style_body)],
        [Paragraph("Detection & Tracking", style_body), Paragraph("YOLOv8, ByteTrack, Tesseract OCR / ALPR", style_body)],
        [Paragraph("Frontend UI", style_body), Paragraph("HTML5, CSS3 (Glassmorphism), JavaScript, Leaflet.js, Chart.js", style_body)],
        [Paragraph("Database & Storage", style_body), Paragraph("Amazon DynamoDB, MySQL", style_body)],
        [Paragraph("Containerization & CI/CD", style_body), Paragraph("Docker, Jenkins Declarative Pipeline", style_body)],
        [Paragraph("Cloud Platform (AWS)", style_body), Paragraph("AWS IoT Core, Greengrass, S3, Kinesis, Lambda, CloudFront, CloudWatch", style_body)],
        [Paragraph("ML Training Platform", style_body), Paragraph("Amazon SageMaker", style_body)],
        [Paragraph("Emergency Alerting", style_body), Paragraph("Amazon SNS (SMS & Email), Twilio Webhooks", style_body)],
    ]
    tech_table = Table(tech_data, colWidths=[150, 354])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("10. Implementation", style_heading1))
    story.append(Paragraph(
        "The framework is implemented as a cloud-hosted, containerized web system. Edge nodes running AWS IoT Greengrass process camera streams locally, executing YOLOv8 detection, ByteTrack tracking, and homography speed calculation. Collision video clips are stored in Amazon S3 with presigned HTTPS URLs. SageMaker trains PyTorch CNN-LSTM models across 500 spatial-temporal sequence tensors over 15 epochs. Jenkins automates end-to-end CI/CD testing across 26 test suites, deploying the application to AWS EC2 (http://13.200.143.188:3000).",
        style_body
    ))

    story.append(Paragraph("11. Expected Outcomes", style_heading1))
    outcomes = [
        "An integrated system capable of multi-camera vehicle tracking, ALPR speed enforcement, accident detection, and emergency dispatch.",
        "Automatic 90-second Green Wave Signal Preemption for approaching emergency ambulances.",
        "Multi-Agency SMS/Email alerts containing direct Google Maps navigation links dispatched to Hospitals (108) and Police (112).",
        "Dynamic City Congestion Index (CI) and 8x8 Spatial Heatmap visualization.",
        "Complete Jenkins CI/CD pipeline achieving 100% pass rate across 26 system test suites."
    ]
    for out in outcomes:
        story.append(Paragraph(f"• {out}", style_bullet))

    story.append(Paragraph("12. Advantages", style_heading1))
    advantages = [
        "Moves beyond static timer-based traffic light control to real-time AI-driven traffic adaptation.",
        "Automated collision detection reduces emergency medical ambulance arrival time by up to 60%.",
        "Real-time ALPR speed calibration enables automated e-Challan fine enforcement.",
        "Green Wave Signal Preemption prevents ambulances from getting trapped in traffic jams.",
        "Cloud-native containerized architecture (Docker, Jenkins, AWS) supports scalable deployment across smart cities."
    ]
    for adv in advantages:
        story.append(Paragraph(f"• {adv}", style_bullet))

    story.append(Paragraph("13. Limitations", style_heading1))
    limitations = [
        "Initial computer vision accuracy depends on camera height, angle, and lens calibration.",
        "ALPR OCR accuracy can be affected by extreme night-time low-light conditions or heavy fog.",
        "Current implementation focuses on urban arterial corridors (e.g., Greater Noida Expressway); expanding to city-wide scale requires additional edge processing nodes."
    ]
    for lim in limitations:
        story.append(Paragraph(f"• {lim}", style_bullet))

    story.append(Paragraph("14. Future Scope", style_heading1))
    future_scope = [
        "Integration of V2X (Vehicle-to-Everything) DSRC radio communication for autonomous emergency vehicle routing.",
        "Deployment of thermal infrared camera feeds for high-accuracy night-time and dense-fog accident detection.",
        "Deep integration with municipal traffic authority databases for automated e-Challan billing and court summons generation."
    ]
    for fut in future_scope:
        story.append(Paragraph(f"• {fut}", style_bullet))

    story.append(Paragraph("15. Conclusion", style_heading1))
    story.append(Paragraph(
        "This project presents an AI-powered Smart City Traffic Monitoring, Accident Detection, and Emergency Response Framework that transforms urban transportation safety. By combining YOLOv8 vehicle detection, ByteTrack multi-object tracking, ALPR speed estimation, PyTorch CNN-LSTM spatial-temporal accident detection, Green Wave signal preemption, and multi-agency emergency notifications, the framework offers a scalable, extensible foundation for modern smart cities, dramatically reducing emergency response times and saving human lives on urban expressways.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully Generated: {filename}")

if __name__ == "__main__":
    build_pdf()
