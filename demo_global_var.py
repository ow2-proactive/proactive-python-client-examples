"""
Demonstrates the Use of Global Variables Between Tasks in ProActive Scheduler

This script exemplifies how to create and manage jobs and tasks within the ProActive Scheduler with a focus on inter-task communication via global variables. The workflow comprises:

1. Establishing a connection with the ProActive Scheduler using the ProActive gateway.
2. Creating a job named "demo_global_var_job" to encapsulate the tasks.
3. Configuring and adding two Python tasks, "PythonTaskA" and "PythonTaskB", to the job. "PythonTaskA" is designed to execute a simple script that sets a global variable. "PythonTaskB" demonstrates accessing and utilizing this global variable, showcasing inter-task communication.
4. Demonstrating task dependency by configuring "PythonTaskB" to depend on "PythonTaskA", ensuring "PythonTaskA" executes first and sets the global variable before "PythonTaskB" attempts to access it.
5. Submitting the job to the ProActive Scheduler and capturing the job ID for reference and tracking.
6. Fetching and displaying the job's output upon completion, providing immediate feedback on the execution results.
7. Closing the gateway connection to the ProActive Scheduler, highlighting the importance of proper cleanup post-execution.

This script serves as a practical guide to utilizing global variables for data sharing between tasks, facilitating complex workflows within the ProActive Scheduler.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a ProActive job...")
job = gateway.createJob("demo_global_var_job")

# Create a Python task A
print("Creating a Python task...")
taskA = gateway.createPythonTask("PythonTaskA")
taskA.setTaskImplementation("""
# Setting a global variable
variables.put("stringVariableFromA", "Hello from TaskA")
variables.put("integerVariableFromA", 1)
variables.put("floatVariableFromA", 0.5)
variables.put("listVariableFromA", [1, 2])  # convert to 'py4j.java_collections.JavaList'
variables.put("dictVariableFromA", {'a': 1, 'b': 2})  # convert to 'py4j.java_collections.JavaMap'
""")

# Create a Python task B
print("Creating a Python task...")
taskB = gateway.createPythonTask("PythonTaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
# Accessing the variable from TaskA
stringVariableFromA = str(variables.get("stringVariableFromA"))  # convert to Python string
integerVariableFromA = variables.get("integerVariableFromA")
floatVariableFromA = variables.get("floatVariableFromA")
listVariableFromA = list(variables.get("listVariableFromA"))  # convert to Python list
dictVariableFromA = dict(variables.get("dictVariableFromA"))  # convert to Python dict

print("Received in TaskB:")
print("stringVariableFromA", stringVariableFromA, type(stringVariableFromA))
print("integerVariableFromA", integerVariableFromA, type(integerVariableFromA))
print("floatVariableFromA", floatVariableFromA, type(floatVariableFromA))
print("listVariableFromA", listVariableFromA, type(listVariableFromA))
print("dictVariableFromA", dictVariableFromA, type(dictVariableFromA))
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
