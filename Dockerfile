FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306
ENV MYSQL_DATABASE=task_db
ENV MYSQL_USER=djangouser
ENV MYSQL_PASSWORD=mypassword

# Run Django development server
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
EXPOSE 8000