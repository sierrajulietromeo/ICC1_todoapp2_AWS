from flask import Flask, request, render_template, redirect, url_for
import os
import boto3
from botocore.exceptions import ClientError
import uuid

app = Flask(__name__)

# DynamoDB config (set these as environment variables for security)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'ICC1_tasks')

# Initialize DynamoDB client
# For AWS Academy, we need to use the session token
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')
dynamodb = boto3.resource('dynamodb', 
                         region_name=AWS_REGION,
                         aws_session_token=AWS_SESSION_TOKEN)

# Check if table exists, if not create it
def create_table_if_not_exists():
    try:
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists with a timeout
        print(f"Waiting for table {DYNAMODB_TABLE} to be created (this may take up to 20 seconds)...")
        waiter = table.meta.client.get_waiter('table_exists')
        waiter.config.max_attempts = 20  # Approximately 20 seconds
        waiter.wait(TableName=DYNAMODB_TABLE)
        print(f"Table {DYNAMODB_TABLE} created successfully")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {DYNAMODB_TABLE} already exists")
        else:
            print(f"Error creating table: {e}")

# Global variable for the table
table = None

# Get the table
try:
    create_table_if_not_exists()
    table = dynamodb.Table(DYNAMODB_TABLE)
    # Verify table exists by making a simple API call
    table.table_status
    print(f"Successfully connected to DynamoDB table: {DYNAMODB_TABLE}")
except Exception as e:
    print(f"Error connecting to DynamoDB: {e}")
    print("WARNING: Application will run but database operations will fail!")
    # Create a dummy table object that will be used if real table creation failed
    table = dynamodb.Table(DYNAMODB_TABLE)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    try:
        if table is None:
            print("DynamoDB table not available")
            return render_template('tasks.html', tasks=[], error="Database not available")
            
        response = table.scan()
        tasks = response.get('Items', [])
        # Sort tasks by priority (higher number = higher priority)
        tasks.sort(key=lambda x: x.get('priority', 1), reverse=True)
        return render_template('tasks.html', tasks=tasks)
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return render_template('tasks.html', tasks=[], error=str(e))

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    priority = int(request.form.get('priority', 1))
    
    task_id = str(uuid.uuid4())
    
    try:
        if table is None:
            print("DynamoDB table not available")
            return redirect(url_for('tasks'))
            
        # Try to put the item with explicit error handling
        table.put_item(
            Item={
                'id': task_id,
                'task': new_task,
                'priority': priority
            }
        )
        print(f"Task added successfully: {new_task}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"DynamoDB error: {error_code} - {error_message}")
        if 'ValidationException' in error_code and 'Missing the key' in error_message:
            print("Table schema mismatch. Check your table's partition key name.")
    except Exception as e:
        print(f"Error adding task: {e}")
    
    return redirect(url_for('tasks'))

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        table.delete_item(
            Key={
                'id': task_id
            }
        )
    except Exception as e:
        print(f"Error deleting task: {e}")
    
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)