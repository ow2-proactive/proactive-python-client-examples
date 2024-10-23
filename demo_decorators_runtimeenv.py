# Demonstrates Python Task Execution with Custom Runtime Environment using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a Python task within the ProActive Scheduler, emphasizing the configurability of the task's execution environment.
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define a Python task, specifying a custom runtime environment using Docker.
# 2. Using the @job decorator to encapsulate the task into a job, demonstrating how to create and manage a workflow.
# 3. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines a single task:
# - print_python_version: A Python task that prints a greeting message along with the current Python version.
#
# This task is then organized into a workflow using the @job decorator, showcasing how ProActive can manage the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing computational workflows with custom runtime environments in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job

# Define print_python_version_task using the @task decorator
@task.python(name="print_python_version_task", runtime_env={"type": "docker", "image": "activeeon/python:3.12"})
def print_python_version():
    return """
import platform
print("Hello from print_python_version_task")
print("Python version: ", platform.python_version())
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_runtimeenv")
def workflow():
    print_python_version()

# Execute the workflow
if __name__ == "__main__":
    workflow()