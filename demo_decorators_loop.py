# Demonstrates Python Task Execution with Loop Control Flow using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a series of Python tasks
# within the ProActive Scheduler, focusing on loop control flow to repeat parts of the workflow.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define multiple Python tasks, specifying dependencies and loop control.
# 2. Using the @job decorator to encapsulate the tasks into a job, demonstrating how to create and manage a workflow.
# 3. Using the @loop.start() and @loop.end() decorators to implement a loop within the workflow, allowing for repeated execution based on custom criteria.
# 4. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines four tasks:
# - `before_task`: A Python task that runs before the loop begins.
# - `start_task`: A Python task that serves as the entry point to the loop.
# - `end_task`: A Python task that controls the loop logic, determining if the loop should continue or end.
# - `after_task`: A Python task that runs after the loop has completed.
#
# These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing computational workflows with loop control in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job, loop

# Define a task to be run before the loop
@task.python(name="before_task")
def before_task():
    return """
print("Hello from the before-loop task")
"""

# Define the start task for the loop
@task.python(name="start_task", depends_on=["before_task"])
@loop.start()
def start_task():
    return """
print("Hello from the start of the loop task")
"""

# Define the end task for the loop with loop control logic
@task.python(name="end_task", depends_on=["start_task"])
@loop.end(loop_criteria="""
i = int(variables.get('PA_TASK_ITERATION'))
if i < 1:
    loop = True
else:
    loop = False
""")
def end_task():
    return """
print("End of loop task execution")
"""

# Define a task to be run after the loop
@task.python(name="after_task", depends_on=["end_task"])
def after_task():
    return """
print("Hello from the after-loop task")
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_loop")
def workflow():
    before_task()    # Task before the loop
    start_task()     # Start of the loop
    end_task()       # End of the loop
    after_task()     # Task after the loop

# Execute the workflow
if __name__ == "__main__":
    workflow()
