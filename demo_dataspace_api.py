"""
ProActive Scheduler Data Management Example

This script demonstrates how to manage data transfer between local spaces and ProActive Scheduler's data spaces (user and global) within a Python script using the ProActive Python Client. It covers scenarios where data is transferred from the local space to both user and global spaces and vice versa.

Key Concepts:
- Data Spaces: The ProActive Scheduler distinguishes between user and global data spaces for storing and managing files.
    - User Space: Private space accessible by the user's jobs.
    - Global Space: Shared space accessible by all users.
- API Usage: Shows how to use the `userspaceapi` and `globalspaceapi` to connect to these spaces and perform file operations like pushing and pulling files.

Workflow:
1. A text file named 'hello_world.txt' containing the text "Hello World" is created in the local space.
2. The file is then transferred to the user space using `userspaceapi`, demonstrating the process of pushing files to a data space.
3. The script also outlines how to modify the code to transfer files to and from the global space instead, using `globalspaceapi`.
4. TaskB retrieves the file from the specified data space (user or global, depending on the modification) and prints its contents.

Instructions for switching between user and global data spaces are provided within the comments for tailored data management needs.

Dependencies:
- ProActive Python Client: Facilitates interaction with the ProActive Scheduler and Resource Manager.
- Java Virtual Machine (JVM) Integration: Required for file operations within the data spaces.

Usage:
- This example is designed to run as a job within the ProActive Scheduler environment, showcasing data space interaction through specific API calls.
- It includes detailed steps for setting up the environment, creating tasks, managing dependencies, and executing the job on the ProActive Scheduler.

Path to the user space: `$PA_SCHEDULER_HOME/data/defaultuser/`
Path to the global space: `$PA_SCHEDULER_HOME/data/defaultglobal/`

# To transfer data to the global space, replace in taskA the following code:
```
print("Transferring file from the local space to the user space")
userspaceapi.connect()
userspaceapi.pushFile(gateway.jvm.java.io.File(file_name), dataspace_path)
print("Done")
````
by:
```
print("Transferring file from the local space to the global space")  
globalspaceapi.connect()
globalspaceapi.pushFile(gateway.jvm.java.io.File(file_name), dataspace_path)
print("Done")
```

# To transfer data from the gloal space, replace in TaskB the following code:
```
# Transfer file from the user space to the local space
print("Importing file from the user space to the local space")
userspaceapi.connect()
userspaceapi.pullFile(dataspace_path, gateway.jvm.java.io.File(file_name))
```
by:
```
# Transfer file from the global space to the local space
print("Importing file from the global space to the local space")
globalspaceapi.connect()
globalspaceapi.pullFile(dataspace_path, gateway.jvm.java.io.File(file_name))
```
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a ProActive job...")
job = gateway.createJob("demo_dataspace_api_job")

# Create a Python task A
print("Creating a Python task...")
taskA = gateway.createPythonTask("PythonTaskA")
taskA.setTaskImplementation("""
import os

# Define the file name
file_name = 'hello_world.txt'

# Write "Hello World" to the file
with open(file_name, 'w') as file:
    file.write("Hello World")
print("File "+file_name+" has been created with content 'Hello World'")

# Get the ID of the job and task
job_id, task_id = variables.get("PA_JOB_ID"), variables.get("PA_TASK_ID")

# Define the file path on the data space
dataspace_path = os.path.join('job_id_{}/task_id_{}'.format(job_id, task_id), file_name)

print("Transferring file from the local space to the user space")
userspaceapi.connect()
userspaceapi.pushFile(gateway.jvm.java.io.File(file_name), dataspace_path)
print("Done")

# Transfer the file path to the next task
variables.put("TASK_A_FILE_NAME", file_name)
variables.put("TASK_A_DATASPACE_PATH", dataspace_path)
""")

# Create a Python task B
print("Creating a Python task...")
taskB = gateway.createPythonTask("PythonTaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
import os

# Get the file info from the previous task
file_name = variables.get("TASK_A_FILE_NAME")
dataspace_path = variables.get("TASK_A_DATASPACE_PATH")

# Transfer file from the user space to the local space
print("Importing file from the user space to the local space")
userspaceapi.connect()
userspaceapi.pullFile(dataspace_path, gateway.jvm.java.io.File(file_name))

# Check if the file exists
if os.path.exists(file_name):
    # Open the file for reading
    print("The contents of "+file_name+" is:")
    with open(file_name, 'r') as file:
        # Read the contents of the file
        contents = file.read()
        # Print the contents
        print(contents)
else:
    print("File does not exist at: "+file_name)
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
