import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloud.lambdas.api_handlers.api_router import lambda_handler

def test_api_gateway_layer():
    print("==================================================")
    print("PHASE 15 AMAZON API GATEWAY REST ENDPOINTS TEST")
    print("==================================================")
    
    endpoints = ["/cameras", "/traffic/current", "/traffic/history", "/accidents", "/statistics"]
    
    for path in endpoints:
        event = {"path": path, "httpMethod": "GET"}
        res = lambda_handler(event, None)
        
        print(f"GET {path:18s} -> Status Code: {res['statusCode']}")
        assert res["statusCode"] == 200, f"Failed GET {path}"
        assert "Access-Control-Allow-Origin" in res["headers"], "CORS headers missing"
        
        body = json.loads(res["body"])
        assert body["status"] == "SUCCESS", f"Expected SUCCESS for {path}"

    print("\n==================================================")
    print("PHASE 15 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_api_gateway_layer()
