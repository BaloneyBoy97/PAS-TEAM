# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system dependencies and upgrade pip
RUN apt-get update && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000

# Run app.py when the container launches
CMD ["python", "environment/app.py"]