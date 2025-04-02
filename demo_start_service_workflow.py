"""
This script submits a PSA workflow from the ProActive catalog to the scheduler and retrieves its execution details.

Steps:
1. Initialize the ProActive gateway and REST API for interaction.
2. Ask the user for bucket and workflow name via command-line input.
3. Submit the workflow using `startPSAWorkflowFromCatalog()`, retrieving:
   - `job_id`: The submitted job ID.
   - `instance_id`: The created service instance ID.
   - `service_job_id`: The running service’s job ID.
   - `endpoint`: The service endpoint URL.
   - `service_description`: Workflow metadata.
4. Check execution success:
   - Print job details if successful.
   - Display an error and exit if failed.
5. Close the connection to the ProActive Scheduler.

Ensures efficient workflow execution with structured error handling and resource management.
"""

from proactive import getProActiveGateway, ProactiveRestApi
import sys

# Initialize the ProActive gateway
gateway = getProActiveGateway()
proactive_rest_api = ProactiveRestApi()

# Ask the user for bucket and workflow names
workflow_name = input("Enter the name of the service you want to launch: ").strip()
bucket_name = input("Enter the bucket name containing the service: ").strip()

# Start the workflow
workflow_variables = {}
try:
    job_id, instance_id, service_job_id, endpoint, service_description = gateway.startPSAWorkflowFromCatalog(
        bucket_name, workflow_name, workflow_variables
    )
except Exception as e:
    print(f"\n[ERROR] Exception occurred while starting the workflow: {e}")
    gateway.close()
    sys.exit(1)

# Check if the workflow started successfully
if instance_id:
    print("\n[INFO] Workflow Started Successfully!")
    print(f"JOB_ID: {job_id}")
    print(f"INSTANCE_ID: {instance_id}")
    print(f"ENDPOINT_URL: {endpoint}")
else:
    print(f"\n[ERROR] Failed to start workflow '{workflow_name}' in bucket '{bucket_name}'. Check if bucket_name and/or workflow_name are valid.")
    gateway.close()
    sys.exit(1)

# Cleanup
gateway.close()
print("\n[INFO] Disconnected and finished.")
