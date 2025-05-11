# Django Task Manager API

Task manager API that can be set up using Docker and Docker Compose. It includes a Django Backend application, Redis, and MySQL.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd django-task-manager-api
   ```

2. **Build and Start the Services**

   Run the following command to build and start all services:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the Django application, Redis, and MySQL services.

3. **Environment Variables**

   Ensure the necessary environment variables are set. You can configure them in the `.env` file or directly in the `docker-compose.yml` file.

## Running the Celery Consumer Service

Make sure the `django-task-manager-api` service is up and running before starting the Celery consumer service.

To run the Celery consumer service, use the following command:

```bash
cd celery_consumer
docker-compose up
```

This command will start the Celery worker service defined in the `docker-compose.yml` file.

For more information of celery_consumer, refer to the [celery_consumer README](celery_consumer/README.md).