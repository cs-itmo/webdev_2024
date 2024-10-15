# Docker

This section demonstrates how to containerize Python applications using Docker. Examples include using Nginx, FastAPI, and a multi-container setup with Docker Compose.

## Files and Descriptions

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [index.html](index.html)                       | Main documentation for Docker lessons.                            |
| [1-nginx.yml](1-nginx.yml)                     | Docker Compose setup for Nginx as a reverse proxy.                |
| [2-python-http-server.yml](2-python-http-server.yml) | Docker setup for a simple Python HTTP server.                   |
| [3-adminer.yml](3-adminer.yml)                 | Docker setup for Adminer (Database management tool).              |

### FastAPI with Docker

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [4-fastapi/Dockerfile](4-fastapi/Dockerfile)   | Dockerfile for containerizing FastAPI.                            |
| [4-fastapi/docker-compose.yml](4-fastapi/docker-compose.yml) | Docker Compose setup for FastAPI.                                  |
| [4-fastapi/main.py](4-fastapi/main.py)         | Main FastAPI application file.                                     |

### FastAPI with Database

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [5-fastapi-db/Dockerfile](5-fastapi-db/Dockerfile) | Dockerfile for FastAPI with a database integration.               |
| [5-fastapi-db/docker-compose.yml](5-fastapi-db/docker-compose.yml) | Docker Compose setup for FastAPI and database.                    |
| [5-fastapi-db/main.py](5-fastapi-db/main.py)   | FastAPI application with database integration.                    |
| [5-fastapi-db/database.py](5-fastapi-db/database.py) | Database handling logic for FastAPI.                              |
| [5-fastapi-db/data/.gitkeep](5-fastapi-db/data/.gitkeep) | Placeholder for database files.                                   |

### Nginx with WebSocket and HTML App

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [6-docker-nginx-proxy-pass/docker-compose.yml](6-docker-nginx-proxy-pass/docker-compose.yml) | Multi-container setup using Docker Compose for Nginx, HTML app, and WebSocket app. |
| [6-docker-nginx-proxy-pass/nginx/nginx.conf](6-docker-nginx-proxy-pass/nginx/nginx.conf) | Nginx configuration for proxy pass.                               |
| [6-docker-nginx-proxy-pass/html_app/Dockerfile](6-docker-nginx-proxy-pass/html_app/Dockerfile) | Dockerfile for the HTML app.                                      |
| [6-docker-nginx-proxy-pass/html_app/main.py](6-docker-nginx-proxy-pass/html_app/main.py) | Main logic for the HTML app.                                      |
| [6-docker-nginx-proxy-pass/ws_app/Dockerfile](6-docker-nginx-proxy-pass/ws_app/Dockerfile) | Dockerfile for the WebSocket app.                                 |
| [6-docker-nginx-proxy-pass/ws_app/main.py](6-docker-nginx-proxy-pass/ws_app/main.py) | Main logic for the WebSocket app.                                 |

### Workers and Queues with Docker

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [7-workers/docker-compose.yml](7-workers/docker-compose.yml) | Docker Compose setup for worker-based applications.               |
| [7-workers/web/Dockerfile](7-workers/web/Dockerfile)         | Dockerfile for the worker application.                            |
| [7-workers/web/requirements.txt](7-workers/web/requirements.txt) | Dependencies for the worker app.                                  |
| [7-workers/web/main.py](7-workers/web/main.py) | Main logic for the worker-based application.                      |
| [7-workers/web/log.txt](7-workers/web/log.txt) | Log file for worker execution.                                    |
