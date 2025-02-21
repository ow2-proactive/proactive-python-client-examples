"""
This script demonstrates how to submit a Bash task to the ProActive Scheduler for execution using the ProActive gateway. The key steps performed in this script include:

1. Establishing a connection with the ProActive Scheduler using the 'getProActiveGateway' function from the 'proactive' library, enabling interaction with the scheduler.
2. Creating a new job named "demo_nodesource_job" through the ProActive gateway. A job serves as a container for one or more tasks, managed and executed by the scheduler.
3. Configuring a task named "demo_nodesource_task" with Bash as the execution language. The task prints a message indicating the task name and the node source on which it runs.
4. Specifying generic information to ensure the task runs on a predefined node source, "On-Prem-Server-Static-Nodes," which helps direct the execution to the desired infrastructure.
5. Adding the configured Bash task to the job, assembling the job's structure with its constituent tasks.
6. Submitting the job to the ProActive Scheduler for execution. The scheduler handles resource allocation, scheduling, and execution of the job.
7. Retrieving and displaying the job's output upon completion. This step provides immediate feedback, useful for debugging and validation.
8. Closing the gateway connection to the ProActive Scheduler to ensure proper resource management and cleanup.

This script provides a simple yet effective example of how to submit and execute a Bash task within the ProActive Scheduler environment. It highlights job and task creation, resource specification, and job execution management.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_nodesource_job")

# Create a task
print("Creating a proactive task...")
task = gateway.createTask(task_name="demo_nodesource_task", language="bash")
task.setTaskImplementation("""
echo "Task $variables_PA_TASK_NAME running on $variables_PA_NODE_SOURCE"
""")

# if you want to run the task on a specific node source
task.addGenericInformation("NODE_SOURCE", "On-Prem-Server-Static-Nodes")
# if NODE_SOURCE is not specified or it is empty, the task will run on any available node source

# Add the task to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task)

# Job submission
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")
