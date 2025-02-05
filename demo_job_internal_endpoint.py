"""
ProActive Job Submission with Internal Endpoint Demo

This script demonstrates the process of job submission and monitoring using the ProActive Python SDK,
with a focus on managing internal endpoints within a job. 

It covers:
- Creating and submitting a ProActive job with a Python task
- Adding an internal endpoint URL (Google) during task execution
- Monitoring the job status until completion
- Removing the internal endpoint before task completion
- Retrieving the job's output

The script showcases how to dynamically manage internal endpoints during job execution using the schedulerapi.
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

schedulerapi.connect()

# Add an external endpoint URL to the job inside the task
schedulerapi.addExternalEndpointUrl(variables.get("PA_JOB_ID"), "google", "https://www.google.com/", "https://cdn-icons-png.flaticon.com/128/2504/2504914.png")

print("Task is running for 15s...")
time.sleep(15)

# Remove an endpoint
schedulerapi.removeExternalEndpointUrl(variables.get("PA_JOB_ID"), "google")

print("Execution completed")
''')

print("Adding proactive task to the proactive job...")
job.addTask(task)

# Submit the job to the ProActive scheduler
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")

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
