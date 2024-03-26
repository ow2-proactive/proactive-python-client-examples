"""
Demonstrates Replication and Merge Flow with Python Tasks

This script showcases the creation and execution of a ProActive Job designed to demonstrate replication and merge control flows. It outlines the process of establishing a connection to the ProActive Scheduler, constructing a job with tasks configured for splitting, processing with replication, and merging the results. Key steps and features demonstrated include:

- Initializing the ProActive Scheduler gateway for subsequent operations.
- Creating a job named "demo_replicate_job" to encapsulate the workflow.
- Configuring a "split" task to initiate the replication process, utilizing the ProactiveFlowBlock for flow control.
- Implementing a replication flow script to specify the criteria for task replication, in this case, triggering three parallel instances of the "process" task.
- Setting up a "process" task that is dynamically replicated based on the replication criteria, demonstrating the scheduler's capability to handle parallel task execution.
- Adding a "merge" task to conclude the replication process, aggregating the outcomes of the replicated tasks. This task utilizes a flow block to signify the end of the replication and merge process.
- Adding tasks to the job, submitting the job to the ProActive Scheduler, and managing the job output, highlighting the end-to-end process of job creation, submission, and output retrieval.
- Ensuring proper cleanup and disconnection from the ProActive Scheduler gateway after job execution.

This script serves as a practical example of leveraging replication and merge flows within ProActive Scheduler jobs, facilitating the construction of complex distributed computing workflows that require parallel processing and result aggregation.

+--------------+      +-------------------+      +--------------+
|              |      |                   |      |              |
|   Split Task |----->| Process Task (x3) |----->|  Merge Task  |
|              |      |                   |      |              |
+--------------+      +-------------------+      +--------------+
        |                      |
        |----------------------|
                   |
              +----------------+
              | Replicate      |
              | Script         |
              +----------------+
"""
from proactive import getProActiveGateway, ProactiveFlowBlock, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_replicate_job")

# Create the split task
print("Creating the split task...")
task_split = gateway.createPythonTask("task_split")
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

# Add the Python tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task_split)
job.addTask(task_process)
job.addTask(task_merge)

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
