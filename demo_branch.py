"""
Branching Logic Demonstration with Python Tasks

This script exemplifies the use of branching logic in a ProActive Scheduler job to demonstrate conditional task execution. It establishes a connection to the ProActive Scheduler and configures a job to execute tasks based on a specified condition. The workflow includes a condition task that determines the execution path (IF/ELSE), followed by a continuation task that runs regardless of the branch taken. This setup showcases the flexibility of the ProActive Scheduler in handling complex job flows.

Key Steps and Features:
- Establishing a connection with the ProActive Scheduler via the ProActive gateway.
- Creating a new job named "demo_branch_job" to encapsulate the conditional execution tasks.
- Configuring a "condition" task to evaluate and decide the execution path. This task implements a simple script to print a greeting and sets up a branch flow script to direct the workflow.
- Setting up "IF" and "ELSE" tasks that represent the branches of conditional execution, each with its own task implementation to print a greeting. The branch taken is determined by the evaluation in the condition task.
- Creating a "continuation" task that will execute after the branching logic, demonstrating how to continue the workflow irrespective of the conditional branches.
- Defining the branch flow script to specify the condition logic and the corresponding tasks for the "IF" and "ELSE" branches, along with the continuation task.
- Adding all tasks to the job and submitting it to the ProActive Scheduler for execution.
- Retrieving and printing the job's output to verify the execution flow and the effective handling of conditional logic.

This script serves as a practical guide for implementing conditional execution within ProActive Scheduler jobs, illustrating how to orchestrate tasks with branching logic and continuation paths.

+----------------+
|                |
|  Condition     |
|  Task          |
|                |
+----------------+
       |
       |
       |---------------------------- 
       |              |             |
       v              v             v
 +---------+      +---------+    +-------------------+
 |         |      |         |    |                   |
 |  IF     |      |  ELSE   |    | Continuation Task |
 |  Task   |      |  Task   |    |                   |
 +---------+      +---------+    +-------------------+
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_branch_job")

# Create the condition task
print("Creating the condition task...")
task_condition = gateway.createPythonTask("task_condition")
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
