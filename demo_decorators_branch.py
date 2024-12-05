# Demonstrates Python Task Execution with If-Else Branching Control Flow using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a series of Python tasks
# within the ProActive Scheduler, focusing on if-else branching control flow to conditionally execute tasks.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define multiple Python tasks, specifying dependencies and branching control.
# 2. Using the @job decorator to encapsulate the tasks into a job, demonstrating how to create and manage a workflow.
# 3. Using the @branch.condition(), @branch.on_if(), and @branch.on_else() decorators to implement
#    conditional execution within the workflow.
# 4. Using the @branch.continuation() decorator to define a continuation task that always runs after the branching.
# 5. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines five tasks:
# - `start_task`: A Python task that initiates the workflow.
# - `condition_task`: A Python task that evaluates a condition to decide the subsequent flow.
# - `if_task`: A Python task that runs if the condition is satisfied.
# - `else_task`: A Python task that runs if the condition is not satisfied.
# - `continuation_task`: A Python task that always runs after the if-else branches.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline
# the process of defining and executing computational workflows with branching control in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job, branch

# Define the start task
@task.python(name="start_task")
def start_task():
    return """
print("Hello from start_task")
"""

# Define the condition task
@task.python(name="condition_task", depends_on=["start_task"])
@branch.condition()
def condition_task():
    return """
# Always select the "IF" branch
if True:
    branch = "if"
else:
    branch = "else"
"""

# Define the if branch task
@task.python(name="if_task")
@branch.on_if()
def if_task():
    return """
print("Hello from if_task")
"""

# Define the else branch task
@task.python(name="else_task")
@branch.on_else()
def else_task():
    return """
print("Hello from else_task")
"""

# Define the continuation task
@task.python(name="continuation_task")
@branch.continuation()
def continuation_task():
    return """
print("Hello from continuation_task")
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_branch_job")
def workflow():
    start_task()          # Initial task
    condition_task()      # Condition task that branches
    if_task()             # Task to run if condition is True
    else_task()           # Task to run if condition is False
    continuation_task()   # Task that runs after the branches

# Execute the workflow
if __name__ == "__main__":
    workflow()