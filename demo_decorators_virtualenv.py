# Demonstrates Python Task Execution with Custom Virtual Environment using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a Python task within the ProActive Scheduler, with a focus on configuring a custom virtual environment.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define a Python task, specifying a virtual environment using either a requirements file or a list of specific Python packages.
# 2. Using the @job decorator to encapsulate the task into a job, demonstrating how to create and manage a workflow.
# 3. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines a single task:
# - `print_virtualenv`: A Python task that prints a greeting message, the current Python version, a list of installed packages, and performs a simple HTTP request.
#
# This task is then organized into a workflow using the @job decorator, showcasing how ProActive can manage the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing computational workflows with custom virtual environments in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job

# Define python_task using the @task decorator
# The task can be configured in two ways:
# Example 1: Define the task using a requirements file
# @task.python(name="virtualenv_task", virtual_env={"requirements_file": "demo_virtualenv/requirements.txt"})
# Example 2: Define the task with specific Python packages using virtual_env requirement
@task.python(name="virtualenv_task", virtual_env={"requirements": ["requests==2.26.0"]})
def print_virtualenv():
     return """
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
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_virtualenv")
def workflow():
    print_virtualenv()

# Execute the workflow
if __name__ == "__main__":
    workflow()