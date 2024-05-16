"""
ProActive Signal API Demonstration

This script demonstrates how to submit a Python job to the ProActive Scheduler and send a 'Stop' signal to a specified job.

Overview:
1. Handle command-line arguments to retrieve the target job ID.
2. Initialize the ProActive Scheduler gateway.
3. Create a ProActive job for sending signals.
4. Create a task to send the 'Stop' and 'Continue' signals using a bash script.
5. Add a pre-script to the task to set session ID and ProActive URL.
6. Submit the job to the ProActive Scheduler.
7. Retrieve and display the job output.
8. Ensure proper cleanup by disconnecting from the ProActive Scheduler gateway post-execution.

Documentation:
- https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/signal/Signal.html
"""
import argparse
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Step 1: Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description='Submit a Python task to the ProActive Scheduler.')
parser.add_argument('--target_job_id', required=True, type=str, help='The target job ID to send the stop signal to')
args = parser.parse_args()

# Retrieve the target_job_id from command-line arguments
target_job_id = args.target_job_id

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a job to send signal and variables to the previous job
print("Creating a proactive job to send stop signal to the previous job...")

# Create a new job
job = gateway.createJob("demo_signal_send_job")

# Create a bash task to send the stop signal
send_signal_task = gateway.createTask(ProactiveScriptLanguage().linux_bash(), "send_signal_task")

# Set the task implementation to send the stop signal using curl
send_signal_task.setTaskImplementation(f""" 
sessionid=$variables_SESSION_ID
proactiveurl=$variables_PROACTIVE_URL
target_job_id={target_job_id}

# Send the Continue signal with variables
curl -X POST \\
-H "sessionid:$sessionid" \\
-H "Content-Type: application/json" \\
-d '{{"BOOLEAN_VARIABLE": "false", "INTEGER_VARIABLE": 24}}' \\
"$proactiveurl/rest/scheduler/job/$target_job_id/signals?signal=Continue"

# Send the Stop signal
# curl -X POST -H "sessionid:$sessionid" $proactiveurl/rest/scheduler/job/$target_job_id/signals?signal="Stop"
""")

# Add a pre-script to the task to set session ID and the ProActive URL
print("Adding a pre-script to task...")
pre_script = gateway.createPreScript(ProactiveScriptLanguage().groovy())
pre_script.setImplementation("""
schedulerapi.connect()
def sessionId = schedulerapi.getSession()

def connectionInfo = schedulerapi.getConnectionInfo()
String ciUrl = connectionInfo.getUrl()
def url = new URL(ciUrl)
def proactiveUrl = url.getProtocol() + "://" + url.getHost() + ":" + url.getPort()

variables.put("SESSION_ID", sessionId) 
variables.put("PROACTIVE_URL", proactiveUrl)
""")
send_signal_task.setPreScript(pre_script)

# Add the task to the job
job.addTask(send_signal_task)

# Submit the job to the proactive scheduler
print("Submitting the send signal job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")
