import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from edge.mqtt_publisher import SmartCityMQTTClient
from cloud.iot_provisioner import AWSIoTProvisioner

def test_iot_core_integration():
    print("==================================================")
    print("PHASE 10 AWS IOT CORE MQTT & PROVISIONING TEST")
    print("==================================================")
    
    # 1. Test IoT Thing & Policy Provisioning
    provisioner = AWSIoTProvisioner(region="us-east-1")
    prov_res = provisioner.provision_camera_thing(camera_id="CAM-NORTH-001")
    print(f"[1] IoT Provisioning Result: {prov_res}")
    assert "thing_name" in prov_res, "IoT Provisioning failed"

    # 2. Test MQTT Message Publishing
    mqtt_client = SmartCityMQTTClient(client_id="CAM-NORTH-001")
    
    telemetry_payload = {
        "event_type": "TELEMETRY",
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "metrics": {"vehicle_count": 18, "density": "HIGH", "congestion": "MEDIUM"}
    }
    
    accident_payload = {
        "event_type": "ACCIDENT_ALERT",
        "camera_id": "CAM-NORTH-001",
        "timestamp_ms": int(time.time() * 1000),
        "severity": "CRITICAL",
        "accident_probability": 0.94
    }
    
    pub_telemetry_ok = mqtt_client.publish_telemetry("CAM-NORTH-001", telemetry_payload)
    pub_accident_ok = mqtt_client.publish_accident_alert("CAM-NORTH-001", accident_payload)
    
    print(f"[2] MQTT Telemetry Publish Status: {'SUCCESS' if pub_telemetry_ok else 'FAILED'}")
    print(f"[3] MQTT Accident Alert Publish Status: {'SUCCESS' if pub_accident_ok else 'FAILED'}")
    
    assert pub_telemetry_ok, "MQTT telemetry publish failed"
    assert pub_accident_ok, "MQTT accident alert publish failed"
    
    mqtt_client.disconnect()
    
    print("\n==================================================")
    print("PHASE 10 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_iot_core_integration()
