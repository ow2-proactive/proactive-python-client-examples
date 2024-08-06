"""
This script demonstrates how to submit a Dockerfile task to the ProActive Scheduler for execution. The key steps performed in this script include:

1. Initializing a connection with the ProActive Scheduler using the 'getProActiveGateway' function from the 'proactive' library.
2. Creating a new job named "demo_dockerfile_job" through the ProActive gateway.
3. Configuring a Dockerfile task named "demo_dockerfile_task" using ProactiveScriptLanguage().dockerfile(). This task is set up to use a Dockerfile for its implementation.
4. Setting the task implementation by specifying the path to a Dockerfile using setTaskImplementationFromFile().
5. Adding input files for the Dockerfile task, which includes all files in the "demo_dockerfile" directory.
6. Adding the configured Dockerfile task to the newly created job.
7. Submitting the job to the ProActive Scheduler for execution, including any input and output paths.
8. Retrieving and displaying the job's output upon completion.
9. Closing the gateway connection to the ProActive Scheduler.

This script showcases how to create and submit a job that uses a Dockerfile for its task implementation within the ProActive Scheduler environment. It demonstrates the flexibility of the ProActive system in handling different types of tasks, including those based on Docker containers.
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_dockerfile_job")

# Create a Dockerfile task
print("Creating a proactive task...")
task = gateway.createTask(language=ProactiveScriptLanguage().dockerfile(), task_name="demo_dockerfile_task")
task.setTaskImplementationFromFile("demo_dockerfile/Dockerfile")
task.addInputFile("demo_dockerfile/**")

# Add the task to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task)

# Job submission
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print("job_id: " + str(job_id))

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")
