import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.s3_manager import S3DataLakeManager

def test_s3_data_lake():
    print("==================================================")
    print("PHASE 8 AWS S3 DATA LAKE & EVIDENCE TEST")
    print("==================================================")
    
    manager = S3DataLakeManager(
        region="us-east-1",
        evidence_bucket="smart-city-traffic-evidence-demo",
        datalake_bucket="smart-city-traffic-datalake-demo"
    )
    
    # 1. Bucket Initialization
    success = manager.initialize_buckets()
    print(f"[1] Bucket Initialization Status: {'SUCCESS' if success else 'FAILED'}")
    assert success, "Bucket initialization failed"

    # 2. Upload Evidence Snapshot
    sample_snapshot_path = "data/sample_evidence_test.jpg"
    with open(sample_snapshot_path, "wb") as f:
        f.write(b"MOCK_JPEG_IMAGE_DATA_FOR_ACCIDENT_EVIDENCE")
        
    camera_id = "CAM-NORTH-001"
    timestamp_ms = int(time.time() * 1000)
    
    s3_key = manager.upload_accident_evidence(sample_snapshot_path, camera_id, timestamp_ms)
    print(f"[2] Evidence Upload S3 Key: {s3_key}")
    assert s3_key is not None, "Failed to upload snapshot evidence"

    # 3. Presigned URL Generation
    presigned_url = manager.generate_presigned_url(s3_key, expiration_sec=3600)
    print(f"[3] Generated Presigned URL: {presigned_url[:80]}...")
    assert "https://" in presigned_url, "Invalid presigned URL format"

    # Clean up test file
    if os.path.exists(sample_snapshot_path):
        os.remove(sample_snapshot_path)

    print("\n==================================================")
    print("PHASE 8 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_s3_data_lake()
