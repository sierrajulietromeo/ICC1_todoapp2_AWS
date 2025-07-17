from flask import Flask, request, render_template, redirect, url_for
import os
from azure.cosmos import CosmosClient, PartitionKey

app = Flask(__name__)

# Cosmos DB config (set these as environment variables for security)
COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
COSMOS_KEY = os.environ.get('COSMOS_KEY')
COSMOS_DB = 'ICC1db'
COSMOS_CONTAINER = 'tasks'

# Initialize Cosmos client and container
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DB)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER,
    partition_key=PartitionKey(path="/id")
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    tasks = list(container.read_all_items())
    tasks.sort(key=lambda x: x.get('priority', 1))
    return render_template('tasks.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    priority = int(request.form.get('priority', 1))
    task_doc = {
        'id': str(hash(new_task + str(priority))),
        'task': new_task,
        'priority': priority
    }
    container.upsert_item(task_doc)
    return redirect(url_for('tasks'))

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    container.delete_item(item=task_id, partition_key=task_id)
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
