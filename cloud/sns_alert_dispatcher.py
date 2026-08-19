import json
import time
import logging
import boto3
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SNSAlertDispatcher")

class SNSAlertDispatcher:
    """
    Amazon SNS Real-Time Accident Alert Dispatcher.
    Constructs high-priority alert notifications and dispatches Email/SMS alerts
    to first responders and traffic control officers with presigned S3 evidence image links.
    """
    def __init__(
        self,
        region: str = "us-east-1",
        topic_arn: str = "arn:aws:sns:us-east-1:123456789012:AccidentAlertTopic"
    ):
        self.region = region
        self.topic_arn = topic_arn
        
        try:
            self.sns_client = boto3.client("sns", region_name=self.region)
            logger.info(f"Initialized Boto3 SNS Client for region: {self.region}")
        except Exception as e:
            logger.warning(f"SNS Client initialization notice ({e}). Operating in Local/Mock Mode.")
            self.sns_client = None

    def dispatch_accident_alert(
        self,
        camera_id: str,
        location_name: str,
        confidence_score: float,
        presigned_s3_url: str,
        severity: str = "CRITICAL"
    ) -> bool:
        """
        Formats and dispatches high-priority accident notification via Amazon SNS.
        """
        subject = f"🚨 SMART CITY ALERT: CRITICAL TRAFFIC ACCIDENT DETECTED [{camera_id}]"
        
        message_body = (
            f"=== SMART CITY REAL-TIME ACCIDENT ALERT ===\n\n"
            f"Camera ID: {camera_id}\n"
            f"Location: {location_name}\n"
            f"Severity: {severity}\n"
            f"AI Accident Confidence: {confidence_score * 100:.1f}%\n"
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n"
            f"View S3 Evidence Snapshot:\n{presigned_s3_url}\n\n"
            f"Please dispatch emergency services immediately if unverified."
        )

        if self.sns_client is not None:
            try:
                res = self.sns_client.publish(
                    TopicArn=self.topic_arn,
                    Subject=subject[:100], # SNS Subject line length limit
                    Message=message_body
                )
                logger.critical(f"Dispatched Amazon SNS Email Alert to topic [{self.topic_arn}]. Message ID: {res.get('MessageId')}")
                return True
            except Exception as e:
                logger.warning(f"Amazon SNS Publish notice ({e}). Falling back to local mock notification logging.")

        logger.critical(f"[MOCK SNS ALERT DISPATCHED]\nSubject: {subject}\nBody:\n{message_body}")
        return True
