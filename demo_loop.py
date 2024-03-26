"""
Demonstrates Loop Control Flow with Python Tasks in ProActive Scheduler

This script exemplifies how to create and manage a ProActive Scheduler job incorporating a loop control flow between tasks. It demonstrates establishing a connection to the ProActive Scheduler, setting up a job with Python tasks for starting and ending the loop, and controlling the loop flow using a custom script. The key aspects include:

- Initializing the ProActive Scheduler gateway.
- Creating a job with a descriptive name for the loop demonstration.
- Configuring a "start" task to initiate the loop, showcasing simple Python task creation and execution.
- Setting up an "end" task with a dependency on the "start" task, introducing task dependencies.
- Implementing a loop flow script to control the execution flow based on a loop condition, illustrating advanced job control techniques.
- Submitting the job to the ProActive Scheduler and managing job output, highlighting job submission and output retrieval processes.
- Ensuring proper cleanup by disconnecting from the ProActive Scheduler gateway post-execution.

The script serves as a practical guide for utilizing loop control flows within ProActive Scheduler jobs, facilitating the construction of complex workflows with conditional task execution.

+-------------+           +-------------+
|             |           |             |
|  Start Task |---------->|   End Task  |
|             |           |             |
+-------------+           +-------------+
       ^                           |
       |                           |
       |          +-------------------+
       |          |                   |
       +----------|  Loop Flow Script |
                  |                   |
                  +-------------------+
"""
from proactive import getProActiveGateway, ProactiveFlowBlock, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_loop_job")

# Create the start task
print("Creating the start task...")
task_start = gateway.createPythonTask("task_start")
task_start.setFlowBlock(ProactiveFlowBlock().start())
task_start.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the end task
print("Creating the end task...")
task_end = gateway.createPythonTask("task_end")
task_end.addDependency(task_start)
task_end.setFlowBlock(ProactiveFlowBlock().end())
task_end.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Define the loop criteria script
loop_script = """
i = int(variables.get('PA_TASK_ITERATION'))
if i < 1:
    loop = True
else:
    loop = False
"""
# Create the loop flow between the start and end tasks
flow_script = gateway.createLoopFlowScript(loop_script, task_start.getTaskName(), script_language=ProactiveScriptLanguage().python())
# Associate the loop flow script to the end task
task_end.setFlowScript(flow_script)

# Add the Python tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task_start)
job.addTask(task_end)

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
