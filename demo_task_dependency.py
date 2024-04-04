"""
Demonstrates Task Dependencies and Execution Order in ProActive Scheduler

This script showcases how to structure a ProActive Scheduler job with multiple Python tasks that have specific execution dependencies. The objective is to illustrate the control over task execution order through dependencies, ensuring tasks execute in a predetermined sequence. The workflow includes:

1. Establishing a connection with the ProActive Scheduler via the ProActive gateway, setting the stage for job and task management.
2. Creating a new job titled "demo_task_dependency" to encapsulate the series of tasks designed to demonstrate dependency management.
3. Configuring four Python tasks (Task A, Task B, Task C, and Task D), each designed to print the task name and Python version to illustrate task execution.
4. Setting execution dependencies among the tasks to establish the execution order: Task A executes first; Tasks B and C depend on Task A and execute in parallel after Task A completes; Task D depends on both Task B and Task C and executes only after both have completed. This setup demonstrates parallel and sequential task execution strategies within the same job.
5. Submitting the configured job to the ProActive Scheduler, with the script providing a job ID for reference and management purposes.
6. Fetching and displaying the job output upon completion, allowing for verification of the execution order and dependency management among the tasks.
7. Closing the gateway connection to ensure a clean and orderly shutdown of the session, highlighting best practices in resource management and post-execution cleanup.

Task A
 |
 |--- Task B ---|
 |              |
 |              ---> Task D
 |              |
 |--- Task C ---|

Through this example, users gain insights into leveraging task dependencies within the ProActive Scheduler to orchestrate complex workflows, achieving precise control over task execution sequencing and parallelism.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_task_dependency")

# Create a Python task A
print("Creating a proactive task...")
taskA = gateway.createPythonTask("PythonTaskA")
taskA.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version())
""")

# Create a Python task B
print("Creating a proactive task...")
taskB = gateway.createPythonTask("PythonTaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"), " [running in parallel with Task C]")
print("Python version: ", platform.python_version())
""")

# Create a Python task C
print("Creating a proactive task...")
taskC = gateway.createPythonTask("PythonTaskC")
taskC.addDependency(taskA)
taskC.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"), " [running in parallel with Task B]")
print("Python version: ", platform.python_version())
""")

# Create a Python task D
print("Creating a proactive task...")
taskD = gateway.createPythonTask("PythonTaskD")
taskD.addDependency(taskB)
taskD.addDependency(taskC)
taskD.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"), " [waits for Task B and C to be finished]")
print("Python version: ", platform.python_version())
""")

# Add the Python tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(taskA)
job.addTask(taskB)
job.addTask(taskC)
job.addTask(taskD)

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
