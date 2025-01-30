"""
This script demonstrates a straightforward use case of submitting a Docker-based task to the ProActive Scheduler for execution. The key steps performed in this script include:

1. Initializing a connection with the ProActive Scheduler using the 'getProActiveGateway' function from the 'proactive' library, facilitating the integration of ProActive Scheduler capabilities into Python applications.
2. Creating a new job named "demo_docker_run_job" through the ProActive gateway. A job serves as a container for one or more tasks, managed and executed by the scheduler.
3. Configuring a task named "demo_docker_run_task" with a Bash script. The script runs a Docker container with Python 3.9 and executes a simple Python command inside the container. This demonstrates how to use Docker to encapsulate and run tasks in a controlled environment.
4. Adding the configured task to the newly created job, assembling the job's structure with its constituent tasks.
5. Submitting the job to the ProActive Scheduler for execution. The scheduler handles the job's lifecycle, including task scheduling, execution, and resource allocation.
6. Retrieving and displaying the job's output upon completion. This step provides immediate insight into the execution results, which is essential for debugging and validation purposes.
7. Closing the gateway connection to the ProActive Scheduler in a graceful manner. This emphasizes the importance of proper resource management and cleanup after job submission and execution.

This script offers a basic example of how to submit and execute a Docker-based task within the ProActive Scheduler environment, focusing on simplicity and user-friendliness. It lays the groundwork for more sophisticated scheduling and task execution scenarios.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_docker_run_job")

# Create a Python task
print("Creating a proactive task...")
task = gateway.createTask(language="bash", task_name="demo_docker_run_task")
task.setTaskImplementation("""
docker run --rm python:3.9 python -c "print('Hello from Docker!')"
""")

# Add the Python task to the job
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
