"""
ProActive Job Submission with External Endpoint Demo

This script demonstrates the process of job submission and monitoring using the ProActive Python SDK,
with a focus on managing external endpoints. 

It covers:
- Creating and submitting a ProActive job with a Python task
- Adding an external endpoint URL (Google) to the job
- Monitoring the job status until completion
- Removing the endpoint when the job finishes
- Retrieving the job's output

The script showcases how to integrate external services with ProActive jobs through endpoints.
"""
import time
from proactive import getProActiveGateway

gateway = getProActiveGateway()

# Create and configure a ProActive job and task
print("Creating a proactive job...")
job = gateway.createJob("demo_job_endpoint")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_job_endpoint_task")
task.setTaskImplementation('''
import time
print("Task is running for 30s...")
time.sleep(30)
print("Execution completed")
''')

print("Adding proactive task to the proactive job...")
job.addTask(task)

# Submit the job to the ProActive scheduler
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")

# Add an external endpoint URL
endpoint_name = "google"
gateway.addExternalEndpointUrl(
    job_id=job_id, 
    endpoint_name=endpoint_name,
    external_endpoint_url="https://www.google.com/",
    endpoint_icon_uri="https://cdn-icons-png.flaticon.com/128/2504/2504914.png"
)

time.sleep(15)

# Remove an endpoint
gateway.removeExternalEndpointUrl(
    job_id=job_id,
    endpoint_name=endpoint_name
)

# Monitor job status
is_finished = False
while not is_finished:
    # Get the current state of the job
    job_status = gateway.getJobStatus(job_id)
    
    # Print the current job status
    print(f"Current job status: {job_status}")
    
    # Check if the job has finished
    if job_status.upper() in ["FINISHED", "CANCELED", "FAILED"]:
        is_finished = True
    else:
        # Wait for a few seconds before checking again
        time.sleep(.5)

# Retrieve and print job results
print("Job output:")
print(gateway.getJobOutput(job_id))

# Cleanup
gateway.close()
print("Disconnected and finished.")
