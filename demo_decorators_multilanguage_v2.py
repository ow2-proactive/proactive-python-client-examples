# Demonstrates Multi-language Usage of ProActive Decorators for Task and Job Definition

# This script showcases the use of ProActive decorators to create and execute tasks written in different languages using the ProActive Scheduler. Key features demonstrated include:
#
# 1. Utilizing the @task decorator to define individual tasks in various languages such as Python, Bash, R, and Groovy.
# 2. Employing the @job decorator to encapsulate a workflow of tasks into a job.
# 3. Illustrating how to define task dependencies using the 'depends_on' parameter in the @task decorator, including tasks written in different languages.
# 4. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines four tasks:
# - python_task: A simple Python task that prints a message.
# - bash_task: A Bash task that prints a message using the echo command.
# - r_task: An R task that prints a message.
# - groovy_task: A Groovy task that depends on the completion of python_task, demonstrating cross-language task dependencies.
#
# These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage complex task dependencies and executions with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing multi-language computational workflows in a distributed environment.

from proactive.decorators import task, job

# Define python_task using the @task decorator
@task.python(name="python_task")
def python_task():
    # Return a string that will be executed as Python code on the ProActive node
    return 'print("This is a Python task!")'

# Define bash_task using the @task decorator
@task.bash(name="bash_task")
def bash_task():
    # Return a string that will be executed as Bash code on the ProActive node
    return 'echo "This is a Bash task!"'

# Define r_task using the @task decorator
@task.r(name="r_task")
def r_task():
    # Return a string that will be executed as R code on the ProActive node
    return 'print("This is an R task!")'

# Define groovy_task using the @task decorator, specifying a dependency on python_task
@task.groovy(name="groovy_task", depends_on=["python_task"])
def groovy_task():
    # This task will only execute after python_task has completed
    return 'println("This is a Groovy task that depends on the Python task!")'

# Define the workflow using the @job decorator
@job(name="demo_multilanguage_decorators")
def workflow():
    # Register tasks
    python_task()
    bash_task()
    r_task()
    groovy_task()

# Execute the workflow
if __name__ == "__main__":
    workflow()