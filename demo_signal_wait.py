"""
ProActive Signal API Demonstration

This script demonstrates the usage of the ProActive Scheduler Signal API to receive and handle signals.
The example encompasses the following steps:

- Initializing the ProActive Scheduler gateway.
- Creating a ProActive job.
- Creating a Groovy task that waits for signals with specified variables.
- Declaring that the current job is ready to receive and handle the 'Stop' and 'Continue' signals with the given variables (signal variables).
- Waiting until one of the signals 'Continue' or 'Stop' is sent (via the Workflow Execution portal, Scheduler portal, or REST API).
- Removing ready signals from the set of job signals.
- Displaying the received signal and its updated variables.
- Submitting the job to the ProActive Scheduler and retrieving the job ID.
- Ensuring proper cleanup by disconnecting from the ProActive Scheduler gateway post-execution.

Documentation:
- https://doc.activeeon.com/latest/javadoc/org/ow2/proactive/scheduler/signal/Signal.html
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_signal_wait_job")

# Create a Groovy task for waiting for signals with variables
signal_task = gateway.createTask("groovy", "wait_for_signals_with_variables")

# Set the Groovy task implementation
signal_task.setTaskImplementation(""" 
import com.google.common.base.Splitter;
import org.ow2.proactive.scheduler.common.job.JobVariable;

// Define signal variables
List<JobVariable> signalVariables = new java.util.ArrayList<JobVariable>()
signalVariables.add(new JobVariable("INTEGER_VARIABLE", "12", "PA:INTEGER", "Put here a description of the Signal Variable. It will be displayed to the Users when sending the Signal.", "", false, false))
signalVariables.add(new JobVariable("LIST_VARIABLE", "True", "PA:LIST(True,False)", "Put here a description of the Signal Variable. It will be displayed to the Users when sending the Signal.", "Group", true, false))
signalVariables.add(new JobVariable("BOOLEAN_VARIABLE", "true", "PA:Boolean", "Put here a description of the Signal Variable. It will be displayed to the Users when sending the Signal.", "", true, false))

// Read the variable SIGNALS
signals = "Stop, Continue"

// Split the value of the variable SIGNALS and transform it into a list
Set signalsSet = new HashSet<>(Splitter.on(',').trimResults().omitEmptyStrings().splitToList(signals))

// Send a ready notification for each signal in the set
println("Ready for signals "+ signalsSet)
signalsSet.each { signal ->
    if(signal.equals("Stop")) {
		signalapi.readyForSignal(signal);
	} else {
		signalapi.readyForSignal(signal, signalVariables)
	}
}

// Wait until one signal among those specified is received
println("Waiting for any signal among "+ signalsSet)
receivedSignal = signalapi.waitForAny(signalsSet)

// Remove ready signals
signalapi.removeManySignals(new HashSet<>(signalsSet.collect { signal -> "ready_"+signal }))

// Display the received signal and add it to the job result
println("Received signal: "+ receivedSignal)

println("Signal variables:")
def variables = receivedSignal.getUpdatedVariables().each{ k, v -> println "${k}:${v}" }

result = receivedSignal
""")

# Add the Groovy task to the job
job.addTask(signal_task)

# Submit the job to the ProActive scheduler
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

# Cleanup
gateway.close()
print("Disconnected and finished.")
