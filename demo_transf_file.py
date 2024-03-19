"""
This script demonstrates the creation and submission of a ProActive job that includes a single Bash task designed to count the number of files within a specified directory, outputting the count both to the terminal and to a file within the same directory. The task showcases file handling in ProActive tasks, particularly how to include input files for processing and designate output files to capture task results. This example is particularly useful for understanding data transfer and file management in ProActive workflows.

Key Steps:
- Establishes a connection to the ProActive scheduler and creates a new job.
- Sets up a Bash task that counts files in the 'demo_transf_file' directory, saving the count to 'file_count.txt' within the same directory.
- Demonstrates the use of input and output files in ProActive tasks, specifying patterns to include all files within a directory for processing and result generation.
- Submits the job to the ProActive scheduler, retrieves, and prints the job output to the console.

Ensure the ProActive scheduler is accessible and the 'proactive' module is correctly set up before executing this script.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_transf_file_job")

print("Creating a proactive task...")
task = gateway.createTask(language="bash", task_name="demo_transf_file_task")
task.setTaskImplementation("""
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
""")
task.addInputFile('demo_transf_file/**')
task.addOutputFile('demo_transf_file/**')

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

print("Disconnecting")
gateway.close()
print("Disconnected and finished.")
