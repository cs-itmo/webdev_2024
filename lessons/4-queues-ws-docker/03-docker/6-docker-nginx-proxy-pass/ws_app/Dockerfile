# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file if you have any additional dependencies (optional)
COPY main.py .

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn[standard]

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
