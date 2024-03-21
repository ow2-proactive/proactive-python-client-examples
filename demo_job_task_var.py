"""
Demonstrates Managing Job and Task Variables in ProActive Scheduler

This script provides a concise example of how to effectively use job and task variables within the ProActive Scheduler to facilitate data sharing and parameterization across different levels of a job's execution context. The workflow includes:

1. Initiating a connection with the ProActive Scheduler via the ProActive gateway to manage job submissions and task executions.
2. Creating a new job, "demo_job_task_var_job", to encapsulate the execution of tasks and demonstrating the setting of job-level variables.
3. Adding a Python task to the job, which is designed to access both job-level and task-level variables. This showcases the hierarchical nature of variable access and management within the ProActive Scheduler.
4. Demonstrating how to set and access job-level variables ("jobVar") and task-level variables ("taskVar"), including conversion from 'unicode' to 'str' for compatibility and ease of use in Python scripts.
5. Submitting the configured job to the ProActive Scheduler, obtaining a job ID for tracking and management purposes.
6. Retrieving and displaying the output of the job upon completion to verify the correct usage and access of variables at both the job and task levels.
7. Closing the gateway connection to the ProActive Scheduler to ensure a clean termination of the session, emphasizing best practices in resource management and cleanup post-job execution.

This example highlights the flexibility and utility of job and task variables in the ProActive Scheduler, enabling dynamic configurations and data passing within complex computational workflows.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a ProActive job...")
job = gateway.createJob("demo_job_task_var_job")

# Define job-level variables
job.addVariable("jobVar", "jobValue")  # only strings are supported

# Create the first Python task
task = gateway.createPythonTask()
task.setTaskName("task")
task.setTaskImplementation("""
jobVar = str(variables.get("jobVar"))  # convert from 'unicode' to 'str'
taskVar = str(variables.get("taskVar"))  # convert from 'unicode' to 'str'
print("Job variable: ", jobVar, type(jobVar))
print("Task variable: ", taskVar, type(taskVar))
""")

# Define task-level variables
task.addVariable("taskVar", "taskValue")  # only strings are supported

# Add tasks to the job
job.addTask(task)

# Submit the job to the ProActive scheduler
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")
