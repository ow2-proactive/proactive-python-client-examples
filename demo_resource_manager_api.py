"""
ProActive Resource Manager API Demo

This script showcases how to use the ProActive Resource Manager (RM) API for interacting with the resource management capabilities of the ProActive scheduling system through Python. It illustrates establishing a connection to the ProActive Scheduler, creating a job, and adding a Groovy task designed to interact with the Resource Manager to perform various operations like retrieving the current Resource Manager state, listing node sources, and managing node tokens.

Key Features:
- Connecting to the ProActive Scheduler and initializing a job.
- Creating a Groovy task that utilizes the Resource Manager API to:
- - Display the state of resources managed by the Resource Manager.
- - List node sources and other Resource Manager configurations.
- - Add and remove node tokens, demonstrating dynamic node management.
- Submitting the job to the scheduler and retrieving the job output upon completion.

Requirements:
- ProActive Scheduler and Python client installed and configured, with access to the Resource Manager.
- Groovy language support for task scripting.

Usage:
- Make sure the ProActive Scheduler is up and running, and accessible from the environment where this script is executed.
- Run this script with Python to perform the demonstrated Resource Manager operations. The script will automatically handle job creation, task submission, and output retrieval.

Note:
- The script assumes familiarity with the ProActive Scheduler and Resource Manager configurations. Modify the connection details and task implementations as necessary for your specific setup.
- This example presumes a proper setup of the ProActive Scheduler, Python client, and Groovy support on the server side.
"""
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_rm_api_job")

# Create a Groovy task
print("Creating a proactive task...")
task = gateway.createTask(language=ProactiveScriptLanguage().groovy(), task_name="demo_rm_api_task")
task.setTaskImplementation("""
// Resource Manager API Documentation
// https://try.activeeon.com/doc/javadoc/org/ow2/proactive/resourcemanager/frontend/ResourceManager.html

// connect to the rm
rmapi.connect()

// displaying the RM state
full = rmapi.getRMStateFull()
full.getNodesEvents().each { event ->
    println(event.getNodeUrl())
    println(event.getNodeState())
}

// println "Test rmapi.getTopology() " + rmapi.getTopology()
println "Test rmapi.getExistingNodeSources() " + rmapi.getExistingNodeSources()
// println "Test rmapi.getInfrasToPoliciesMapping() " + rmapi.getInfrasToPoliciesMapping()
println "Test rmapi.getConnectionInfo() " + rmapi.getConnectionInfo()
println "Test rmapi.getRMStateFull() " + rmapi.getRMStateFull()
// println "Test rmapi.getRMThreadDump() " + rmapi.getRMThreadDump()
println "Test rmapi.getState() " + rmapi.getState()
// println "Test rmapi.getSupportedNodeSourceInfrastructures() " + rmapi.getSupportedNodeSourceInfrastructures()
// println "Test rmapi.getSupportedNodeSourcePolicies() " + rmapi.getSupportedNodeSourcePolicies()
println "Test rmapi.getVersion() " + rmapi.getVersion()
println "Test rmapi.isActive() " + rmapi.isActive()

// get current node url (where the current task is running on)
nodeUrl = variables.get("PA_NODE_URL")
println "PA_NODE_URL: " + nodeUrl

// add node token to the current node
rmapi.addNodeToken(nodeUrl, "demo_rm_api_token")

// Sleep for 5 sec
Thread.sleep(5000)

// remove node token from the current node
rmapi.removeNodeToken(nodeUrl, "demo_rm_api_token")

// do not forget to disconnect from the rm
rmapi.disconnect();
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
