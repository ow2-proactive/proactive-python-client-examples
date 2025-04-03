"""
This script demonstrates how to run multiple jobs across specific node sources using the ProActive Scheduler.
It provides a practical example of how to:

- Connect to the ProActive server using the SDK.
- Create and submit multiple Python-based tasks as individual jobs.
- Distribute these jobs across defined node sources for parallel execution.
- Collect and display hardware metrics (CPU and RAM usage) per job after execution.
- Handle exceptions and ensure clean disconnection from the gateway.

This example showcases ProActive ability to target workloads to custom infrastructure (via node sources) and retrieve performance metrics.
"""
from proactive import getProActiveGateway
from proactive.monitoring.ProactiveNodeMBeanClient import ProactiveNodeMBeanClient
from proactive import getProActiveGateway
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("demo_multi_job_node_source")

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_multi_job_node_source")


# Define specific node sources to target
node_sources = ["On-Prem-Server-Static-Nodes-TryDev2", "On-Prem-Server-Static-Nodes"]

# Create multiple jobs with Python tasks
jobs = []
for i in range(4):
    job = gateway.createJob(f"NodeJob_{i}")
    task = gateway.createPythonTask(f"Task_{i}")
    task.setTaskImplementation(f'''
    import time
    print("Starting task {i}...")
    time.sleep(15)
    print("Finished task {i}")
    ''')
    job.addTask(task)
    jobs.append(job)

# Submit and execute the jobs across selected node sources
job_results = gateway.executeJobsAcrossNodeSources(jobs, node_sources)

# Display job execution results and collected hardware metrics
for result in job_results:
    logger.info(f"Job ID: {result['job_id']}, State: {result['job_state']}, "
    f"CPU Usage: {result['hardware_metrics']['cpu_usage']:.2f}%, "
    f"RAM Usage: {result['hardware_metrics']['ram_usage']:.2f}%")

# Cleanup
gateway.close()
print("Disconnected and finished.")