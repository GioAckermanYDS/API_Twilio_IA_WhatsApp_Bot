# Use the official Python image as the base image
FROM python:3.10.5-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install gcc
RUN apt-get update --allow-insecure-repositories \
    && apt-get install -y gcc

RUN apt-get update && apt-get install -y build-essential

# Install the Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the Flask application will run on
EXPOSE 3002

# Add a volume to the container
VOLUME /app/logs

# Run the RQ worker in the background
CMD gunicorn app.main:app --log-level info --workers 6 --worker-class "uvicorn.workers.UvicornWorker" --bind 0.0.0.0:3002 --timeout 240