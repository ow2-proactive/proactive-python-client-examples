# Demonstrates Bash Task Execution with File Transfer using ProActive Decorators

# This script demonstrates how to use ProActive decorators to create and execute a Bash task within the ProActive Scheduler, focusing on file management and data transfer.
#
# Key features showcased include:
#
# 1. Utilizing the @task decorator to define a Bash task, specifying input and output files for data transfer.
# 2. Using the @job decorator to encapsulate the task into a job, demonstrating how to create and manage a workflow.
# 3. Demonstrating the automatic execution of the defined workflow when the script is run as the main program.
#
# The script defines a single task:
# - `count_files`: A Bash task that prints a greeting message, counts the number of files in a directory, and saves the result to a file.
#
# This task is then organized into a workflow using the @job decorator, showcasing how ProActive can manage the execution of tasks with minimal boilerplate code.
#
# This example serves as a starting point for users to understand how ProActive decorators can be used to streamline the process of defining and executing computational workflows with file transfers in a distributed environment.

# Import the ProActive decorators
from proactive.decorators import task, job

# Define bash_task using the @task decorator to manage input and output files during execution
@task.bash(name="demo_decorators_transf_file_task", input_files=["demo_transf_file/*"], output_files=["demo_transf_file/*"])
def count_files():
    return """
echo "Hello from $variables_PA_TASK_NAME"
pwd && find .

# Specify the directory to count files in
DIRECTORY="./demo_transf_file"

# Count the number of files in the specified directory (excluding directories)
FILE_COUNT=$(find "$DIRECTORY" -type f | wc -l)

# Print the file count to the terminal
echo "Number of files in $DIRECTORY: $FILE_COUNT"

# Specify the filename where the result should be saved inside the DIRECTORY
RESULT_FILE="$DIRECTORY/file_count.txt"

# Write the file count to the specified result file inside the directory
echo "Number of files in $DIRECTORY: $FILE_COUNT" > "$RESULT_FILE"
"""

# Define the workflow using the @job decorator
@job(name="demo_decorators_transf_file_job")
def workflow():
    count_files()

# Execute the workflow
if __name__ == "__main__":
    workflow()