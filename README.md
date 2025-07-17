# ICC1_todoapp_2 - AWS

## Purpose

This repository is meant to be used as a basis for the ICC1 module at Ada.
This is the second task for the part of learning for the capstone project.
Learners will deploy this in a virtual machine on a Cloud Provider such as AWS, Azure, or GCP. 

The database aspect has been implemented using a serverless AWS DynamoDB.

A simple Flask-based To-Do application that lets you manage tasks with priorities.

## Features

- Add, view, and delete tasks
- Tasks have priorities (higher number = higher priority)
- Data stored in an AWS DynamoDB NoSQL database

## Getting Started

### Prerequisites

- Python 3.9+
- Flask
- AWS Academy Learner Lab account
- EC2 instance running in AWS Academy environment

### Installation and Running

1. Clone this repository to your EC2 instance
2. Install pip and Python development tools:
   ```bash
   sudo yum update -y
   sudo yum install python3-pip python3-devel -y
   ```
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
5. Set AWS Academy environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_academy_access_key
   export AWS_SECRET_ACCESS_KEY=your_academy_secret_key
   export AWS_SESSION_TOKEN=your_academy_session_token
   export AWS_REGION=us-east-1  # Use the region of your AWS Academy lab
   export DYNAMODB_TABLE=ICC1_tasks
   ```
   
   > **Note**: You can find these credentials in your AWS Academy Learner Lab by clicking on the "AWS Details" button and looking for the "AWS CLI" section.
   
   > **Important**: AWS Academy credentials expire when your lab session ends. You'll need to update these environment variables with new values each time you start a new lab session.

6. Run the application: 
   ```bash
   python app.py
   ```
7. Access the application at: `http://your-ec2-public-ip:8080`

## Project Structure

- `app.py` — Main Flask application
- `templates/` — HTML templates
- `static/` — CSS and images
- `requirements.txt` — Python dependencies

## License

MIT License