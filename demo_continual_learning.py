"""
Continual Learning Demo with ProActive Scheduler

This script demonstrates how to implement a continual learning workflow using the ProActive Scheduler. 
It creates a job with two main tasks that loop for multiple iterations:

1. Data Generation Task:
   - Generates synthetic classification data using scikit-learn
   - Stores the generated data as variables for the next task

2. Incremental Learning Task:
   - Retrieves the generated data
   - Initializes or loads an SGDClassifier model
   - Performs partial fitting on the new data
   - Evaluates the model's current accuracy
   - Stores the updated model for the next iteration

Key features:
- Uses ProActive's flow control to create a loop between tasks
- Demonstrates how to use virtual environments for task-specific dependencies
- Shows how to pass data and model states between iterations using ProActive variables
- Illustrates the use of flow blocks to define task dependencies

This example showcases how ProActive can be used to orchestrate machine learning workflows,
particularly those involving continuous or incremental learning processes.
"""
from proactive import getProActiveGateway, ProactiveFlowBlock, ProactiveScriptLanguage

# Connect to the ProActive Scheduler
gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("ContinualLearningJob")

# Task 1: Data Generation
print("Creating data generation task...")
data_gen_task = gateway.createPythonTask("DataGeneration")
data_gen_task.setFlowBlock(ProactiveFlowBlock().start())
data_gen_task.setTaskImplementation("""
import numpy as np
from sklearn.datasets import make_classification

def generate_batch(batch_size=100, n_features=10):
    X, y = make_classification(n_samples=batch_size, n_features=n_features, n_classes=2, random_state=None)
    return X, y

# Generate initial batch
X, y = generate_batch()

# Store the data as variables
variables.put("X", X.tolist())
variables.put("y", y.tolist())
print("Generated batch of data with shape:", X.shape)
""")
data_gen_task.setVirtualEnv(requirements=['scikit-learn', 'pickle'], basepath='/shared/', name='continual_learning_env')

# Task 2: Incremental Learning
print("Creating incremental learning task...")
learning_task = gateway.createPythonTask("IncrementalLearning")
learning_task.setFlowBlock(ProactiveFlowBlock().end())
learning_task.addDependency(data_gen_task)
learning_task.setTaskImplementation("""
import numpy as np
from sklearn.linear_model import SGDClassifier
import pickle

# Retrieve the data
X = np.array(variables.get("X"))
y = np.array(variables.get("y"))

# Initialize the model (or load if exists)
try:
    model_pickle = variables.get("model_pickle")
    if model_pickle is not None:
        model = pickle.loads(model_pickle)
        print("Loaded existing model")
    else:
        raise ValueError("No existing model found")
except:
    print("Initializing new model")
    model = SGDClassifier(loss="log", random_state=42)

# Partial fit
model.partial_fit(X, y, classes=np.unique(y))

# Evaluate
accuracy = model.score(X, y)
print(f"Current model accuracy: {accuracy:.4f}")

# Store the updated model
model_pickle = pickle.dumps(model)
variables.put("model_pickle", model_pickle)
print("Model stored successfully")

# Get the current iteration
iteration = variables.get("PA_TASK_ITERATION")
print(f"Completed iteration {iteration}")
""")
learning_task.setVirtualEnv(requirements=['scikit-learn', 'pickle'], basepath='/shared/', name='continual_learning_env')

# Define the loop criteria script
loop_script = """
i = int(variables.get('PA_TASK_ITERATION'))
if i < 5:  # Run for 5 iterations
    loop = True
else:
    loop = False
"""
# Create the loop flow between the data_gen_task and learning_task tasks
flow_script = gateway.createLoopFlowScript(loop_script, data_gen_task.getTaskName(), script_language=ProactiveScriptLanguage().python())
# Associate the loop flow script to the learning_task task
learning_task.setFlowScript(flow_script)

# Add tasks to the job
job.addTask(data_gen_task)
job.addTask(learning_task)

# Submit the job
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("Job submitted with ID:", job_id)

# Wait for the job to complete and print the output
print("Waiting for job completion...")
job_output = gateway.getJobOutput(job_id)
print("Job output:")
print(job_output)

# Disconnect from the gateway
gateway.close()
print("Disconnected and finished.")