"""
Demonstrates Branch Flow with Python Tasks

This script demonstrates the creation and execution of a ProActive job designed to illustrate branch flow control with Python tasks. It outlines the process of establishing a connection to the ProActive Scheduler, constructing a job with tasks configured for conditional branching, and executing a streamlined workflow. Key steps include:

- Initializing the ProActive Scheduler gateway for subsequent operations.
- Creating a job named "demo_brunch_job" to encapsulate the workflow.
- Executing a "start" task to initiate the workflow.
- Configuring a "condition" task to implement a conditional flow that dictates the subsequent path (IF or ELSE).
- Setting up an "if" task and an "else" task, each executed based on the condition.
- Executing a "continuation" task that is always performed after the branching, regardless of the path taken.
- Adding tasks to the job, submitting the job to the ProActive Scheduler, and managing the job output, highlighting the entire process of job creation, submission, and output retrieval.

This script serves as a practical example of leveraging branch flows within ProActive Scheduler jobs, facilitating the construction of straightforward distributed computing workflows that require conditional task execution.

+----------------+     +------------------+     +-------------------+
|                |     |                  |     |                   |
|   Start Task   |---->| Condition Task   |---->| Continuation Task |
|                |     | (IF or ELSE)     |     |                   |
+----------------+     +------------------+     +-------------------+
       |
       |------------------------------------------->|
                       |
               +----------------+
               | Branch Flow     |
               | Script          |
               +----------------+
"""
from proactive import getProActiveGateway, ProactiveFlowBlock, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_brunch_job")

# Create the start task
print("Creating the start task...")
task_start = gateway.createPythonTask("task_start")
task_start.setFlowBlock(ProactiveFlowBlock().start())
task_start.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the condition task
print("Creating the condition task...")
task_condition = gateway.createPythonTask("task_condition")
task_condition.addDependency(task_start)
task_condition.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the IF task
print("Creating the IF task...")
task_if = gateway.createPythonTask("task_IF")
task_if.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the ELSE task
print("Creating the ELSE task...")
task_else = gateway.createPythonTask("task_ELSE")
task_else.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the continuation task
# The continuation task will always be executed regardless of the branch criteria
print("Creating the continuation task...")
task_continuation = gateway.createPythonTask("task_continuation")
task_continuation.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")
task_continuation.setFlowBlock(ProactiveFlowBlock().end())  # Add end block to match start

# Define the branch flow script
branch_script = """
# Always select the "IF" branch
if True:
    branch = "if"
else:
    branch = "else"
"""
flow_script = gateway.createBranchFlowScript(
    branch_script, 
    task_if.getTaskName(), 
    task_else.getTaskName(), 
    task_continuation.getTaskName(), 
    script_language=ProactiveScriptLanguage().python()
)
task_condition.setFlowScript(flow_script)

# Add the Python tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task_start)
job.addTask(task_condition)
job.addTask(task_if)
job.addTask(task_else)
job.addTask(task_continuation)

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