import pytest
from main import app, db, Task

# Use Flask's test client
@pytest.fixture
def client():
    # Set the app's testing configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for tests
    app.config['TESTING'] = True
    with app.app_context():  # Create an application context
        db.create_all()  # Create the tables in the test database
        with app.test_client() as client:
            yield client
        db.session.remove()
# Test GET /tasks endpoint without hitting the real database
def test_get_tasks(client, mocker):
    # Add tasks to the in-memory database before the test
    task1 = Task(title="New Task 1", description="Description for task 1", done=False)
    task2 = Task(title="New Task 2", description="Description for task 2", done=True)
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()

    # Now perform the GET request
    response = client.get('/tasks')

    # Check the response
    assert response.status_code == 200
    tasks = response.json['tasks']
    assert len(tasks) == 2
    assert tasks[0]['title'] == 'New Task 1'
    assert tasks[1]['done'] is True

# Test PUT /tasks/<task_id> endpoint (Update Task)
def test_update_task(client):
    # Add a task to the in-memory database before the test
    task = Task(title="Old Task", description="Old description", done=False)
    db.session.add(task)
    db.session.commit()

    updated_task_data = {
        'title': 'Updated Task',
        'description': 'Updated description',
        'done': True
    }

    # Perform the PUT request to update the task with ID 1
    response = client.put(f'/tasks/{task.id}', json=updated_task_data)

    # Check the response
    assert response.status_code == 200
    assert response.json['message'] == 'Task updated'
    updated_task = response.json['task']
    assert updated_task['title'] == 'Updated Task'
    assert updated_task['description'] == 'Updated description'
    assert updated_task['done'] is True

    # Verify the task was actually updated in the database
    updated_task_in_db = Task.query.get(task.id)
    assert updated_task_in_db.title == 'Updated Task'
    assert updated_task_in_db.description == 'Updated description'
    assert updated_task_in_db.done is True

# Test DELETE /tasks/<task_id> endpoint (Delete Task)
def test_delete_task(client):
    # Add a task to the in-memory database before the test
    task = Task(title="Task to delete", description="This task will be deleted", done=False)
    db.session.add(task)
    db.session.commit()

    # Perform the DELETE request to delete the task with ID 1
    response = client.delete(f'/tasks/{task.id}')

    # Check the response
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted'

    # Verify the task was actually deleted from the database
    deleted_task = Task.query.get(task.id)
    assert deleted_task is None  # Task should no longer exist in the databaseimport pytest