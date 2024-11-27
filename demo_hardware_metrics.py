"""
This script demonstrates how to monitor hardware metrics using the ProActive Scheduler's monitoring capabilities. It provides a comprehensive overview of both current and historical CPU and memory usage statistics. The workflow includes:

- Connection to the ProActive server using the ProActive gateway, showcasing the SDK's monitoring features.
- Retrieval and display of current CPU metrics, including combined, user, system, idle, and wait CPU usage percentages.
- Collection of historical CPU usage data over the last 5 minutes, showing average, peak, and minimum values.
- Monitoring of current memory metrics, displaying total, used, and free memory in human-readable format.
- Analysis of historical memory usage over the last 5 minutes, presenting average, peak, and minimum values.
- Implementation of proper error handling and gateway connection management.

This script serves as a practical example for users who need to monitor system resources through the ProActive Scheduler, demonstrating the monitoring client's capabilities in tracking both real-time and historical system performance metrics.
"""

from proactive import getProActiveGateway
from proactive.monitoring.ProactiveNodeMBeanClient import TimeRange, CPUMetric, MemoryMetric
import humanize

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    return humanize.naturalsize(bytes_value, binary=True)

# Initialize gateway and client
gateway = getProActiveGateway()
monitoring_client = gateway.getProactiveMonitoringClient()

# Fetch and list all ProActive JMX URLs along with additional information
nodes_info = monitoring_client.list_proactive_jmx_urls()

print("\nUnique ProActive JMX URLs with Node Information:")
for node in nodes_info:
    print(f"JMX URL: {node['proactiveJMXUrl']}, Node Source: {node['nodeSource']}, Host Name: {node['hostName']}")

# Example usage with custom node URL
# node_url = "service:jmx:ro:///jndi/pamr://4097/rmnode" # Default node URL (try)
# node_url = "service:jmx:ro:///jndi/pamr://9232/rmnode" # Custom node URL (trydev2)
# monitoring_client.node_url = node_url

print("\nCurrent ProActive JMX URL:")
print(f"JMX URL: {monitoring_client.node_url}")

try:
    # Get current CPU metrics
    print("\nCurrent CPU Usage:")
    print("-" * 40)
    cpu_usage = monitoring_client.get_cpu_metrics(CPUMetric.COMBINED)
    print(f"Combined CPU Usage: {cpu_usage:.1f}%")
    
    print("\nDetailed CPU Usage:")
    user_cpu = monitoring_client.get_cpu_metrics(CPUMetric.USER)
    system_cpu = monitoring_client.get_cpu_metrics(CPUMetric.SYSTEM)
    idle_cpu = monitoring_client.get_cpu_metrics(CPUMetric.IDLE)
    wait_cpu = monitoring_client.get_cpu_metrics(CPUMetric.WAIT)
    print(f"User CPU........ {user_cpu:.1f}%")
    print(f"System CPU...... {system_cpu:.1f}%")
    print(f"Idle CPU....... {idle_cpu:.1f}%")
    print(f"Wait CPU....... {wait_cpu:.1f}%")

    # Get historical CPU usage (last 5 minutes)
    print("\nHistorical CPU Usage (last 5 minutes):")
    print("-" * 40)
    historical_cpu = monitoring_client.get_cpu_metrics(CPUMetric.COMBINED, historical=True, time_range=TimeRange.MINUTE_5)
    if historical_cpu:
        values = [v for v in historical_cpu if v > 0]  # Filter out zero values
        if values:
            avg_cpu = sum(values) / len(values)
            peak_cpu = max(values)
            min_cpu = min(values)
            print(f"Average CPU Usage.. {avg_cpu:.1f}%")
            print(f"Peak CPU Usage.... {peak_cpu:.1f}%")
            print(f"Minimum CPU Usage. {min_cpu:.1f}%")

    # Get current Memory metrics
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

    # Get historical memory usage (last 5 minutes)
    print("\nHistorical Memory Usage (last 5 minutes):")
    print("-" * 40)
    historical_mem = monitoring_client.get_memory_metrics(MemoryMetric.USED_PERCENT, historical=True, time_range=TimeRange.MINUTE_5)
    if historical_mem:
        values = [v for v in historical_mem if v > 0]  # Filter out zero values
        if values:
            avg_mem = sum(values) / len(values)
            peak_mem = max(values)
            min_mem = min(values)
            print(f"Average Memory Usage.. {avg_mem:.1f}%")
            print(f"Peak Memory Usage.... {peak_mem:.1f}%")
            print(f"Minimum Memory Usage. {min_mem:.1f}%")

except Exception as e:
    print(f"\nError during monitoring: {str(e)}")
finally:
    gateway.close()
    print("\nDisconnected and finished.")

"""
Logging on proactive-server...
Connecting on: https://try.activeeon.com:8443
Connected

Unique ProActive JMX URLs with Node Information:
JMX URL: service:jmx:ro:///jndi/pamr://4097/rmnode, Node Source: On-Prem-Server-Static-Nodes, Host Name: 163-172-30-91.rev.poneytelecom.eu
JMX URL: service:jmx:ro:///jndi/pamr://9232/rmnode, Node Source: On-Prem-Server-Static-Nodes-TryDev2, Host Name: trydev2.activeeon.com

Current ProActive JMX URL:
JMX URL: service:jmx:ro:///jndi/pamr://4097/rmnode

Current CPU Usage:
----------------------------------------
Combined CPU Usage: 1.1%

Detailed CPU Usage:
User CPU........ 0.7%
System CPU...... 0.4%
Idle CPU....... 98.9%
Wait CPU....... 0.0%

Historical CPU Usage (last 5 minutes):
----------------------------------------
Average CPU Usage.. 1.5%
Peak CPU Usage.... 2.0%
Minimum CPU Usage. 1.1%

Current Memory Usage:
----------------------------------------
Memory Usage.... 12.0%
Total Memory.... 62.7 GiB
Used Memory..... 7.5 GiB
Free Memory..... 55.2 GiB

Historical Memory Usage (last 5 minutes):
----------------------------------------
Average Memory Usage.. 12.0%
Peak Memory Usage.... 12.0%
Minimum Memory Usage. 11.9%

Disconnected and finished.
"""