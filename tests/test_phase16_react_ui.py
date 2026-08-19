import os
import sys

def test_react_dashboard_files():
    print("==================================================")
    print("PHASE 16 REACT DASHBOARD FRONTEND TEST")
    print("==================================================")
    
    required_files = [
        "frontend/package.json",
        "frontend/public/index.html",
        "frontend/src/index.js",
        "frontend/src/App.jsx",
        "frontend/src/App.css"
    ]
    
    for fpath in required_files:
        assert os.path.exists(fpath), f"Required frontend file missing: {fpath}"
        print(f"Verified React Dashboard File: {fpath}")

    print("\n==================================================")
    print("PHASE 16 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_react_dashboard_files()
