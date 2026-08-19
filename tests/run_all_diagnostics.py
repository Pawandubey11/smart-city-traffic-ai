import os
import sys
import glob
import subprocess

def run_all_tests():
    print("==================================================")
    print("RUNNING MASTER DIAGNOSTIC & ALL SYSTEM TEST SUITES")
    print("==================================================")
    
    test_files = sorted(glob.glob("tests/test_*.py") + glob.glob("tests/verify_*.py"))
    
    passed_tests = []
    failed_tests = []
    
    for tf in test_files:
        print(f"\n[EXEC] Running {tf}...")
        res = subprocess.run([sys.executable, tf], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[PASS] {tf}")
            passed_tests.append(tf)
        else:
            print(f"[FAIL] {tf}")
            print("--- Error Log ---")
            print(res.stderr or res.stdout)
            failed_tests.append(tf)
            
    print("\n==================================================")
    print(f"MASTER DIAGNOSTIC SUMMARY: {len(passed_tests)}/{len(test_files)} PASSED")
    print("==================================================")
    
    if failed_tests:
        print(f"Failed Test Suites: {failed_tests}")
        sys.exit(1)
    else:
        print("ALL SYSTEM TEST SUITES PASSED 100% CLEANLY!")

if __name__ == "__main__":
    run_all_tests()
