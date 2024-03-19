"""
This script demonstrates the process of creating and submitting a job to the ProActive Scheduler.
It involves the following steps:

1. Establishing a connection to the ProActive Scheduler gateway.
2. Creating a job with the name "demo_selectionscript_job".
3. Creating a Python task named "demo_selectionscript_task", which prints a greeting message.
4. Adding a selection script to ensure the task runs only on Linux machines.
5. Submitting the created job to the ProActive Scheduler for execution.
6. Finally, disconnecting and terminating the gateway session.

The script makes use of utility functions from 'proactive' module for gateway connection and task/job management.

Please ensure the ProActive Scheduler is running and accessible, and the required scripts are present in the specified locations before executing this script.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_selectionscript_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_selectionscript_task")
task.setTaskImplementation("""print("Hello from " + variables.get("PA_TASK_NAME"))""")
task.addGenericInformation("PYTHON_COMMAND", "python3")

print("Adding a selection script to the proactive task...")
task_selection_script = gateway.createSelectionScript(language="groovy")
task_selection_script.setImplementationFromFile("scripts/is_linux.groovy")  # assert task only runs on linux machines
task.setSelectionScript(task_selection_script)

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job, debug=False)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

print("Disconnecting")
gateway.close()
print("Disconnected and finished.")
