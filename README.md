# Autonomous Code Review System

## Overview
This project implements an autonomous code review agent system that uses AI to analyze GitHub pull requests. It performs code style checks, detects potential bugs, suggests performance improvements, and ensures best practices are followed.

## Features

- **FastAPI API Endpoints**:
  - `POST /analyze-pr`: Start analyzing a GitHub pull request.
  - `GET /status/{task_id}`: Get the status of an analysis task.
  - `GET /results/{task_id}`: Retrieve analysis results.
- **Asynchronous Processing**:
  - Powered by Celery and Redis for task queuing and background processing.
- **AI-Powered Analysis**:
  - Uses OpenAI GPT-based models to review code files.
- **Database Integration**:
  - Task metadata and results stored in PostgreSQL and Redis.
- **Bonus Features**:
  - Dockerized deployment.
  - Basic caching of API results.
  - Meaningful logging.
  - Multi-language support for code analysis.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Docker and Docker Compose (for containerized setup)
- OpenAI API Key

## Installation and Setup (Without Docker)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the root directory.
   - Add the following:
     ```env
     OPENAI_API_KEY=<your_openai_api_key>
     REDIS_URL=redis://localhost:6379/0
     DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:<port>/<database_name>
     ```

5. Set up PostgreSQL and Redis:
   - Ensure PostgreSQL and Redis are running.
   - Create a database for the project.

6. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the Celery worker:
   ```bash
   celery -A app.workers.tasks worker --loglevel=info
   ```

8. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Running the Project (With Docker)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Verify the services:
   - FastAPI will be running at: `http://localhost:8000`
   - Redis container will be available on port `6379`.

4. To stop the containers:
   ```bash
   docker-compose down
   ```

## API Endpoints

1. **Start PR Analysis**
   - Endpoint: `POST /analyze-pr`
   - Request Body:
     ```json
     {
       "repo_url": "<github_repo_url>",
       "pr_number": <pull_request_number>
     }
     ```
   - Response:
     ```json
     {
       "task_id": "<task_id>"
     }
     ```

2. **Check Task Status**
   - Endpoint: `GET /status/{task_id}`
   - Response:
     ```json
     {
       "task_id": "<task_id>",
       "status": "pending" | "processing" | "completed" | "failed"
     }
     ```

3. **Retrieve Results**
   - Endpoint: `GET /results/{task_id}`
   - Response (example):
     ```json
     {
       "task_id": "<task_id>",
       "results": {
         "files": [
           {
             "name": "main.py",
             "issues": [
               {
                 "type": "style",
                 "line": 15,
                 "description": "Line too long",
                 "suggestion": "Break line into multiple lines"
               }
             ]
           }
         ],
         "summary": {
           "total_files": 1,
           "total_issues": 1,
           "critical_issues": 0
         }
       }
     }
     ```

## Docker Configuration

### Dockerfile
```dockerfile
# Use Python base image
FROM python:3.8-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### docker-compose.yml
```yaml
services:
  redis:
    image: redis:7.0
    container_name: redis_container
    ports:
      - "6379:6379"
    networks:
      - app_network

  celery_worker:
    build:
      context: .
    image: celery_worker_image
    container_name: celery_worker
    command: celery -A app.workers.tasks worker --loglevel=info
    depends_on:
      - redis
    networks:
      - app_network
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>

  fastapi_app:
    build:
      context: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - celery_worker
    networks:
      - app_network

networks:
  app_network:
    driver: bridge
```

## Logging and Caching

- **Logging**: All API and task events are logged to a file (`logs/app.log`).
- **Caching**: API results are cached in Redis to improve response times for repeated requests.

## Multi-Language Support
- The AI model supports code analysis for Python, JavaScript, Java, and more.
- Ensure the repository files contain valid code for accurate analysis.

## Live Deployment
- Deploy using platforms like AWS, Azure, or GCP.
- Use Docker for consistent environment configuration.

## Contribution Guidelines
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Open a pull request with a detailed description of your changes.

---

Feel free to reach out with any questions or suggestions for improvement!
