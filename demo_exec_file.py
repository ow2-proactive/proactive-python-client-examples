"""
This script demonstrates an advanced use case of the ProActive Scheduler for running Python tasks, incorporating the use of input files, pre-scripts, and post-scripts. The steps are outlined as follows:

1. The script initiates a connection to the ProActive Scheduler via a utility function provided by 'proactive'.
2. A new job, "demo_exec_file_job," is created to encapsulate the tasks to be executed.
3. A Python task, "demo_exec_file_task," is defined. This task is configured to execute a Python script from a file ('main.py'), with 'param1' and 'param2' as its parameters. This demonstrates the ability to run complex Python scripts with arguments within the ProActive Scheduler environment.
4. The task is further configured to include an entire directory ('hellopkg/**') as input files, illustrating the scheduler's capability to handle tasks with external dependencies or resources.
5. The task is set to run using Python 3, indicated by the addition of generic information specifying the Python command.
6. A pre-script is added to the task, which runs before the main task execution. This pre-script is a simple Bash command that prints a message, showcasing the ability to perform setup operations or environment checks before the task runs.
7. Similarly, a post-script is attached to run after the main task execution. This post-script, also a Bash command, prints a concluding message, useful for cleanup operations or post-execution checks.
8. The task is then added to the job, preparing it for submission to the ProActive Scheduler.
9. The job is submitted, with the script capturing and printing the job ID for reference. The scheduler then manages the job execution based on the provided configuration and its internal policies.
10. The script actively fetches and prints the job's output, allowing for immediate inspection of the execution results.

In conclusion, the script disconnects and terminates the gateway connection, emphasizing clean resource management.

This script highlights the ProActive Scheduler's flexibility and robustness in handling Python tasks, especially those requiring pre-execution and post-execution steps, as well as tasks dependent on external files or resources.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_exec_file_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_exec_file_task")
task.setTaskExecutionFromFile('demo_exec_file/main.py', ['param1', 'param2'])
task.addInputFile('demo_exec_file/hellopkg/**')
task.addGenericInformation("PYTHON_COMMAND", "python3")

print("Adding a pre-script to task...")
pre_script = gateway.createPreScript(gateway.getProactiveScriptLanguage().linux_bash())
pre_script.setImplementation("""echo "\n --- This is a pre-script --- \n";""")
task.setPreScript(pre_script)

print("Adding a post-script to task...")
post_script = gateway.createPostScript(gateway.getProactiveScriptLanguage().linux_bash())
post_script.setImplementation("""echo "\n --- This is a post-script --- \n";""")
task.setPostScript(post_script)

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

gateway.close()
print("Disconnected and finished.")
