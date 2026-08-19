import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.cloudfront_s3_deploy import CloudFrontS3Deployer

def test_cloudfront_deployment():
    print("==================================================")
    print("PHASE 17 AMAZON CLOUDFRONT CDN & S3 DEPLOYMENT TEST")
    print("==================================================")
    
    deployer = CloudFrontS3Deployer()
    res = deployer.deploy_react_build()
    
    print(f"Deployment Result: {res}")
    assert res["status"] == "SUCCESS"
    assert "https://" in res["https_dashboard_url"]
    
    print("\n==================================================")
    print("PHASE 17 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_cloudfront_deployment()
