"""
This script demonstrates how to monitor hardware metrics using the ProActive Scheduler's monitoring capabilities. It provides a comprehensive overview of both current and historical CPU and memory usage statistics. The workflow includes:

- Connection to the ProActive server using the ProActive gateway, showcasing the SDK's monitoring features.
- Retrieval and display of current CPU metrics, including combined, user, system, idle, and wait CPU usage percentages.
- Collection of historical CPU usage data based on the dynamic job duration, showing average, peak, and minimum values.
- Monitoring of current memory metrics, displaying total, used, and free memory in human-readable format.
- Analysis of historical memory usage based on the dynamic job duration, presenting average, peak, and minimum values.
- Implementation of proper error handling and gateway connection management.

This script serves as a practical example for users who need to monitor system resources through the ProActive Scheduler, demonstrating the monitoring client's capabilities in tracking both real-time and historical system performance metrics.
"""

import time
import logging
from proactive import getProActiveGateway
from proactive.monitoring.ProactiveNodeMBeanClient import TimeRange, CPUMetric, MemoryMetric
import humanize

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MonitoringJobMetrics')

# Helper function to format bytes into human-readable format
def format_bytes(bytes_value):
    return humanize.naturalsize(bytes_value, binary=True)

# Function to map job duration to the appropriate TimeRange
def get_dynamic_time_range(duration_minutes):
    """Returns the most suitable TimeRange based on the given duration in minutes."""
    if duration_minutes <= 1:
        return TimeRange.MINUTE_1
    elif duration_minutes <= 5:
        return TimeRange.MINUTE_5
    elif duration_minutes <= 10:
        return TimeRange.MINUTE_10
    elif duration_minutes <= 30:
        return TimeRange.MINUTE_30
    elif duration_minutes <= 60:
        return TimeRange.HOUR_1
    elif duration_minutes <= 120:
        return TimeRange.HOUR_2
    elif duration_minutes <= 240:
        return TimeRange.HOUR_4
    elif duration_minutes <= 480:
        return TimeRange.HOUR_8
    elif duration_minutes <= 1440:
        return TimeRange.DAY_1
    elif duration_minutes <= 10080:
        return TimeRange.WEEK_1
    elif duration_minutes <= 43200:
        return TimeRange.MONTH_1
    else:
        return TimeRange.YEAR_1

# Function to convert TimeRange to human-readable label
def get_time_range_label(time_range):
    """Map TimeRange to a human-readable label."""
    mapping = {
        TimeRange.MINUTE_1: "1 minute",
        TimeRange.MINUTE_5: "5 minutes",
        TimeRange.MINUTE_10: "10 minutes",
        TimeRange.MINUTE_30: "30 minutes",
        TimeRange.HOUR_1: "1 hour",
        TimeRange.HOUR_2: "2 hours",
        TimeRange.HOUR_4: "4 hours",
        TimeRange.HOUR_8: "8 hours",
        TimeRange.DAY_1: "1 day",
        TimeRange.WEEK_1: "1 week",
        TimeRange.MONTH_1: "1 month",
        TimeRange.YEAR_1: "1 year",
    }
    return mapping.get(time_range, "Unknown Time Range")

# Initialize the ProActive gateway
gateway = getProActiveGateway()

try:
    logger.info("Connected to ProActive server.")

    # Initialize monitoring client
    monitoring_client = gateway.getProactiveMonitoringClient()

    # Create a job with a high CPU/RAM task
    job = gateway.createJob("Monitoring_Job_Metrics")
    task = gateway.createPythonTask("MonitoringJobMetrics")
    task.setTaskImplementation('''
import subprocess
import sys

# Ensure numpy is installed
subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "numpy"])

import numpy as np
import time

print("Generating high CPU and RAM usage...")
# Simulate high CPU usage
for _ in range(20):  # Increased iterations for more execution time
    matrix = np.random.random((3000, 3000))  # Moderate matrix size
    np.dot(matrix, matrix)

# Simulate high RAM usage
large_data = np.zeros((50000000,), dtype=np.float32)  # Increased memory allocation
time.sleep(20)  # Add a sleep to extend execution time
print("Task completed.")
''')

    job.addTask(task)

    # Submit the job
    logger.info("Submitting the job to the ProActive scheduler...")
    job_id = gateway.submitJob(job)
    logger.info(f"Job submitted with ID: {job_id}")

    # Monitor job status
    logger.info("Monitoring job status...")
    start_time = time.time()
    is_finished = False
    while not is_finished:
        job_status = gateway.getJobStatus(job_id)
        logger.info(f"Current job status: {job_status}")

        # Check if the job has finished
        if job_status.upper() in ["FINISHED", "CANCELED", "FAILED"]:
            is_finished = True
        else:
            # Wait for a few seconds before checking again
            time.sleep(5)

    # Calculate job duration in minutes
    end_time = time.time()
    duration_seconds = end_time - start_time
    duration_minutes = round(duration_seconds / 60)
    logger.info(f"Job duration: {duration_seconds:.2f} seconds")

    # Determine the time range based on job duration
    time_range = get_dynamic_time_range(duration_minutes)
    time_range_label = get_time_range_label(time_range)
    logger.info(f"Using dynamic time range: {time_range_label}")

    # Fetch hardware metrics
    print("\nCurrent CPU Usage:")
    print("-" * 40)
    combined_cpu = monitoring_client.get_cpu_metrics(CPUMetric.COMBINED)
    print(f"Combined CPU Usage: {combined_cpu:.1f}%")

    print("\nDetailed CPU Usage:")
    user_cpu = monitoring_client.get_cpu_metrics(CPUMetric.USER)
    system_cpu = monitoring_client.get_cpu_metrics(CPUMetric.SYSTEM)
    idle_cpu = monitoring_client.get_cpu_metrics(CPUMetric.IDLE)
    wait_cpu = monitoring_client.get_cpu_metrics(CPUMetric.WAIT)
    print(f"User CPU........ {user_cpu:.1f}%")
    print(f"System CPU...... {system_cpu:.1f}%")
    print(f"Idle CPU....... {idle_cpu:.1f}%")
    print(f"Wait CPU....... {wait_cpu:.1f}%")

    # Historical CPU Metrics
    print(f"\nHistorical CPU Usage (last {time_range_label}):")
    print("-" * 40)
    historical_cpu = monitoring_client.get_cpu_metrics(CPUMetric.COMBINED, historical=True, time_range=time_range)
    if historical_cpu:
        avg_cpu = sum(historical_cpu) / len(historical_cpu)
        peak_cpu = max(historical_cpu)
        min_cpu = min(historical_cpu)
        print(f"Average CPU Usage.. {avg_cpu:.1f}%")
        print(f"Peak CPU Usage.... {peak_cpu:.1f}%")
        print(f"Minimum CPU Usage. {min_cpu:.1f}%")

    # Current Memory Metrics
    print("\nCurrent Memory Usage:")
    print("-" * 40)
    used_percent = monitoring_client.get_memory_metrics(MemoryMetric.USED_PERCENT)
    total = monitoring_client.get_memory_metrics(MemoryMetric.TOTAL)
    used = monitoring_client.get_memory_metrics(MemoryMetric.ACTUAL_USED)
    free = monitoring_client.get_memory_metrics(MemoryMetric.ACTUAL_FREE)
    print(f"Memory Usage.... {used_percent:.1f}%")
    print(f"Total Memory.... {format_bytes(total)}")
    print(f"Used Memory..... {format_bytes(used)}")
    print(f"Free Memory..... {format_bytes(free)}")

    # Historical Memory Metrics
    print(f"\nHistorical Memory Usage (last {time_range_label}):")
    print("-" * 40)
    historical_mem = monitoring_client.get_memory_metrics(MemoryMetric.USED_PERCENT, historical=True, time_range=time_range)
    if historical_mem:
        avg_mem = sum(historical_mem) / len(historical_mem)
        peak_mem = max(historical_mem)
        min_mem = min(historical_mem)
        print(f"Average Memory Usage.. {avg_mem:.1f}%")
        print(f"Peak Memory Usage.... {peak_mem:.1f}%")
        print(f"Minimum Memory Usage. {min_mem:.1f}%")

except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    gateway.close()
    logger.info("Disconnected and finished.")