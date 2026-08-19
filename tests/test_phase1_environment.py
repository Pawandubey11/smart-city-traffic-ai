import sys
import os
import shutil
import importlib

def test_environment():
    print("==================================================")
    print("PHASE 1 ENVIRONMENT VERIFICATION TEST")
    print("==================================================")
    
    # 1. Python Version
    print(f"[1] Python Executable: {sys.executable}")
    print(f"    Python Version: {sys.version.split()[0]}")
    assert sys.version_info >= (3, 8), "Python 3.8+ required"

    # 2. Core Computer Vision & ML Libraries
    libs = [
        ("cv2", "OpenCV"),
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("boto3", "AWS Boto3 SDK")
    ]
    
    print("\n[2] Checking Dependencies:")
    for mod_name, label in libs:
        try:
            mod = importlib.import_module(mod_name)
            version = getattr(mod, "__version__", "Installed")
            print(f"    - {label} ({mod_name}): SUCCESS (v{version})")
        except ImportError:
            print(f"    - {label} ({mod_name}): NOT INSTALLED (will be installed in pip phase)")

    # PyTorch CUDA check
    try:
        import torch
        cuda_avail = torch.cuda.is_available()
        device_name = torch.cuda.get_device_name(0) if cuda_avail else "CPU"
        print(f"    - PyTorch Accelerator Device: {device_name}")
    except Exception as e:
        print(f"    - PyTorch device check skipped: {e}")

    # 3. AWS CLI check
    aws_cli = shutil.which("aws")
    print(f"\n[3] AWS CLI Tool: {'FOUND (' + aws_cli + ')' if aws_cli else 'NOT FOUND (Optional for local, required for deployment)'}")

    # 4. Docker check
    docker_cli = shutil.which("docker")
    print(f"[4] Docker CLI Tool: {'FOUND (' + docker_cli + ')' if docker_cli else 'NOT FOUND (Optional for local dev, required for containers)'}")

    print("\n==================================================")
    print("PHASE 1 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_environment()
