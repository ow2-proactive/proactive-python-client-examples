"""
This script finishes one or more PSA service instances via REST using the ProActive Python SDK.

Steps:
1. Connect to the ProActive gateway.
2. Retrieve active service instances.
3. Ask the user to choose which instances to stop (comma-separated).
4. Use `finishServiceViaRest()` (PUT) to finish each selected service.
5. Confirm success or failure for each.
6. Disconnect.
"""

from proactive import getProActiveGateway
import sys
import json

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Get all running service instances
instances = gateway.getProactiveRestApi().get_active_service_instances()

if not instances:
    print("\n[INFO] No running service instances found.")
    gateway.close()
    sys.exit(0)

instances_info = {
    str(inst["instance_id"]): {
        "instance_id": inst["instance_id"],
        "user_name": inst.get("user_name"),
        "INSTANCE_NAME": inst["variables"].get("INSTANCE_NAME", "N/A"),
        "workflow_name": inst["service_id"],
        "bucket_name": inst.get("bucket_name", "service-automation"),
        "endpoint": (
            inst["deployments"][0]["endpoint"].get("proxyfiedUrl")
            or inst["deployments"][0]["endpoint"].get("url")
            if inst.get("deployments") else "N/A"
        )
    }
    for inst in instances
}

print("\nAvailable Service Instances:")
for sid, info in instances_info.items():
    print(f" - ID {sid}: {info['INSTANCE_NAME']} | Endpoint: {info['endpoint']}")

selected_ids = input(
    "\nEnter one or more INSTANCE_IDs to stop (comma-separated): "
).strip().split(",")

# Validation
selected_ids = [sid.strip() for sid in selected_ids if sid.strip() in instances_info]

if not selected_ids:
    print("\n[ERROR] No valid INSTANCE_IDs selected. Exiting.")
    gateway.close()
    sys.exit(1)

for sid in selected_ids:
    instance = instances_info[sid]
    print(f"\n[INFO] Stopping Instance {sid} ({instance['INSTANCE_NAME']})...")

    try:
        result = gateway.finishServiceViaRest(
            instance_id=instance["instance_id"],
            bucket_name=instance["bucket_name"],
            workflow_name=f"Finish_{instance['workflow_name']}",
            variables={}
        )
        print("[SUCCESS] Service finished.")
        #print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[ERROR] Failed to finish service {sid}: {e}")

# Disconnect
gateway.close()
print("\n[INFO] Disconnected and finished.")

