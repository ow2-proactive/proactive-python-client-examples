# Demonstrates Python Task Execution with Pre-Script and Post-Script using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a Python task with pre-script and post-script support within the ProActive Scheduler.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define a Python task, with pre-script and post-script to manage additional setup and cleanup operations.
# 2. Using the @job decorator to encapsulate the task into a job, demonstrating how to create and manage a workflow.
# 3. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines a single task:
# - `example_task`: A Python task that prints a greeting and the Python version, with pre-script and post-script in Bash.
#
# This task is then organized into a workflow using the @job decorator, showcasing how ProActive can manage the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing computational workflows in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job

# Define the pre-script in Bash using the @task.prescript decorator
@task.prescript.bash
def pre_script_example():
    return '''#!/bin/bash
echo "Starting pre-script execution"
date
echo "Pre-script completed"
'''

# Define the post-script in Bash using the @task.postscript decorator
@task.postscript.bash
def post_script_example():
    return '''#!/bin/bash
echo "Starting post-script execution"
date
echo "Post-script completed"
'''

# Define a Python task using the @task decorator
# This task includes the pre-script and post-script defined above
@task.python(
    name="example_task",
    prescript=pre_script_example,
    postscript=post_script_example
)
def example_task():
    return '''
import platform
import sys

print("Hello from Python Task!")
print(f"Python version: {platform.python_version()}")
print(f"System platform: {sys.platform}")
'''

# Define the workflow using the @job decorator
@job(name="demo_decorators_pre_post_script_job")
def workflow():
    example_task()

# Execute the workflow
if __name__ == "__main__":
    workflow()