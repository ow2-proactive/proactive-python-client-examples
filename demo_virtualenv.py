"""
This script demonstrates the creation and execution of a Python task within a ProActive Scheduler job, highlighting task customization and execution environment configuration. The process is as follows:

1. A connection is established with the ProActive Scheduler through the `getProActiveGateway` utility function from the 'proactive' package.
2. A job named "demo_virtualenv_job" is created, serving as a container for the tasks that will be executed.
3. A Python task named "demo_virtualenv_task" is set up. This task is designed to print a greeting message along with the Python version of the runtime environment. The task implementation is defined inline, showcasing the flexibility of embedding task logic directly within the script.
4. The Python task is configured to run using the specified Python interpreter (default is Python 3), ensuring compatibility with the provided task implementation.
5. A virtual environment is configured for the Python task. The `setVirtualEnv` method is used to specify the required Python packages, such as 'requests'. This method handles the creation of a virtual environment and the installation of specified packages, ensuring a clean and isolated execution environment for the task.
6. The Python task is added to the job, making it ready for submission to the ProActive Scheduler.
7. The job is submitted to the scheduler, and the script prints the job ID as a reference. The scheduler manages the execution of the job according to its configuration and scheduling policies.
8. After submission, the script fetches and prints the output of the job, providing immediate feedback on the task execution.

Finally, the script ensures proper disconnection and termination of the gateway connection to the ProActive Scheduler, emphasizing the importance of resource management and cleanup post-execution.

This script exemplifies a basic yet powerful use case of the ProActive Scheduler for executing Python tasks with specific runtime environments, demonstrating both task and environment configurability.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_virtualenv_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_virtualenv_task")
task.setTaskImplementation("""
import sys
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version(), sys.executable)

import pkg_resources

def list_installed_packages():
    installed_packages = pkg_resources.working_set
    package_list = sorted([f"{package.key}=={package.version}" for package in installed_packages])
    return package_list

packages = list_installed_packages()
for package in packages:
    print(package)

import requests
print("Running a simple http datetime request")
r = requests.get('http://httpbin.org/ip')
print(r.json())
""")

task.setDefaultPython("/usr/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py39/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py310/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py311/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py312/bin/python3")

# Sets up a virtual environment for the task.
# 
# Parameters:
# - requirements (list): List of Python packages to install in the virtual environment (default is an empty list).
# - basepath (str): Base path where the virtual environment will be created (default is current directory).
# - name (str): Name of the virtual environment directory (default is 'venv').
# - verbosity (bool): If True, enables verbose output (default is False).
# - overwrite (bool): If True, overwrites the existing virtual environment (default is False).
# - install_requirements_if_exists (bool): If True, installs requirements even if the virtual environment already exists (default is False).

task.setVirtualEnv(requirements=['requests==2.26.0'])
# task.setVirtualEnvFromFile('demo_virtualenv/requirements.txt')

# Notes:
# - The current directory of a task is its localspace which is a temporary space (removed after task execution).
# If you want to keep the virtual env existing for the others tasks, the best is to use a common shared space (e.g. set basepath="/shared")

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
