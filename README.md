# Proactive Python Client Examples

This repository contains a collection of example scripts that demonstrate various features of the proactive Python client. These scripts showcase how to create and manage jobs, tasks, and use advanced scheduling features in a Python environment.

## Summary

- [Proactive Python Client Examples](#proactive-python-client-examples)
  - [Summary](#summary)
  - [Setting Up the Environment](#setting-up-the-environment)
    - [Creating a Virtual Environment (Optional)](#creating-a-virtual-environment-optional)
      - [On Mac and Linux](#on-mac-and-linux)
      - [On Windows](#on-windows)
    - [Upgrading Required Packages](#upgrading-required-packages)
      - [On Mac and Linux](#on-mac-and-linux-1)
      - [On Windows](#on-windows-1)
  - [Installing the Proactive Python SDK](#installing-the-proactive-python-sdk)
    - [Using Makefile (For Mac and Linux)](#using-makefile-for-mac-and-linux)
    - [On Windows](#on-windows-2)
  - [Running the Examples](#running-the-examples)
    - [Using Makefile (For Mac and Linux)](#using-makefile-for-mac-and-linux-1)
    - [On Windows](#on-windows-3)
  - [Examples Description](#examples-description)
  - [Leveraging Pre-built AI Tasks from Proactive AI Orchestration](#leveraging-pre-built-ai-tasks-from-proactive-ai-orchestration)
    - [Machine Learning Workflows](#machine-learning-workflows)
  - [Advanced Examples](#advanced-examples)
    - [CIFAR-10 Logistic Regression Classifier](#cifar-10-logistic-regression-classifier)
  - [Additional Information](#additional-information)
  - [Contributing](#contributing)

## Setting Up the Environment

Before running the examples, you may want to create a virtual environment to avoid conflicts with other Python projects. A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages.

### Creating a Virtual Environment (Optional)

#### On Mac and Linux

To create a virtual environment, run the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

You can also use the provided `Makefile`:

```bash
make virtualenv
```

#### On Windows

On Windows, you can use the provided `build.bat` script to create and manage the virtual environment:

```cmd
build.bat VIRTUAL_ENV
```

This command will create a new virtual environment or use the existing one based on your input.

### Upgrading Required Packages

Once the virtual environment is activated, upgrade `pip`, `setuptools` and `python-dotenv` to the latest versions:

#### On Mac and Linux

```bash
python3 -m pip install --upgrade pip setuptools python-dotenv
```

If you have used the provided `Makefile`, it automatically upgrades these packages when setting up the virtual environment.

#### On Windows

The `build.bat` script automatically upgrades these packages when setting up the virtual environment.

## Installing the Proactive Python SDK

To install the latest pre-release or development version of the Proactive Python SDK, which includes the most recent features and fixes, use the following command:

```bash
python3 -m pip install --upgrade --pre proactive
```

The `--pre` flag is included to allow pip to find and install pre-releases.

### Using Makefile (For Mac and Linux)

```bash
make install_latest
```

### On Windows

```cmd
build.bat INSTALL_LATEST
```

## Running the Examples

To test if the installation was successful and see the proactive client in action, you can run the provided example scripts. For instance, to run the `demo_basic.py` script:

```bash
python3 demo_basic.py
```

### Using Makefile (For Mac and Linux)

For instance, to run all the provided example scripts:

```bash
make run_all
```

### On Windows

To run all the provided example scripts:

```cmd
build.bat RUN_ALL
```

This command will execute all `.py` files in the current directory.

## Examples Description

- `demo_basic.py`: A simple script that showcases how to connect to the ProActive Scheduler, create a job and a Python task, and execute it.

- `demo_pre_post_script.py`: Illustrates adding pre-scripts and post-scripts to tasks for setup and cleanup. Enhances task flexibility by allowing pre and post execution actions. Ideal for complex setups or post-task data handling.

- `demo_job_task_var.py`: Demonstrates the use of job and task-level variables within the ProActive Scheduler. This script highlights how to define and access variables that can be shared across tasks within a job, facilitating dynamic task configuration and the passing of data between tasks. It showcases setting variables at both the job and individual task levels, and accessing these variables within task implementations for flexible, dynamic workflow execution.

- `demo_global_var.py`: Demonstrates the use of global variables between tasks in ProActive Scheduler. It exemplifies creating and managing jobs and tasks with a focus on inter-task communication via global variables.

- `demo_task_result.py`: Highlights job submission with task dependencies and result handling, showing how to create tasks that process and utilize the results of preceding tasks.

- `demo_task_dependency.py`: Illustrates how to manage task dependencies within the ProActive Scheduler. It demonstrates creating a series of tasks with specific execution orders, showcasing the scheduler's capability to handle complex dependencies. This example provides insights into structuring a job where tasks execute sequentially or in parallel, based on their dependencies, ensuring that dependent tasks wait for their predecessors to complete before starting.

- `demo_multilanguage_job.py`: Showcases the creation and submission of a multi-language job (Python and Groovy tasks), emphasizing the scheduler's support for diverse programming languages within a single job.

- `demo_job_status.py`: Demonstrates the process of job submission and monitoring with the ProActive Python SDK. It walks through creating a job, adding a Python task, submitting the job to the ProActive Scheduler, and monitoring its status until completion, concluding with the retrieval and display of the job's output.

- `demo_impl_file.py`: Demonstrates the basic usage of the ProActive Scheduler for executing a Python task implemented in an external file.

- `demo_impl_url.py`: Illustrates how to set up a machine learning task (Logistic Regression) using a script sourced from a URL, showing the ProActive Scheduler's capability to incorporate external scripts.

- `demo_exec_file.py`: Demonstrates how to execute a Python task using a script sourced from an external file. This script is designed to illustrate the process of configuring and submitting a ProActive Scheduler task where the task's implementation is defined in an external Python file, showcasing how to incorporate external Python scripts into ProActive Scheduler jobs for flexible and modular task execution.

- `demo_dataspace_api.py`: Demonstrates managing data transfers between local spaces and the ProActive Scheduler's data spaces (user and global), using the ProActive Python Client.

- `demo_transf_file.py`: Demonstrates file handling in ProActive tasks, focusing on including input files for processing and designating output files to capture task results. This script counts the number of files in a specified directory and outputs the count both to the terminal and to a file within the same directory, showcasing data transfer and file management in ProActive workflows.

- `demo_python_module.py`: Demonstrates how to execute Python tasks that depend on custom Python modules or external libraries, demonstrating the ProActive Scheduler's support for complex Python environments and dependencies.

- `demo_forkenv.py`: Shows how to create and execute a Python task within a job, with emphasis on configuring the execution environment using a fork environment script.

- `demo_runtimeenv.py`: Demonstrates the process of executing a Python task within the ProActive Scheduler, emphasizing the configurability of the task's execution environment. It demonstrates establishing a connection to the scheduler, creating a job, and configuring a Python task to run within a specified container environment. This example highlights the scheduler's flexibility in executing tasks in varied and complex runtime settings.

- `demo_selectionscript.py`: This script explains how to create a job and a task, and ensures that the task is executed only on Linux machines using a selection script.

- `demo_loop.py`: Illustrates loop control flow within a ProActive Scheduler job, demonstrating how to create loops within jobs for repeated task execution based on dynamic conditions.

- `demo_replicate.py`: Demonstrates replication and merge flow with Python Tasks. This script showcases the creation and execution of a ProActive Job designed to demonstrate replication and merge control flows.

- `demo_branch.py`: Demonstrates branching logic within ProActive Scheduler jobs, illustrating how to implement conditional task execution paths based on dynamic criteria.

- `demo_3controls.py`: Combines replication, iteration, and branching for advanced job workflows. Demonstrates the scheduler's capability for sophisticated task management. Enables complex computational workflows with parallel execution and conditional logic.

- `demo_ai_workflow.py`: Sets up and executes a machine learning workflow for the Iris dataset using the ProActive Scheduler. It demonstrates how to create a job, add tasks, and manage their execution sequence.

Additional scripts found in the `demo_ai_workflows` directory showcase various machine learning workflows, leveraging the ProActive Scheduler for tasks like data preprocessing, model training, evaluation, and prediction across different datasets and using various algorithms.

Please ensure the ProActive Scheduler is running and accessible, and that you have the required scripts and environments set up before executing these examples.

## Leveraging Pre-built AI Tasks from Proactive AI Orchestration

This section of the repository showcases advanced examples that leverage the powerful capabilities of the Proactive AI Orchestration platform, specifically utilizing tasks from the `ai-machine-learning` bucket. The `ai-machine-learning` bucket is a comprehensive collection of generic machine learning tasks, designed to facilitate the seamless composition of workflows for the learning and testing of predictive models. These tasks are highly versatile and can be tailored to meet specific requirements, enabling users to effortlessly integrate and execute sophisticated machine learning models and workflows.

Each example demonstrates the practical application of these pre-built tasks, offering insights into how they can be customized and combined to create complex machine learning solutions. Whether you're looking to add new tasks or modify existing ones, the `ai-machine-learning` bucket provides a flexible framework that supports a wide range of machine learning activities, from data preprocessing and model training to evaluation and inference.

For detailed information on how to customize the `ai-machine-learning` bucket to suit your unique needs, and to explore the full range of tasks and capabilities it offers, please refer to the [Proactive AI Orchestration User Guide](https://trydev2.activeeon.com/doc/PAIO/PAIOUserGuide.html).

### Machine Learning Workflows

- **Diabetics Detection**: Utilizes various machine learning algorithms to detect diabetic patients from clinical datasets.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_AutoSklearn_Classifier`: Detects diabetes using the Auto-sklearn Classifier.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_Isolation_Forest`: Applies Isolation Forest for anomaly detection in diabetes data.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_K_Means`: Employs K-Means clustering for diabetes data segmentation.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_Mean_Shift`: Uses Mean Shift clustering for diabetes data analysis.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_One_Class_SVM`: Implements One-Class SVM for outlier detection in diabetes datasets.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_TPOT_Classifier`: Leverages the TPOT Classifier for automated machine learning in diabetes detection.

- **House Price Prediction**: Demonstrates the use of various regression models to predict house prices based on the Boston housing dataset.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_AutoSklearn_Regressor`: Predicts house prices using Auto-sklearn Regressor.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Bayesian_Ridge_Regression`: Applies Bayesian Ridge Regression for house price prediction.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Linear_Regression`: Utilizes Linear Regression for predicting house prices.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Support_Vector_Regression`: Employs Support Vector Regression for house price estimation.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_TPOT_Regressor`: Uses the TPOT Regressor for automated machine learning in house price prediction.

- **Iris Flowers Classification**: Showcases classification models for identifying Iris flower species from the Iris dataset.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_AdaBoost`: Classifies Iris species using AdaBoost.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_CatBoost`: Implements CatBoost for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Gaussian_Naive_Bayes`: Utilizes Gaussian Naive Bayes for classifying Iris species.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Gradient_Boosting`: Applies Gradient Boosting for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Logistic_Regression`: Uses Logistic Regression for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Random_Forest`: Employs Random Forest for classifying Iris species.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Support_Vector_Machines`: Demonstrates SVM usage for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_XGBoost`: Leverages XGBoost for Iris species classification.

## Advanced Examples

The repository also includes a collection of advanced examples that demonstrate more complex use cases of the ProActive Scheduler, particularly focusing on machine learning workflows. These examples illustrate how to set up, configure, and execute sophisticated machine learning models and workflows using the ProActive Python client.

### CIFAR-10 Logistic Regression Classifier

The [CIFAR-10 Logistic Regression Classifier](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) example demonstrates how to train and evaluate a logistic regression model on the CIFAR-10 dataset, which is a common benchmark in machine learning for image classification tasks.

- **Repository Contents**: The repository includes:

- Scripts for training and evaluating the model (`train.py` and `eval.py`).
- A directory structure to organize models and predictions.
- A sample script (`submit2proactive.py`) to submit a job to the ProActive Scheduler, showing how to run complex machine learning workflows on distributed computing environments.

- **Getting Started**: To explore this advanced example, visit the [repository](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) and follow the instructions provided in its `README` to set up your environment, train the model, and submit the job to ProActive.

Please ensure that your environment meets the prerequisites and that the ProActive Scheduler is running and accessible before you begin.

## Additional Information

- Ensure you have Python 3.6 or later to use the proactive client.
- If you encounter any issues, please report them on the [Issues](https://github.com/ow2-proactive/proactive-python-client-examples/issues) page.
- For more information about the proactive client, refer to the [official documentation](https://github.com/ow2-proactive/proactive-python-client).

## Contributing

We welcome contributions to this repository. If you have an improvement or a new example, please fork the repository, make your changes, and submit a pull request.
