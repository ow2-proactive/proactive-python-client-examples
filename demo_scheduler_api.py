"""
ProActive Scheduler API Demo

This script demonstrates the usage of the ProActive Scheduler API to create and manage computational jobs using Python. It utilizes the ProActive Python client to establish a connection to the ProActive Scheduler, create a job and tasks, and submit these for execution. The example includes creating a Groovy-based task that executes a simple "Hello World" script, showcasing how to interact with the scheduler, submit jobs, and retrieve their output.

Key Features:
- Establishing a connection to the ProActive Scheduler.
- Creating a job and configuring it with a unique name.
- Creating a Groovy task, setting its script implementation to print "Hello World".
- Submitting the job to the scheduler and waiting for its completion.
- Retrieving and displaying the output of the job.

Requirements:
- ProActive Scheduler and Python client installed and configured.
- Groovy language support on the ProActive Scheduler side.

Usage:
- Ensure the ProActive Scheduler is running and accessible.
- Execute this script using Python. The script will connect to the Scheduler, create and submit a job, then retrieve and display the job's output.

Note:
- The script includes placeholders for Scheduler API connectivity, which should be replaced with actual values appropriate for your environment.
- This example assumes that the ProActive Scheduler and Python client are correctly set up and configured in your environment.
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_scheduler_api_job")

# Create a Groovy task
print("Creating a proactive task...")
task = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_scheduler_api_task")
task.setTaskImplementation("""
// Scheduler API Documentation
// https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/task/client/SchedulerNodeClient.html

// importing necessary classes
import org.ow2.proactive.scheduler.common.job.*
import org.ow2.proactive.scheduler.common.task.*
import org.ow2.proactive.scripting.*

// connect to the scheduler
schedulerapi.connect()

// create a hello world job
job = new TaskFlowJob()
job.setName("HelloJob")
task = new ScriptTask()
task.setName("HelloTask")
task.setScript(new TaskScript(new SimpleScript("println 'Hello World'", "groovy")))
job.addTask(task)

// submitting the job
jobid = schedulerapi.submit(job)

// Wait for the task termination
taskResult = schedulerapi.waitForTask(jobid.toString(), "HelloTask", 120000)

// displaying the task output
println taskResult.getOutput().getAllLogs(false)
""")

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
