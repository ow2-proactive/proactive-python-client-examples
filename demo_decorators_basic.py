"""
Demonstrates Basic Usage of ProActive Decorators for Task and Job Definition

This script showcases the use of ProActive decorators to simplify the creation and execution of tasks and jobs within the ProActive Scheduler. Key features demonstrated include:

1. Utilizing the @task decorator to define individual tasks with customizable attributes such as name and dependencies.
2. Employing the @job decorator to encapsulate a workflow of tasks as a cohesive job.
3. Illustrating how to define task dependencies using the 'depends_on' parameter in the @task decorator.
4. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.

The script defines three tasks:
- task_1: A simple task that takes two parameters and prints them
- task_2: A task that accepts keyword arguments and prints them
- task_3: A task that depends on the completion of task_1 and task_2, demonstrating task dependencies

These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage complex task dependencies and executions with minimal boilerplate code.

This example serves as a starting point for users to understand how ProActive decorators can streamline the process of defining and executing computational workflows in a distributed environment.
"""
from proactive.decorators import task, job

# Define task_1 using the @task decorator
@task(name="task_1")
def task_1(param1, param2):
    # Return a string that will be executed as Python code on the ProActive node
    return f'print("Task 1 executing on ProActive with param1={param1} and param2={param2}")'

# Define task_2 using the @task decorator, accepting arbitrary keyword arguments
@task(name="task_2")
def task_2(**kwargs):
    # Return a string that will be executed as Python code, printing all received keyword arguments
    return f'print("Task 2 executing on ProActive with kwargs={kwargs}")'

# Define task_3 using the @task decorator, specifying dependencies on task_1 and task_2
@task(name="task_3", depends_on=["task_1", "task_2"])
def task_3():
    # This task will only execute after task_1 and task_2 have completed
    return 'print("Task 3 executing on ProActive after task_1 and task_2 completion")'

# Define the workflow using the @job decorator
@job(name="demo_decorators_basic")
def workflow():
    # Register tasks with their respective arguments
    task_1(10, 20)
    task_2(param1="value1", param2="value2")
    task_3()

# Execute the workflow
if __name__ == "__main__":
    workflow()
