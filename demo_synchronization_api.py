"""
ProActive Synchronization API Demonstration

This script illustrates the application of the ProActive Synchronization API in managing dependencies and coordinating task execution within a ProActive Scheduler job. The example encompasses the creation of a job and multiple tasks, where task execution is synchronized using a shared channel and key/value pairs in the ProActive Scheduler's Synchronization API. The scenario includes initializing a synchronization channel, executing tasks with dependencies and conditional execution, and cleaning up resources upon completion.

Key Features:
- Establishing a synchronization channel for a job to coordinate task execution.
- Using the Synchronization API to set and check conditions for task execution, effectively allowing tasks to wait for certain conditions to be met before starting.
- Demonstrating task dependency management where tasks are configured to run sequentially or conditionally based on the state of shared data.
- Illustrating the use of selection scripts and explicit API calls to synchronize task execution.
- Cleanup of synchronization resources to maintain a clean state within the scheduler.

Documentation:
- https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/synchronization/Synchronization.html

Note:
- This script is designed as an educational example to demonstrate the capabilities of the ProActive Synchronization API in a controlled environment.
- Adjustments may be needed to tailor the script to specific operational requirements or scheduler configurations.

                  +------------+
                  | Task Init  |
                  | (Initialize|
                  |  channel & |
                  |  lock)     |
                  +------------+
                        |
     +------------------+------------------+
     |                  |                  |
     v                  v                  v
+--------+         +---------+         +---------+
| Task A |         | Task B  |         | Task C  |
|(Unlock |         |(With    |         |(Explicit|
| B & C) |         |Selection|         | Wait)   |
|        |         | Script) |         |         |
+--------+         +---------+         +---------+
     |                  |                  |
     +------------------+------------------+
                        |
                        v
                 +--------------+
                 |  Task Clean  |
                 |  (Delete     |
                 |  channel)    |
                 +--------------+
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_synchronization_api_job")

# Create the init task in Groovy
print("Creating a proactive task init...")
task_init = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_synchronization_api_task_init")
task_init.setTaskImplementation("""
// Initialize the channel.
// This task creates a channel using the current job id.
// It also sets a lock binding in the key/value store with an initial true value.
jobid = variables.get("PA_JOB_ID")
synchronizationapi.createChannel(jobid, false)
synchronizationapi.put(jobid, "lock", true)
println "Channel " + jobid + " created."
""")

# Create the task A in Groovy
print("Creating a proactive task A...")
task_A = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_synchronization_api_task_a")
task_A.addDependency(task_init)
task_A.setTaskImplementation("""
// Task A unlocks Task B and C.
// This task will sleep for a few seconds and then unlock Task B using the Synchronization API
println "Sleeping 5 seconds"
Thread.sleep(5000)
println "Unlocking Task B and C"
synchronizationapi.put(variables.get("PA_JOB_ID"), "lock", false)
""")

# Create the task B in Groovy (with Selection Script)
print("Creating a proactive task B...")
task_B = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_synchronization_api_task_b")
task_B.addDependency(task_init)
task_B.setTaskImplementation("""
// Prints a message when the task B is running
println "Task B is running"
""")

# Add a selection script to the task B
print("Adding a selection script to the task B...")
task_B_selection_script = gateway.createSelectionScript(language=ProactiveScriptLanguage().groovy())
task_B_selection_script.setImplementation('''
// Wait to be unlocked.
// This task will not be executed until the lock binding changed to false.
// A selection script allows to handle this verification
selected = !(synchronizationapi.get(variables.get("PA_JOB_ID"), "lock"))
''')
task_B.setSelectionScript(task_B_selection_script)

# Create the task C in Groovy (with Explicit Wait)
print("Creating a proactive task C...")
task_C = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_synchronization_api_task_c")
task_C.addDependency(task_init)
task_C.setTaskImplementation("""
// This example is very similar to the task B example, but instead of delaying the execution of Task C using a selection script, Task C will start its execution and explicitly call the Synchronization API to wait.
println "Waiting for Task A"
synchronizationapi.waitUntil(variables.get("PA_JOB_ID"), "lock", "{k, x -> x == false}")
println "Task C has been unlocked by Task A"
""")

# Create the task clean in Groovy
print("Creating a proactive task clean...")
task_clean = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_synchronization_api_task_clean")
task_clean.addDependency(task_A)
task_clean.addDependency(task_B)
task_clean.addDependency(task_C)
task_clean.setTaskImplementation("""
// Delete the channel.
// This task simply deletes the channel used in this job.
// As there is no automatic mechanism to remove channels, it is necessary to delete them explicitly when they are not used any more.
jobid = variables.get("PA_JOB_ID")
synchronizationapi.deleteChannel(jobid )
println "Channel " + jobid + " deleted."
""")

# Add tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task_init)
job.addTask(task_A)
job.addTask(task_B)
job.addTask(task_C)
job.addTask(task_clean)

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
