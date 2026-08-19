import os
import sys

def test_cicd_pipeline_config():
    print("==================================================")
    print("PHASE 19 DEVOPS CI/CD PIPELINE CONFIG TEST")
    print("==================================================")
    
    workflow_file = ".github/workflows/ci_cd_pipeline.yml"
    dockerfile = "edge/Dockerfile"
    
    assert os.path.exists(workflow_file), f"GitHub Actions workflow missing: {workflow_file}"
    assert os.path.exists(dockerfile), f"Edge Dockerfile missing: {dockerfile}"
    
    print(f"Verified GitHub Actions Workflow: {workflow_file}")
    print(f"Verified Edge Dockerfile: {dockerfile}")
    
    print("\n==================================================")
    print("PHASE 19 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_cicd_pipeline_config()
