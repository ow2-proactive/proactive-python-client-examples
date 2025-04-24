"""
This script starts a PSA service instance via REST using the ProActive Python SDK.

Steps:
1. Initialize the ProActive gateway.
2. Ask the user for bucket and workflow name via input.
3. Submit the service using `startServiceViaRest()`.
4. Display the service instance information.
5. Close the connection.
"""

from proactive import getProActiveGateway
import sys

# Initialize the ProActive gateway
gateway = getProActiveGateway()

workflow_name = input("Enter the name of the service you want to launch: ").strip()
bucket_name = input("Enter the bucket name containing the service: ").strip()

workflow_variables = {
    "INSTANCE_NAME": f"{workflow_name.lower()}-${{PA_JOB_ID}}",
    "ENDPOINT_ID": f"{workflow_name.lower()}-endpoint-${{PA_JOB_ID}}",
    # Add more variables if needed, e.g. "DATABASE": "TEST", "USER": "admin"
}

try:
    # Start service via REST POST
    response = gateway.startService(
        bucket_name=bucket_name,
        workflow_name=workflow_name,
        variables=workflow_variables
    )
except Exception as e:
    print(f"\n[ERROR] Failed to start service: {e}")
    gateway.close()
    sys.exit(1)

if "instance_id" in response:
    print("\n[INFO] Service started successfully!")
    print(f"INSTANCE_ID: {response['instance_id']}")
    print(f"SERVICE_ID: {response.get('service_id')}")
    print(f"STATUS: {response.get('instance_status')}")
    deployments = response.get("deployments", [])
    if deployments:
        for dep in deployments:
            endpoint = dep.get("endpoint", {}).get("proxyfiedUrl") or dep.get("endpoint", {}).get("url")
            print(f"ENDPOINT: {endpoint}")
else:
    print("\n[ERROR] Unexpected response format.")
    print(response)

# Cleanup
gateway.close()
print("\n[INFO] Disconnected and finished.")
