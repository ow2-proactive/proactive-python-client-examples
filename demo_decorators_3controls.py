# Demonstrates Python Task Execution with Loop, Branch, and Replication Control Flow using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a series of Python tasks
# within the ProActive Scheduler, focusing on loop control, conditional branching, and replication control
# to execute tasks in a dynamic workflow.

# Key features showcased include:
#
# 1. Utilizing the @task decorator to define multiple Python tasks, specifying dependencies, branching, looping, and replication control.
# 2. Using the @job decorator to encapsulate the tasks into a job, demonstrating how to create and manage a complete workflow.
# 3. Using the @branch.condition(), @branch.on_if(), and @branch.on_else() decorators to implement conditional branching within the workflow.
# 4. Using the @replicate.start() and @replicate.end() decorators to introduce replication, allowing for parallel execution of tasks.
# 5. Using the @loop.start() and @loop.end() decorators to repeat tasks until specified criteria are met.
# 6. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.

# The script defines the following tasks:
#
# - task_start: A Python task that starts the workflow and initiates the loop.
# - task_condition: A Python task that determines whether to follow the IF or ELSE branch.
# - task_if: A Python task executed if the condition is true.
# - task_else: A Python task executed if the condition is false.
# - task_continuation: A Python task that runs after the branching, regardless of which branch was taken.
# - task_split: A Python task that starts the replication process, triggering multiple parallel instances.
# - task_process: A Python task that processes the replicated instances in parallel.
# - task_merge: A Python task that aggregates the results of the replicated tasks.
# - task_end: A Python task that concludes the workflow, with loop control to decide if the workflow should repeat.
#
# These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage
# the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline
# the process of defining and executing computational workflows with replication control in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job, branch, loop, replicate

# Define the start task
@task.python(name="task_start")
@loop.start()
def task_start():
    return """
print("Hello from task_start")
"""

# Define the condition task for branching
@task.python(name="task_condition", depends_on=["task_start"])
@branch.condition()
def task_condition():
    return """
# Always select the "IF" branch
if True:
    branch = "if"
else:
    branch = "else"
"""

# Define the IF branch task
@task.python(name="task_if")
@branch.on_if()
def task_if():
    return """
print("Hello from task_if")
"""

# Define the ELSE branch task
@task.python(name="task_else")
@branch.on_else()
def task_else():
    return """
print("Hello from task_else")
"""

# Define the continuation task
@task.python(name="task_continuation")
@branch.continuation()
def task_continuation():
    return """
print("Hello from task_continuation")
"""

# Define the split task for replication
@task.python(name="task_split", depends_on=["task_continuation"])
@replicate.start(replicate_criteria="""
runs = 3  # Trigger 3 parallel instances of the process task
""")
def task_split():
    return """
print("Hello from task_split")
"""

# Define the process task that will be replicated
@task.python(name="task_process", depends_on=["task_split"])
def task_process():
    return """
print("Hello from task_process")
"""

# Define the merge task to aggregate the replicated tasks
@task.python(name="task_merge", depends_on=["task_process"])
@replicate.end()
def task_merge():
    return """
print("Hello from task_merge")
"""

# Define the end task with loop control logic
@task.python(name="task_end", depends_on=["task_merge"])
@loop.end(loop_criteria="""
i = int(variables.get('PA_TASK_ITERATION'))
if i < 1:
    loop = True
else:
    loop = False
""")
def task_end():
    return """
print("Hello from task_end")
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_3controls_job")
def workflow():
    task_start()          # Start of the loop
    task_condition()      # Condition task for branching
    task_if()             # IF branch task
    task_else()           # ELSE branch task
    task_continuation()   # Continuation task after branching
    task_split()          # Start of replication
    task_process()        # Process task to be replicated
    task_merge()          # Merge task after replication
    task_end()            # End task with loop control

# Execute the workflow
if __name__ == "__main__":
    workflow()