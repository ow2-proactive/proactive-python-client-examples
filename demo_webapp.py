"""
Interactive Data Editing Pipeline Using Flask and ProActive Scheduler

This script demonstrates the creation of a multi-step interactive pipeline using the ProActive Scheduler 
and a Flask web application for real-time user input. Key features include:

1. Establishing a connection with the ProActive Scheduler using the getProActiveGateway function.
2. Creating a job named "demo_pipeline_job" to manage and execute a series of Python tasks.
3. Defining a pipeline of three tasks:
   - Load_Data: Generates a dataframe and stores it in ProActive variables for use in subsequent tasks.
   - Flask_App: Launches a Flask-based web application, allowing users to view and edit the dataframe interactively.
   - Display_Final_Dataframe: Outputs the final dataframe after modifications made in the Flask application.
4. Passing data between tasks using ProActive variables, enabling seamless communication across the pipeline.
5. Leveraging task dependencies to ensure correct execution order, with the Flask application task dependent on the dataframe creation task.
6. Utilizing the ProActive Scheduler's job submission capabilities to execute the defined workflow.
7. Fetching and displaying the job's output upon completion for validation and debugging.

This script highlights how the ProActive Scheduler can be used to create complex, interactive workflows 
with integrated user input. It demonstrates the scheduler's flexibility in managing both automated and 
interactive tasks, providing a foundation for developing robust computational pipelines.
"""
from proactive import getProActiveGateway
import json
# Initialize the ProActive gateway
gateway = getProActiveGateway()
# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_pipeline_job")
# Task 1: Load data into a dataframe
print("Creating Task 1: Load data into a dataframe...")
task1 = gateway.createPythonTask("Load_Data")
task1.setTaskImplementation("""
import pandas as pd
# Create a simple dataframe
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)
# Save the dataframe to a JSON string to pass it to the next task
variables.put("dataframe_json", df.to_json())
print("Dataframe created and passed to Task 2.")
""")
task1.setDefaultPython("/usr/bin/python3")
task1.setVirtualEnv(requirements=['pandas'])
# Task 2: Start a Flask application
print("Creating Task 2: Flask application for editing...")
task2 = gateway.createPythonTask("Flask_App")
task2.setTaskImplementation("""
import pandas as pd
import threading
from flask import Flask, request, render_template_string
import os
# Load the dataframe passed from Task 1
dataframe_json = variables.get("dataframe_json")
df = pd.read_json(dataframe_json)
# Flask application
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    global df
    # Render a simple HTML page to display and edit the dataframe
    html_template = '''
    <h1>Dataframe Viewer and Editor</h1>
    <form method="POST" action="/update">
        <textarea name="dataframe" rows="10" cols="50">{{ dataframe }}</textarea><br>
        <button type="submit" formaction="/continue">Continue</button>
        <button type="submit" formaction="/stop">Stop</button>
    </form>
    '''
    return render_template_string(html_template, dataframe=df.to_json())
@app.route('/update', methods=['POST'])
def update():
    global df
    try:
        # Retrieve the updated dataframe JSON from the form
        updated_data = request.form['dataframe']
        # Parse the updated JSON and update the dataframe
        df = pd.read_json(updated_data)
        print("Dataframe successfully updated:", df)
        # Reload the page to display the updated dataframe
        return index()
    except Exception as e:
        print("Error updating dataframe:", e)
        return f"Error updating dataframe: {e}", 400
@app.route('/continue', methods=['POST'])
def continue_pipeline():
    global df
    try:
        # Retrieve the updated JSON from the form
        updated_data = request.form['dataframe']
        # Parse the updated JSON and update the dataframe
        df = pd.read_json(updated_data)
        print("Updated dataframe reloaded in Task 2:")
        print(df)
        # Save the updated dataframe to ProActive variables
        variables.put("dataframe_json", df.to_json())
        print("Updated dataframe passed to Task 3.")
        # Display confirmation and the updated dataframe
        html_response = f'''
        <h1>Data saved and pipeline will continue.</h1>
        <h2>Updated Dataframe:</h2>
        <pre>{df.to_string(index=False)}</pre>
        '''
        return html_response, 200
    except Exception as e:
        print("Error in continue_pipeline:", e)
        return f"Error in continue_pipeline: {e}", 400
@app.route('/stop', methods=['POST'])
def stop_pipeline():
    print("User clicked Stop. Terminating pipeline.")
    # Send a response before shutting down
    return "Pipeline terminated. You can close this page now.", 200
# Flask shutdown utility
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
@app.after_request
def shutdown_if_requested(response):
    if request.endpoint in ['stop_pipeline']:
        shutdown_server()
    return response
# Start Flask app in a separate thread
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)
print("Starting Flask application...")
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()
""")
task2.setDefaultPython("/usr/bin/python3")
task2.setVirtualEnv(requirements=['pandas', 'flask'])
# Task 3: Display the final dataframe
print("Creating Task 3: Display final dataframe...")
task3 = gateway.createPythonTask("Display_Final_Dataframe")
task3.setTaskImplementation("""
import pandas as pd
# Load the dataframe passed from Task 2
dataframe_json = variables.get("dataframe_json")
if not dataframe_json:
    print("Error: No dataframe_json found in variables!")
else:
    print("Dataframe JSON received in Task 3:", dataframe_json)
df = pd.read_json(dataframe_json)
# Display the dataframe
print("Final dataframe:")
print(df)
""")
task3.setDefaultPython("/usr/bin/python3")
task3.setVirtualEnv(requirements=['pandas'])
# Add dependencies to create a pipeline
print("Linking tasks...")
job.addTask(task1)
job.addTask(task2)
job.addTask(task3)
task2.addDependency(task1)
task3.addDependency(task2)
# Submit the job
print("Submitting the job to the ProActive Scheduler...")
job_id = gateway.submitJob(job)
print("Job submitted with ID: " + str(job_id))
# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)
# Cleanup
gateway.close()
print("Disconnected and finished.")