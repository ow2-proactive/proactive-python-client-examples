# Proactive Python Client Examples

This repository contains a collection of example scripts that demonstrate various features of the proactive Python client. These scripts showcase how to create and manage jobs, tasks, and use advanced scheduling features in a Python environment.

## Setting Up the Environment

Before running the examples, you may want to create a virtual environment to avoid conflicts with other Python projects. A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages.

### Creating a Virtual Environment (Optional)

To create a virtual environment, run the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

### Upgrading Required Packages

Once the virtual environment is activated, upgrade `pip` and `setuptools` to the latest versions:

```bash
python3 -m pip install --upgrade pip setuptools
```

### Installing Dependencies

Install the required packages listed in `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

## Installing the Proactive Python SDK

To install the latest pre-release or development version of the Proactive Python SDK, which includes the most recent features and fixes, use the following command:

```bash
python3 -m pip install --pre proactive
```

The `--pre` flag is included to allow pip to find and install pre-releases.

## Running the Examples

To test if the installation was successful and see the proactive client in action, you can run the provided example scripts. For instance, to run the `demo_basic.py` script:

```bash
python3 demo_basic.py
```

## Examples Description

- `demo_basic.py`: A simple script that showcases how to connect to the ProActive Scheduler, create a job and a Python task, and execute it.

- `demo_impl_file.py`: Demonstrates the basic usage of the ProActive Scheduler for executing a Python task implemented in an external file.

- `demo_exec_file.py`: This advanced script runs a Python task from a file with input files, pre-scripts, and post-scripts. It highlights the ability to execute complex scripts with external dependencies.

- `demo_forkenv.py`: Shows how to create and execute a Python task within a job, with emphasis on configuring the execution environment using a fork environment script.

- `demo_selectionscript.py`: This script explains how to create a job and a task, and ensures that the task is executed only on Linux machines using a selection script.

- `demo_impl_url.py`: Illustrates how to set up a machine learning task (Logistic Regression) using a script sourced from a URL, showing the ProActive Scheduler's capability to incorporate external scripts.

- `demo_ai_workflow.py`: Sets up and executes a machine learning workflow for the Iris dataset using the ProActive Scheduler. It demonstrates how to create a job, add tasks, and manage their execution sequence.

Please ensure the ProActive Scheduler is running and accessible, and that you have the required scripts and environments set up before executing these examples.

## Advanced Examples

In addition to the basic and intermediate examples provided in this repository, we also have an advanced set of examples that delve into more complex use cases of the ProActive Scheduler with machine learning workflows.

### CIFAR-10 Logistic Regression Classifier

The [CIFAR-10 Logistic Regression Classifier](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) example demonstrates how to train and evaluate a logistic regression model on the CIFAR-10 dataset, which is a common benchmark in machine learning for image classification tasks.

The repository includes:

- Scripts for training and evaluating the model (`train.py` and `eval.py`).
- A directory structure to organize models and predictions.
- A sample script (`submit2proactive.py`) to submit a job to the ProActive Scheduler, showing how to run complex machine learning workflows on distributed computing environments.

To explore this advanced example, visit the [repository](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) and follow the instructions provided in its `README` to set up your environment, train the model, and submit the job to ProActive.

Please ensure that your environment meets the prerequisites and that the ProActive Scheduler is running and accessible before you begin.

## Additional Information

- Ensure you have Python 3.6 or later to use the proactive client.
- If you encounter any issues, please report them on the [Issues](https://github.com/ow2-proactive/proactive-python-client-examples/issues) page.
- For more information about the proactive client, refer to the [official documentation](https://github.com/ow2-proactive/proactive-python-client).

## Contributing

We welcome contributions to this repository. If you have an improvement or a new example, please fork the repository, make your changes, and submit a pull request.
