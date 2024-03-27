"""
This script demonstrates the creation and execution of a ProActive job that includes a Python task with both pre-execution and post-execution scripts. The workflow encapsulates the entire process from initializing the ProActive gateway, configuring the job and task details, to job submission and output retrieval. Key highlights include:

- Initialization of the ProActive gateway to facilitate communication with the ProActive server.
- Creation of a new job named "demo_pre_post_script_job" to demonstrate the encapsulation of tasks.
- Definition of a Python task "demo_pre_post_script_task" with a custom Python script that utilizes the platform library to print the task name and the Python version.
- Addition of a pre-script and a post-script in Linux Bash, illustrating the capability to perform setup and cleanup operations before and after the main task execution.
- Submission of the job to the ProActive Scheduler and retrieval of the job output, showcasing the end-to-end process of job management within the ProActive ecosystem.

This script is an example of leveraging the ProActive Scheduler's flexibility in handling complex workflows that include pre and post execution steps, suitable for tasks requiring specific environmental setups or cleanup procedures.
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_pre_post_script_job")

# Create a Python task
print("Creating a proactive task...")
task = gateway.createPythonTask("demo_pre_post_script_task")
task.addGenericInformation("PYTHON_COMMAND", "python3")
task.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version())
""")

# Add a pre-script to the task
print("Adding a pre-script to task...")
pre_script = gateway.createPreScript(ProactiveScriptLanguage().linux_bash())
pre_script.setImplementation("""echo "\n --- This is a pre-script --- \n";""")
task.setPreScript(pre_script)

# Add a post-script to the task
print("Adding a post-script to task...")
post_script = gateway.createPostScript(ProactiveScriptLanguage().linux_bash())
post_script.setImplementation("""echo "\n --- This is a post-script --- \n";""")
task.setPostScript(post_script)

# Add the Python task to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task)

# Job submission
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")
