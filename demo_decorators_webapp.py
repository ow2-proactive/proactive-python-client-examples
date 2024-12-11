"""
Demonstrates Python Task Execution with a Flask-based Interactive Pipeline using ProActive Decorators

This script showcases the use of ProActive decorators to create and execute a series of Python tasks 
within the ProActive Scheduler, integrating an interactive Flask application into the workflow. 
Key features demonstrated include:

1. Utilizing the @task decorator to define Python tasks with dependencies, enabling structured task execution.
2. Using the @job decorator to encapsulate the tasks into a cohesive pipeline.
3. Including a Flask-based interactive task to allow users to view and edit a dataframe via a web interface.
4. Demonstrating how to pass data between tasks using ProActive variables, enabling dynamic task communication.
5. Enabling real-time updates to task outputs through the Flask web application.

The script defines three tasks:
- Load_Data: Creates a sample dataframe and stores it in ProActive variables for subsequent tasks.
- Flask_App: Launches a Flask web application to display and edit the dataframe interactively.
- Display_Final_Dataframe: Displays the final version of the dataframe after any user modifications.

These tasks are then organized into a workflow using the @job decorator, showcasing how ProActive can manage 
interactive and non-interactive task dependencies with minimal boilerplate code.

This example serves as a starting point for users to understand how ProActive decorators can be used to create 
computational pipelines with interactive user inputs and seamless task orchestration.
"""
from proactive.decorators import task, job

# Task 1: Load data into a dataframe
@task.python(name="Load_Data", virtual_env={"requirements": ["pandas"]})
def load_data():
    return """
import pandas as pd

# Create a simple dataframe
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# Save the dataframe to a JSON string to pass it to the next task
variables.put("dataframe_json", df.to_json())
print("Dataframe created and passed to Task 2.")
"""

# Task 2: Start a Flask application
@task.python(name="Flask_App", depends_on=["Load_Data"], virtual_env={"requirements": ["pandas", "flask"]})
def flask_app():
    return """
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
        html_response = f'''
        <h1>Data saved and pipeline will continue.</h1>
        <h2>Updated Dataframe:</h2>
        <pre>{df.to_string(index=False)}</pre>
        '''
        return html_response, 200
    except Exception as e:
        return f"Error in continue_pipeline: {e}", 400

@app.route('/stop', methods=['POST'])
def stop_pipeline():
    return "Pipeline terminated. You can close this page now.", 200

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

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

print("Starting Flask application...")
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()
"""

# Task 3: Display the final dataframe
@task.python(name="Display_Final_Dataframe", depends_on=["Flask_App"], virtual_env={"requirements": ["pandas"]})
def display_final_dataframe():
    return """
import pandas as pd

dataframe_json = variables.get("dataframe_json")
if not dataframe_json:
    print("Error: No dataframe_json found in variables!")
else:
    print("Dataframe JSON received in Task 3:", dataframe_json)

df = pd.read_json(dataframe_json)

print("Final dataframe:")
print(df)
"""

# Define the workflow using the @job decorator
@job(name="demo_pipeline_job")
def workflow():
    load_data()
    flask_app()
    display_final_dataframe()

# Execute the workflow
if __name__ == "__main__":
    workflow()
