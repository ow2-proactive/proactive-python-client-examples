from proactive.decorators import task, job

# Example tasks defined using the task decorator
@task(name="task_1")
def task_1(param1, param2):
    return f'print("This is task 1 running on ProActive with param1={param1} and param2={param2}!")'

@task(name="task_2")
def task_2(**kwargs):
    return f'print("This is task 2 running on ProActive with kwargs={kwargs}!")'

@task(name="task_3", depends_on=["task_1", "task_2"])
def task_3():
    return 'print("This is task 3 running on ProActive!")'

# Example flow defined using the job decorator
@job(name="demo_decorators")
def workflow():
    # Register tasks with arguments
    task_1(10, 20)
    task_2(param1="value1", param2="value2")
    task_3()

# Execute the workflow
if __name__ == "__main__":
    workflow()
