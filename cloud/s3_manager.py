import os
import time
import logging
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("S3Manager")

class S3DataLakeManager:
    """
    AWS S3 Data Lake & Evidence Storage Manager.
    Handles bucket creation, folder structure initialization, evidence snapshot uploads,
    presigned URL generation for dashboard access, and model artifact lifecycle management.
    """
    def __init__(
        self,
        region: str = "us-east-1",
        evidence_bucket: str = "smart-city-traffic-evidence-demo",
        datalake_bucket: str = "smart-city-traffic-datalake-demo"
    ):
        self.region = region
        self.evidence_bucket = evidence_bucket
        self.datalake_bucket = datalake_bucket
        
        # Initialize Boto3 S3 Client
        try:
            self.s3_client = boto3.client("s3", region_name=self.region)
            logger.info(f"Initialized Boto3 S3 Client for region: {self.region}")
        except Exception as e:
            logger.warning(f"Boto3 S3 Client initialization notice ({e}). Client will operate in mock/offline mode if credentials are missing.")
            self.s3_client = None

    def initialize_buckets(self) -> bool:
        """
        Provisions S3 Data Lake and Evidence buckets with Block Public Access and encryption.
        Creates standard folder prefixes.
        """
        if self.s3_client is None:
            logger.warning("Mock Mode: Skipping actual AWS S3 provisioning API calls.")
            return True
            
        for bucket in [self.evidence_bucket, self.datalake_bucket]:
            try:
                if self.region == "us-east-1":
                    self.s3_client.create_bucket(Bucket=bucket)
                else:
                    self.s3_client.create_bucket(
                        Bucket=bucket,
                        CreateBucketConfiguration={"LocationConstraint": self.region}
                    )
                logger.info(f"Successfully created S3 bucket: {bucket}")
                
                # Enable default Server-Side Encryption (AES256)
                self.s3_client.put_bucket_encryption(
                    Bucket=bucket,
                    ServerSideEncryptionConfiguration={
                        "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
                    }
                )
                
                # Block Public Access
                self.s3_client.put_public_access_block(
                    Bucket=bucket,
                    PublicAccessBlockConfiguration={
                        "BlockPublicAcls": True,
                        "IgnorePublicAcls": True,
                        "BlockPublicPolicy": True,
                        "RestrictPublicBuckets": True
                    }
                )
            except ClientError as e:
                code = e.response["Error"]["Code"]
                if code in ["BucketAlreadyOwnedByYou", "BucketAlreadyExists"]:
                    logger.info(f"S3 Bucket already exists and owned by you: {bucket}")
                elif code == "NotSignedUp":
                    logger.warning(f"AWS Account notice ({code}): S3 service not active on current AWS credentials. Operating in Local/Mock S3 Data Lake Mode.")
                    self.s3_client = None
                    break
                else:
                    logger.error(f"Failed to create S3 bucket {bucket}: {e}")
                    self.s3_client = None
                    break
            except Exception as e:
                logger.warning(f"AWS S3 Connection error ({e}). Operating in Local/Mock S3 Data Lake Mode.")
                self.s3_client = None
                break

        if self.s3_client is None:
            # Local mock storage initialization
            os.makedirs(f"data/s3_mock/{self.evidence_bucket}", exist_ok=True)
            os.makedirs(f"data/s3_mock/{self.datalake_bucket}", exist_ok=True)
            prefixes = ["raw/", "processed/", "annotations/", "models/", "predictions/", "snapshots/", "logs/"]
            for p in prefixes:
                os.makedirs(f"data/s3_mock/{self.datalake_bucket}/{p}", exist_ok=True)
            logger.info("Initialized Local S3 Data Lake Storage at data/s3_mock/")
                
        return True

    def upload_accident_evidence(
        self,
        local_file_path: str,
        camera_id: str,
        timestamp_ms: int
    ) -> Optional[str]:
        """
        Uploads local snapshot/clip to the Evidence S3 bucket.
        Key Format: accidents/{camera_id}/{date}/accident_{timestamp}.jpg
        Returns S3 Object Key if successful.
        """
        if not os.path.exists(local_file_path):
            logger.error(f"Local evidence file not found: {local_file_path}")
            return None
            
        file_name = os.path.basename(local_file_path)
        date_str = time.strftime("%Y-%m-%d")
        s3_key = f"accidents/{camera_id}/{date_str}/{file_name}"
        
        if self.s3_client is None:
            mock_dest = f"data/s3_mock/{self.evidence_bucket}/{s3_key}"
            os.makedirs(os.path.dirname(mock_dest), exist_ok=True)
            with open(local_file_path, "rb") as src, open(mock_dest, "wb") as dst:
                dst.write(src.read())
            logger.info(f"[MOCK S3 UPLOAD] Saved evidence to local data lake: s3://{self.evidence_bucket}/{s3_key}")
            return s3_key

        try:
            extra_args = {"ContentType": "image/jpeg"} if local_file_path.endswith(".jpg") else {}
            self.s3_client.upload_file(local_file_path, self.evidence_bucket, s3_key, ExtraArgs=extra_args)
            logger.info(f"Uploaded evidence snapshot to S3: s3://{self.evidence_bucket}/{s3_key}")
            return s3_key
        except Exception as e:
            logger.error(f"Failed to upload evidence file to S3: {e}")
            return None

    def generate_presigned_url(self, s3_key: str, expiration_sec: int = 3600) -> str:
        """
        Generates a secure HTTPS presigned URL for the React dashboard to render private S3 evidence objects.
        """
        if self.s3_client is None:
            return f"https://{self.evidence_bucket}.s3.amazonaws.com/{s3_key}?mock_token=123"

        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.evidence_bucket, "Key": s3_key},
                ExpiresIn=expiration_sec
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for {s3_key}: {e}")
            return ""
