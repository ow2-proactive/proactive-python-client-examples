"""
ProActive Signal API Demonstration

This script demonstrates how to send a signal to a specified job with or without variables.

Overview:
1. Handle command-line arguments to retrieve the target job ID, signal name, and variables dictionary.
2. Initialize the ProActive Scheduler gateway.
3. Send the signals using the gateway's sendSignal function.
4. Ensure proper cleanup by disconnecting from the ProActive Scheduler gateway post-execution.

Documentation:
- https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/signal/Signal.html
"""

import argparse
import json
from proactive import getProActiveGateway, ProactiveScriptLanguage

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description='Submit a Python task to the ProActive Scheduler.')
parser.add_argument('--target_job_id', required=True, type=str, help='The target job ID to send the signal to')
parser.add_argument('--signal_name', required=True, type=str, help='The name of the signal to be sent')
parser.add_argument('--variables', required=False, type=str, help='The dictionary of variables to be sent along with the signal.')
args = parser.parse_args()

# Retrieve the target_job_id, signal_name, and variables from command-line arguments
target_job_id = int(args.target_job_id)
signal_name = args.signal_name
if(args.variables):
    variables = json.loads(args.variables)
else:
    variables = {}

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Send signal to the job with target_job_id
gateway.sendSignal(target_job_id,signal_name,variables)

# Cleanup
gateway.close()
print("Disconnected and finished.")
