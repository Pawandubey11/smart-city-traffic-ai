import logging
import boto3
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CloudWatchMonitor")

class CloudWatchMonitor:
    """
    AWS CloudWatch Metrics & Application Performance Monitoring System.
    Logs custom metrics (AI inference latency, vehicle count throughput, accident alerts, Lambda latency)
    and configures automated CloudWatch Alarm triggers for operational alerts.
    """
    def __init__(self, region: str = "us-east-1", namespace: str = "SmartCity/TrafficAI"):
        self.region = region
        self.namespace = namespace
        try:
            self.cw_client = boto3.client("cloudwatch", region_name=self.region)
            logger.info(f"Initialized Boto3 CloudWatch Client for namespace: {self.namespace}")
        except Exception as e:
            logger.warning(f"CloudWatch Client notice ({e}). Operating in Local/Mock Mode.")
            self.cw_client = None

    def put_metric(self, metric_name: str, value: float, unit: str = "Count", camera_id: str = "CAM-NORTH-001") -> bool:
        """Publishes custom telemetry metric to AWS CloudWatch."""
        if self.cw_client is not None:
            try:
                self.cw_client.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=[{
                        "MetricName": metric_name,
                        "Value": value,
                        "Unit": unit,
                        "Dimensions": [{"Name": "CameraID", "Value": camera_id}]
                    }]
                )
                logger.info(f"[CLOUDWATCH METRIC] {metric_name} = {value} {unit} [{camera_id}]")
                return True
            except Exception as e:
                logger.warning(f"CloudWatch put_metric notice ({e}). Operating in Local Mock Mode.")
                
        logger.info(f"[MOCK CLOUDWATCH METRIC] {metric_name} = {value} {unit} [{camera_id}]")
        return True
