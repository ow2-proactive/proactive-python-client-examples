"""
Demonstrates Executing Python Tasks with Custom Runtime Environments in ProActive Scheduler

This script showcases the process of executing a Python task within the ProActive Scheduler, emphasizing the configurability of the task's execution environment. Key steps include:

1. Establishing a connection with the ProActive Scheduler using the 'proactive' library.
2. Creating a job named "demo_runtimeenv_job" to organize the execution tasks.
3. Configuring a Python task, "demo_runtimeenv_task," to execute a simple Python script that prints a greeting and the Python version. This demonstrates embedding task logic directly within the script for flexible task creation.
4. Setting the runtime environment for the Python task to ensure it runs in a specified container environment. This step involves specifying the container type (e.g., Docker) and image, showcasing the scheduler's capability to execute tasks in varied and complex runtime environments.
5. Submitting the job to the ProActive Scheduler and printing the job ID for tracking. The scheduler handles the execution based on its configuration and operational policies.
6. Fetching and displaying the job's output after execution, providing immediate insight into the task's results.
7. Closing the connection to the ProActive Scheduler properly, highlighting the importance of clean disconnection and resource management post-execution.

This example underlines the ProActive Scheduler's flexibility in executing Python tasks within custom-defined runtime environments, demonstrating the platform's wide applicability for diverse computational needs.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_runtimeenv_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_runtimeenv_task")
task.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version())
""")
# Define the runtime environment for the task
# Parameters:
# - type (str): Specifies the type of container technology to use for running the task. 
# Options include "docker", "podman", "singularity", or any other value to indicate a non-containerized execution.
# - image (str): The container image to use for running the task. Ensure that the 'py4j' Python package is available in the specified image.
# - nvidia_gpu (bool): Whether to enable NVIDIA GPU support within the container. Automatically set to False if no NVIDIA GPUs are present.
# - mount_host_path (str): The host machine path to mount into the container, providing the container access to specific directories or files from the host.
# - mount_container_path (str): The path inside the container where the host's file system (or a part of it) specified by `mount_host_path` will be accessible.
# - rootless (bool): Enables or disables rootless mode for the container execution, applicable to all container types (default False).
# - isolation (bool): Enables or disables isolation mode specifically for Singularity containers (default False). This parameter is only applicable if 'type' is set to "singularity".
# - no_home (bool): When set to True, the user's home directory is not mounted inside the container if the home directory is not the current working directory. Only applicable to Singularity containers (default False).
# - host_network (bool): Configures the container to use the host's network stack directly, bypassing the default or custom network namespaces (default False).
# - verbose (bool): Enables verbose output for the container runtime environment setup process (default False).
task.setRuntimeEnvironment(type="docker", image="activeeon/python:3.12")

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job, debug=False)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

print("Disconnecting")
gateway.close()
print("Disconnected and finished.")
