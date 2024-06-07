"""
ProActive Signal API Demonstration

This script demonstrates the usage of the ProActive Scheduler Signal API to receive and handle signals.
The example encompasses the following steps:

- Initializing the ProActive Scheduler gateway.
- Creating a ProActive job.
- Creating a Python task that waits for signals with specified variables.
- Adding signals to the Python task, including 'Continue' and 'Update' with defined signal variables.
- Setting the Python task implementation to handle the received signal and update variables.
- Adding the Python task to the ProActive job.
- Submitting the job to the ProActive Scheduler and retrieving the job ID.
- Retrieving the job output.
- Ensuring proper cleanup by disconnecting from the ProActive Scheduler gateway post-execution.

Documentation:
- https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/signal/Signal.html
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_signal_wait_job")

# Create a Python task
print("Creating a proactive task...")
task = gateway.createPythonTask("demo_signal_wait_task")

# Add signals to the Python task
taskSignals = {
    'Continue': {},
    'Update': [
        {
            "name": "INTEGER_VARIABLE", 
            "value": "12", 
            "model": "PA:INTEGER", 
            "description": "Put here a description of the Signal Variable. It will be displayed to the Users when sending the Signal.", 
            "group": "", 
            "advanced": False, 
            "hidden": False
        },
        {
            "name": "LIST_VARIABLE", 
            "value": "True", 
            "model": "PA:LIST(True,False)", 
            "description": "Put here a description of the Signal Variable. It will be displayed to the Users when sending the Signal.", 
            "group": "Group", 
            "advanced": True, 
            "hidden": False
        }
    ]
}
task.setSignals(taskSignals)

# Set the Python task implementation
task.setTaskImplementation("""
task_name = variables.get("PA_TASK_NAME")
task_id = variables.get("PA_TASK_ID")
receivedSignalObjId = "RECEIVED_SIGNAL_"+task_name+"_"+task_id
receivedSignalObj = variables.get(receivedSignalObjId)
print(receivedSignalObjId, receivedSignalObj)

# User defined action for the received signal
if receivedSignalObj['name'] == "Update":
    updatedVariables = receivedSignalObj['variables']
    INTEGER_VARIABLE = updatedVariables['INTEGER_VARIABLE']
    LIST_VARIABLE = updatedVariables['LIST_VARIABLE']
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
