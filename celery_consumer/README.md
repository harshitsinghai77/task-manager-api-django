# Celery Consumer 

## Setup

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Docker Compose Setup

To set up the project using Docker Compose, follow these steps:

1. Ensure Docker and Docker Compose are installed on your system.

2. Clone the repository:
```bash
 git clone <repository-url>
```

3. Navigate to the project directory:
```bash
cd django-task-manager-api
cd celery_consumer
```

4. Make sure the `django-task-manager-api` service is up and running before starting the Celery consumer service.

5. Build and start the services:
```bash
docker-compose up --build
```

6. To run the Celery consumer service separately:
```bash
docker-compose up celery_consumer
```
The service will spin up 3 services:
1. Celery consumer with default queue
2. Celery consumer with dlq queue
3. Flower UI for monitoring the Celery tasks

Flower UI: http://127.0.0.1:5555/

The Celery Consumer with default queue:
1. Consumes tasks from the `default` queue
2. If a task fails, it will be retried up to 3 times with a delay of 2 seconds between retries
3. If a task fails 3 times, it will be sent to the `dlq` queue

The Celery Consumer with dlq queue:
1. Consumes tasks from the `dlq` queue
2. Put it in the dead_letter_queue_task table for further analysis
