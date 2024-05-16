"""
ProActive Job Submission, Dependency Management, and Result Retrieval Script

This script demonstrates the end-to-end process of job submission, task dependency management, and result retrieval using the ProActive Python SDK.

It covers creating a ProActive job, adding multiple Python tasks with dependencies, submitting the job to the ProActive Scheduler, and retrieving the job's results.

The script concludes by fetching and displaying the precious results for each task.
"""
from proactive import getProActiveGateway
gateway = getProActiveGateway()

job = gateway.createJob("demo_job_results")

print("Creating a proactive task1...")
task1 = gateway.createPythonTask("PythonTask1")
task1.setPreciousResult(True)
task1.setTaskImplementation('''
import json
id = int(variables.get('PA_TASK_ID'))
name = str(variables.get('PA_TASK_NAME'))
data = {
    'ID': id,
    'Name': name
}
result = json.dumps(data)
resultMap.put("T1_RESULT_JSON", result)
resultMap.put("T1_ID", id)
resultMap.put("T1_Name", name)
print("Task ", name, " completed")
''')

print("Creating a proactive task2...")
task2 = gateway.createPythonTask("PythonTask2")
task2.addDependency(task1)
task2.setPreciousResult(True)
task2.setTaskImplementation('''
import json
id = int(variables.get('PA_TASK_ID'))
name = str(variables.get('PA_TASK_NAME'))
data = {
    'ID': id,
    'Name': name
}
result = json.dumps(data)
resultMap.put("T2_RESULT_JSON", result)
resultMap.put("T2_ID", id)
resultMap.put("T2_Name", name)
print("Task ", name, " completed")
''')

print("Adding proactive tasks to the proactive job...")
job.addTask(task1)
job.addTask(task2)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")

print("Getting job resultMap:")
print(gateway.getJobResultMap(job_id))
# {
#   'T1_ID': 0, 'T1_Name': 'PythonTask', 'T1_RESULT_JSON': '{"ID": 0, "Name": "PythonTask"}',
#   'T2_ID': 1, 'T2_Name': 'PythonTask2', 'T2_RESULT_JSON': '{"ID": 1, "Name": "PythonTask2"}'
# }

print("Getting job precious results per task:")
print("PythonTask1: ", gateway.getTaskPreciousResult(job_id, 'PythonTask1')) # {"ID": 0, "Name": "PythonTask1"}
print("PythonTask1: ", gateway.getTaskPreciousResult(job_id, 'PythonTask2')) # {"ID": 1, "Name": "PythonTask2"}

gateway.close()
print("Disconnected and finished.")
