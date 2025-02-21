"""
Interactive Data Editing Pipeline Using Flask and ProActive Scheduler

This script demonstrates the creation of a multi-step interactive pipeline using the ProActive Scheduler 
and a Flask web application for real-time user input. Key features include:

1. Establishing a connection with the ProActive Scheduler using the getProActiveGateway function.
2. Creating a job named "demo_webapp_job" to manage and execute a series of Python tasks.
3. Defining a pipeline of three tasks:
   - Load_Data: Generates a dataframe and stores it in ProActive variables for use in subsequent tasks.
   - Flask_App: Launches a Flask-based web application, allowing users to view and edit the dataframe interactively.
   - Display_Final_Dataframe: Outputs the final dataframe after modifications made in the Flask application.
4. Passing data between tasks using ProActive variables, enabling seamless communication across the pipeline.
5. Leveraging task dependencies to ensure correct execution order, with the Flask application task dependent on the dataframe creation task.
6. Utilizing a prescript in Task 2 to retrieve and store the external IP address of the execution node, demonstrating dynamic runtime information retrieval.
7. Implementing a user-controlled workflow mechanism in Task 2:
   - Users can click "Continue" to proceed to Task 3.
   - Users can click "Stop" to cancel Task 2, which fails the task and stops the entire workflow, ensuring no further execution.
8. Utilizing the ProActive Scheduler's job submission capabilities to execute the defined workflow.
9. Fetching and displaying the job's output upon completion for validation and debugging.
"""

from proactive import getProActiveGateway, ProactiveScriptLanguage

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_webapp")

# Task 1: Load data into a dataframe
print("Creating Task 1: Load data into a dataframe...")
task1 = gateway.createPythonTask("Load_Data")
task1.setTaskImplementation("""
import os
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
task2.setTaskErrorPolicy("cancelJob")

# Add a pre-script to get the external IP address and port
print("Adding a pre-script to Task 2...")
pre_script = gateway.createPreScript(ProactiveScriptLanguage().groovy())
pre_script.setImplementation("""
import java.net.URL

def getExternalIP() {
    def url = new URL("https://api.ipify.org")
    return url.getText()
}

def externalIP = getExternalIP()
def flaskPort = 5000

println "Flask app is running on: ${externalIP}:${flaskPort}"

// Connect to the scheduler
schedulerapi.connect()

// Add an external endpoint URL for the Flask application
def flaskUrl = "http://${externalIP}:${flaskPort}"
schedulerapi.addExternalEndpointUrl(
    variables.get("PA_JOB_ID"),
    "flask-app",
    flaskUrl,
    "https://cdn-icons-png.flaticon.com/128/5968/5968350.png"  // Flask icon
)
""")
task2.setPreScript(pre_script)

task2.setTaskImplementation("""
import os
import threading
import pandas as pd
from flask import Flask, request, render_template_string

# Load the dataframe passed from Task 1
dataframe_json = variables.get("dataframe_json")
df = pd.read_json(dataframe_json)

# Flask application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    global df
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
        updated_data = request.form['dataframe']
        df = pd.read_json(updated_data)
        print("Dataframe successfully updated:", df)
        return index()
    except Exception as e:
        print("Error updating dataframe:", e)
        return f"Error updating dataframe: {e}", 400

@app.route('/continue', methods=['POST'])
def continue_pipeline():
    global df
    try:
        updated_data = request.form['dataframe']
        df = pd.read_json(updated_data)
        variables.put("dataframe_json", df.to_json())
        print("Updated dataframe passed to Task 3.")
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
    print("User clicked Stop. Task 2 is canceled, and the workflow will not proceed.")
    from flask import Response
    import os
    import sys

    sys.stderr = open(os.devnull, 'w')

    response = Response(
        "User has stopped the workflow. Task 2 has been canceled and the rest of the workflow will not be executed.",
        status=200,
        mimetype="text/plain"
    )

    response.call_on_close(lambda: os._exit(1))
    return response

# Flask shutdown utility
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()

@app.after_request
def shutdown_if_requested(response):
    if request.endpoint in ['continue_pipeline', 'stop_pipeline']:
        shutdown_server()
        schedulerapi.connect()
        # Remove an endpoint
        schedulerapi.removeExternalEndpointUrl(variables.get("PA_JOB_ID"), "flask-app")
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
task2.addDependency(task1)

# Task 3: Display the final dataframe
print("Creating Task 3: Display final dataframe...")
task3 = gateway.createPythonTask("Display_Final_Dataframe")
task3.setTaskImplementation("""
import pandas as pd

dataframe_json = variables.get("dataframe_json")
if not dataframe_json:
    print("Error: No dataframe_json found in variables!")
else:
    df = pd.read_json(dataframe_json)
    print("Final dataframe:")
    print(df)
""")
task3.setDefaultPython("/usr/bin/python3")
task3.setVirtualEnv(requirements=['pandas'])
task3.addDependency(task2)

# Add tasks to the job
print("Linking tasks...")
job.addTask(task1)
job.addTask(task2)
job.addTask(task3)

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
