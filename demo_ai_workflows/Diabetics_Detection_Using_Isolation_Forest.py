"""
Diabetics Detection Using Isolation Forest

This script demonstrates the process of creating and submitting a job to ProActive scheduler for detecting diabetics using an Isolation Forest model. It involves several steps including data import, data splitting, model training, and prediction. Each step is encapsulated in a ProActive task, orchestrated to execute in a specific order to achieve the desired workflow.

- Import_Data: Imports the dataset for analysis.
- Split_Data: Splits the dataset into training and testing subsets.
- Isolation_Forest: Prepares the Isolation Forest algorithm for anomaly detection.
- Train_Model: Trains the Isolation Forest model with the training subset.
- Download_Model: Downloads the trained model for local use or future predictions.
- Predict_Model: Uses the trained model to predict outcomes on the testing subset.
- Preview_Results: Provides a preview of the prediction results.

The script uses the 'proactive' module to connect to the ProActive gateway and manage the job submission and execution process. It ensures clean disconnection and termination of the gateway after the job execution.

Ensure that the ProActive Python client and necessary dependencies are installed and that the ProActive server is accessible.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob()
job.setJobName("Diabetics_Detection_Using_Isolation_Forest")

print("Getting the ai-machine-learning bucket")
bucket = gateway.getBucket("ai-machine-learning")

# ------------------------------------------------------------------------

print("Creating the Import_Data task...")
import_data_dataset_task = bucket.create_Import_Data_task()
job.addTask(import_data_dataset_task)

print("Creating the Split_Data task...")
split_data_task = bucket.create_Split_Data_task()
split_data_task.addDependency(import_data_dataset_task)
job.addTask(split_data_task)

print("Creating the Isolation_Forest task...")
isolation_forest_task = bucket.create_Isolation_Forest_task()
job.addTask(isolation_forest_task)

print("Creating the Train_Model task...")
train_model_task = bucket.create_Train_Model_task()
train_model_task.addDependency(split_data_task)
train_model_task.addDependency(isolation_forest_task)
job.addTask(train_model_task)

print("Creating the Download_Model task...")
download_model_task = bucket.create_Download_Model_task()
download_model_task.addDependency(train_model_task)
job.addTask(download_model_task)

print("Creating the Predict_Model task...")
predict_model_task = bucket.create_Predict_Model_task()
predict_model_task.addDependency(split_data_task)
predict_model_task.addDependency(train_model_task)
job.addTask(predict_model_task)

print("Creating the Preview_Results task...")
preview_results_task = bucket.create_Preview_Results_task()
preview_results_task.addDependency(predict_model_task)
job.addTask(preview_results_task)

# ------------------------------------------------------------------------

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

gateway.close()
print("Disconnected and finished.")
