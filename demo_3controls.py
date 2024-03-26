"""
Comprehensive Control Flow Demonstration in ProActive Scheduler

This script presents an advanced demonstration of utilizing various control flows within a single ProActive Scheduler job. The job, named "demo_3controls_job," integrates conditional branching, task replication, and loop control to execute a complex workflow. The process begins with a start task, proceeds through conditional branching (IF/ELSE), continues to task replication, and concludes with a looping mechanism that potentially repeats the entire sequence.

Workflow Overview:
- Initiation of the ProActive Scheduler gateway and job creation with the title "demo_3controls_job."
- Execution of a start task to initiate the workflow.
- Implementation of a conditional flow with a condition task that dictates the subsequent path (IF or ELSE), followed by a continuation task.
- Incorporation of a split task that triggers task replication, creating multiple instances of a process task based on predefined criteria.
- Merging of replicated tasks' outcomes and transitioning into a merge task.
- Finalization with an end task that includes a loop back to the start under certain conditions, allowing for the repetition of the entire workflow.

Key Features:
- Demonstrates the application of ProactiveFlowBlock for defining start and end points within the job.
- Utilizes the ProactiveScriptLanguage for scripting flow controls.
- Integrates a branch flow script to direct workflow based on conditions.
- Employs replication through a replicate flow script, enhancing parallel task execution.
- Establishes a loop control to potentially repeat the workflow, demonstrating dynamic job execution based on runtime data.

This script exemplifies the ProActive Scheduler's capabilities to orchestrate complex job flows, combining multiple control mechanisms to achieve sophisticated task coordination and execution strategies.

+-------------+         +----------------+         
|             |         |                |         
|  Start Task |-------->| Condition Task |---------------------+
|             |         |                |                     |
+-------------+         +----------------+                     |
       ^                             |                         |
       |                             v                         v
       |                      +------+-------+         +---------------+
       |                      | IF   | ELSE  |         | Continuation  |
       |                      +------+-------+         |     Task      |
       |                                               +---------------+
       |                                                       |
       |                                                       v
       |                                                +-------------+         +----------------+
       |                                                |             |         |                |
       |                                                |  Split Task |-------->|  Process Task  |
       |                                                |             |         |      (x3)      |
       |                                                +-------------+         +----------------+
       |                                                                                |
       |                                                                                v
       |                                                                          +-------------+
       |                                                                          |   Merge     |
       |                                                                          |    Task     |
       |                                                                          +-------------+
       |                                                                                 |
       |                                                                                 v
       |                                    +-------------+                       +-------------+
       |                                    |             |                       |             |
       +------------------------------------| Loop        |<----------------------|   End Task  |
                                            | Control     |                       |             |
                                            +-------------+                       +-------------+
"""
from proactive import getProActiveGateway, ProactiveFlowBlock, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_3controls_job")

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

# Create the split task
print("Creating the split task...")
task_split = gateway.createPythonTask("task_split")
task_split.addDependency(task_continuation)
task_split.setFlowBlock(ProactiveFlowBlock().start())
task_split.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the replicate criteria script
replicate_script = """
runs = 3  # Trigger 3 parallel instances of the process task
"""
flow_script = gateway.createReplicateFlowScript(replicate_script, script_language=ProactiveScriptLanguage().python())
# Associate the replicate flow script to the split task
task_split.setFlowScript(flow_script)

# Create the process task to be replicated
print("Creating the process task...")
task_process = gateway.createPythonTask("task_process")
task_process.addDependency(task_split)
task_process.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the merge task
print("Creating the merge task...")
task_merge = gateway.createPythonTask("task_merge")
task_merge.addDependency(task_process)
task_merge.setFlowBlock(ProactiveFlowBlock().end())
task_merge.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create the end task
print("Creating the end task...")
task_end = gateway.createPythonTask("task_end")
task_end.addDependency(task_merge)
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
job.addTask(task_condition)
job.addTask(task_if)
job.addTask(task_else)
job.addTask(task_continuation)
job.addTask(task_split)
job.addTask(task_process)
job.addTask(task_merge)
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
