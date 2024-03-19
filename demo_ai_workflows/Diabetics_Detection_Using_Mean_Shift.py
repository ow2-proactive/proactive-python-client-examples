"""
Diabetics Detection Using Mean Shift

This script outlines the process for setting up and submitting a job to the ProActive scheduler, aimed at detecting diabetes using the Mean Shift clustering algorithm. The workflow comprises several stages, including data importation, data segmentation, model training, and prediction, with each phase encapsulated within a ProActive task. These tasks are orchestrated to execute in a predefined order, facilitating the intended workflow.

Workflow Stages:
- Import_Data: Introduces the dataset into the analytical process.
- Split_Data: Divides the dataset into training and testing subsets, enabling a thorough evaluation of the model's performance.
- Mean_Shift: Initializes the Mean Shift algorithm, preparing it for the clustering-based identification of patterns within the dataset.
- Train_Model: Trains the Mean Shift model using the training data, optimizing it to effectively pinpoint diabetic indicators.
- Download_Model: Allows for the download of the trained model, making it available for offline use or further predictions.
- Predict_Model: Applies the trained model to make predictions on the test data, assessing the model's accuracy and efficacy.
- Preview_Results: Provides an initial glimpse into the prediction results, offering insights into the model's diagnostic capabilities.

The script utilizes 'proactive' for seamless connectivity to the ProActive gateway, overseeing the job's orchestration and execution. Post-execution, it ensures a clean disconnection and termination of the gateway, maintaining system integrity.

Before running the script, ensure the ProActive Python client and necessary dependencies are installed and that the ProActive server is accessible.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob()
job.setJobName("Diabetics_Detection_Using_Mean_Shift")

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

print("Creating the Mean_Shift task...")
mean_shift_task = bucket.create_Mean_Shift_task()
job.addTask(mean_shift_task)

print("Creating the Train_Model task...")
train_model_task = bucket.create_Train_Model_task()
train_model_task.addDependency(split_data_task)
train_model_task.addDependency(mean_shift_task)
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