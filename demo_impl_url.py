"""
This script is designed for submitting a machine learning task, specifically Logistic Regression, to the ProActive Scheduler.
The script follows these steps:

1. It initiates a connection to the ProActive Scheduler gateway.
2. A job named "demo_impl_url_job" is created.
3. A Python task named "demo_impl_url_task" is set up, with variables related to task configuration and scoring metrics.
4. The task implementation is sourced from a URL pointing to a logistic regression script in the catalog, showcasing the ability to incorporate external scripts seamlessly.
5. A fork environment is configured for the task, using a script obtained from another URL. This demonstrates the flexibility in setting up environments, which is essential for tasks requiring specific conditions or dependencies.
6. The task is then added to the job, which is subsequently submitted to the scheduler for execution.

The script emphasizes the use of external resources and environment configuration, highlighting the scheduler's capability to handle complex task setups and dependencies. It's essential to ensure the availability of the specified URLs and the scheduler's accessibility before execution.

This approach is particularly useful for machine learning workflows, where tasks may rely on specific libraries, datasets, and environments.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_impl_url_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_impl_url_task")
task.addVariable("TASK_ENABLED", "True")
task.addVariable("INPUT_VARIABLES", "{}")
task.addVariable("SCORING", "accuracy")
task.setTaskImplementationFromURL(gateway.base_url + "/catalog/buckets/ai-machine-learning/resources/Logistic_Regression_Script/raw")

print("Adding a fork environment to the proactive task...")
task_fork_env = gateway.createForkEnvironment(language="groovy")
task_fork_env.setImplementationFromURL(gateway.base_url + "/catalog/buckets/scripts/resources/fork_env_ai/raw")
task.setForkEnvironment(task_fork_env)
task.addVariable("CONTAINER_PLATFORM", "docker")

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job, debug=False)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

print("Disconnecting")
gateway.close()
print("Disconnected and finished.")
