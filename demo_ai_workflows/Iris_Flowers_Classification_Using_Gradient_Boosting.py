"""
Iris Flowers Classification Using Gradient Boosting

This script showcases the setup and execution of a ProActive scheduler job aimed at classifying Iris flower species using Gradient Boosting. The workflow includes various stages such as dataset loading, data splitting, model training, and prediction, with each stage implemented as a dedicated ProActive task. These tasks are structured to run sequentially, forming a comprehensive classification pipeline.

Workflow Details:
- Load_Iris_Dataset: Retrieves the Iris dataset, which includes features of Iris flowers along with their species, serving as the basis for the classification task.
- Split_Data: Divides the dataset into training and testing subsets, a crucial step for validating the model's classification accuracy.
- Gradient_Boosting: Initializes the Gradient Boosting classifier, a powerful ensemble learning method that builds models sequentially to correct errors of previous models, leading to improved classification accuracy.
- Train_Model: Trains the Gradient Boosting classifier using the training data, fine-tuning it to distinguish between different Iris flower species based on their features.
- Download_Model: Enables the trained model to be downloaded for use outside the ProActive platform or for additional analyses.
- Predict_Model: Utilizes the trained model to classify Iris flowers in the test subset, assessing the model's effectiveness in species identification.
- Preview_Results: Provides a preliminary view of the classification results, offering insight into the performance of the Gradient Boosting classifier in accurately identifying Iris flower species.

The script leverages 'proactive' for effortless connection to the ProActive gateway, ensuring smooth job orchestration and execution. Following job completion, it guarantees a clean disconnection and shutdown of the gateway, maintaining system and resource integrity.

Note: It's essential to have the ProActive Python client and necessary dependencies installed, and ensure the ProActive server is accessible before running the script.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob()
job.setJobName("Iris_Flowers_Classification_Using_Gradient_Boosting")

print("Getting the ai-machine-learning bucket")
bucket = gateway.getBucket("ai-machine-learning")

# ------------------------------------------------------------------------

print("Creating the Load_Iris_Dataset task...")
load_iris_dataset_task = bucket.create_Load_Iris_Dataset_task()
job.addTask(load_iris_dataset_task)

print("Creating the Split_Data task...")
split_data_task = bucket.create_Split_Data_task()
split_data_task.addDependency(load_iris_dataset_task)
job.addTask(split_data_task)

print("Creating the Gradient_Boosting task...")
gradient_boosting_task = bucket.create_Gradient_Boosting_task()
job.addTask(gradient_boosting_task)

print("Creating the Train_Model task...")
train_model_task = bucket.create_Train_Model_task()
train_model_task.addDependency(split_data_task)
train_model_task.addDependency(gradient_boosting_task)
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
