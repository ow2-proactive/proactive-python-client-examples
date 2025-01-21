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
pre_script = gateway.createPreScript(ProactiveScriptLanguage().linux_bash())
pre_script.setImplementation("""
EXTERNAL_IP=$(curl -s ifconfig.me)
FLASK_PORT=5000
echo "Flask app will run on: $EXTERNAL_IP:$FLASK_PORT"
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
