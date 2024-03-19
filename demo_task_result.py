"""
ProActive Python SDK: Job Submission with Task Dependencies and Result Handling

This script demonstrates the creation and submission of a ProActive job consisting of two Python tasks with a dependency.

Task A prints a greeting message and generates a result. Task B, which depends on Task A, processes and prints the result from Task A.

The example showcases how to establish a connection to the ProActive Scheduler, create tasks with dependencies, submit the job, and retrieve the job's output.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a ProActive job...")
job = gateway.createJob("demo_task_result_job")

# Create a Python task A
print("Creating a Python task...")
taskA = gateway.createPythonTask("PythonTaskA")
taskA.setTaskImplementation("""
print("Hello")
result = "World"
""")

# Create a Python task B
print("Creating a Python task...")
taskB = gateway.createPythonTask("PythonTaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
for res in results:
    print(str(res))
""")

# Add tasks to the job
job.addTask(taskA)
job.addTask(taskB)

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
