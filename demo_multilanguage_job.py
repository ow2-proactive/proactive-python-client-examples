"""
This script demonstrates the creation and submission of a multi-language job (Python and Groovy tasks) 
to a ProActive scheduler using the proactive python sdk. It covers the initialization of a ProActive gateway, 
creation of a job and tasks, task dependencies, job submission, and retrieval of job outputs.
"""

from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_multilanguage_job")

# Create a Python task
print("Creating a python task...")
python_task = gateway.createPythonTask("demo_python_task")
python_task.setTaskImplementation("""
print("Hello from " + variables.get("PA_TASK_NAME"))
""")

# Create a Groovy task
print("Creating a groovy task...")
groovy_task = gateway.createTask("groovy", "demo_groovy_task")
groovy_task.addDependency(python_task)
groovy_task.setTaskImplementation("""
print "Hello from " + variables.get("PA_TASK_NAME")
""")

# Add tasks to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(python_task)
job.addTask(groovy_task)

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
