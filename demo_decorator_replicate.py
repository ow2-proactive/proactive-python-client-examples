# Demonstrates Python Task Execution with Replication Control Flow using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a series of Python tasks
# within the ProActive Scheduler, focusing on replication control flow to execute tasks in parallel.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define multiple Python tasks, specifying dependencies and replication control.
# 2. Using the @job decorator to encapsulate the tasks into a job, demonstrating how to create and manage a workflow.
# 3. Using the @replicate.start() and @replicate.end() decorators to implement replication within the workflow,
#    allowing for parallel execution of tasks based on custom criteria.
# 4. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines three tasks:
# - `split_task`: A Python task that starts the replication.
# - `process_task`: A Python task that processes replicated instances.
# - `merge_task`: A Python task that aggregates the outcomes of the replicated tasks.
#
# These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage
# the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline
# the process of defining and executing computational workflows with replication control in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job, replicate

# Define the start task for the replication (split task)
@task.python(name="split_task")
@replicate.start(replicate_criteria="""
runs = 3  # Trigger 3 parallel instances of the process task
""")
def split_task():
    return """
print("Hello from the split task")
"""

# Define the process task to be replicated
@task.python(name="process_task", depends_on=["split_task"])
def process_task():
    return """
print("Processing after split task")
"""

# Define the merge task to aggregate the outcomes of the replicated tasks
@task.python(name="merge_task", depends_on=["process_task"])
@replicate.end()
def merge_task():
    return """
print("Hello from the merge task after replication")
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_replicate")
def workflow():
    split_task()     # Start of the replication
    process_task()   # Processing after replication
    merge_task()     # Merge task after replication

# Execute the workflow
if __name__ == "__main__":
    workflow()