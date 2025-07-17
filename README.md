# ICC1_todoapp_2 - Azure

## Purpose

This repository is meant to be used as a basis for the ICC1 module at Ada.
This is the second task for the part of learning for the capstone project.
Learners will deploy this in a virtual machine on a Cloud Provider such as AWS, Azure, or GCP. 

However, the database aspect has been separated, and is now stored in a serverless Azure Cosmos DB

A simple Flask-based To-Do application that lets you manage tasks with priorities.

## Features

- Add, view, and delete tasks
- Tasks have priorities (lower number = higher priority)
- Data stored in an Azure Cosmos DB

## Getting Started

### Prerequisites

- Python 3.12+
- Flask
- azure-cosmos library  (pip install azure-cosmos)

### Installation and Running 

- Azure: See the Tango Guide **[here](https://app.tango.us/app/workflow/Separating-the-database-from-the-compute---Creating-an-Azure-Cosmos-DB-Serverless-Instance-40067ef85d34476180b76ebea589c2a3)**



## Project Structure

- `app.py` — Main Flask application
- `templates/` — HTML templates

## License

MIT License
