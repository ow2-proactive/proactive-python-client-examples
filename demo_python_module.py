"""
This script illustrates how to execute a Python task within the ProActive Scheduler that depends on a custom Python module. The process involves creating a job, setting up a task that utilizes external Python files, and managing task submission and output retrieval. The workflow is as follows:

- Initialization of the ProActive gateway to connect with the ProActive server, demonstrating the SDK's simplicity in establishing a connection.
- Creation of a new job named "demo_python_module_job," illustrating the straightforward job setup process within the ProActive Scheduler.
- Configuration of a Python task "demo_python_module_task," which is specifically designed to execute a Python script that imports and utilizes functions from a custom module located in the 'demo_python_module' directory. This highlights the Scheduler's capability to handle tasks with external dependencies.
- Addition of the entire 'demo_python_module/**' directory as input files to ensure that all necessary external Python files are available for the task's execution environment, showcasing the flexibility in managing external resources.
- Execution of the Python script within the task, where 'sys.path.append(os.getcwd())' is used to dynamically adjust the Python path at runtime to prevent 'ModuleNotFoundError'. This emphasizes the ability to configure the execution environment to suit specific requirements.
- Submission of the job to the ProActive Scheduler and retrieval of the job output, providing a complete example of how to manage and execute jobs that require external Python modules or packages.

This script serves as a practical example for users looking to execute Python tasks that rely on custom modules, demonstrating both the ProActive Scheduler's flexibility in handling complex tasks and the proactive-python-sdk's functionality in streamlining the process.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_python_module_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_python_module_task")
task.addInputFile('demo_python_module/**')
task.setTaskImplementation("""
from demo_python_module.mymodule import add_numbers
x=1
y=2
z = add_numbers(x, y)
print("x:", x, "+ y:", y, "= z:", z)
""")

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

gateway.close()
print("Disconnected and finished.")