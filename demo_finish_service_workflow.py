"""
This script retrieves and manages active PSA service instances in the ProActive Scheduler.

Steps:
1. Initialize the ProActive gateway for communication.
2. Retrieve all active PSA service instances.
3. Extract relevant details, including:
   - `instance_id`
   - `user_name`
   - `endpoint`
   - `INSTANCE_NAME`
4. Display available instance IDs and prompt the user to select one for termination.
5. Validate user input:
   - If valid, finish the selected service instance.
   - If invalid, prompt again until a correct ID is entered.
6. Close the connection to the ProActive Scheduler.

Ensures efficient instance management with interactive selection and error handling.
"""

from proactive import getProActiveGateway
import json

# Initialize the ProActive gateway
gateway = getProActiveGateway()

instances = gateway.getProactiveRestApi().get_active_service_instances()

# Get instances info
instances_info = {
    str(instance["instance_id"]): {  # Convert instance_id to string for easy comparison
        "instance_id": instance["instance_id"],
        "user_name": instance["user_name"],
        "endpoint": instance["deployments"][0]["endpoint"].get("proxyfiedUrl") or instance["deployments"][0]["endpoint"].get("url"),
        "INSTANCE_NAME": instance["variables"].get("INSTANCE_NAME", "N/A")
    }
    for instance in instances
}

# Show available instance IDs
available_instance_ids = list(instances_info.keys())
print("\nAvailable Instance IDs:", ", ".join(available_instance_ids))

while True:
    user_input = input("\nEnter the INSTANCE_ID of the service instance you want to stop: ").strip()
    
    if user_input in instances_info:
        selected_instance = instances_info[user_input]
        print("\n[INFO] Selected Instance Details:")
        print(selected_instance)

        # Finish service instance
        print("Finishing Service with instance id...")
        gateway.finishPSAServiceInstance(user_input)
        break
    else:
        print(f"[ERROR] Invalid instance_id. Please choose from: {', '.join(available_instance_ids)}")


# Cleanup
gateway.close()
print("Disconnected and finished.")