# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
# Retry mechanism added for pip install to handle transient issues
RUN for i in $(seq 1 5); do pip install --no-cache-dir -r /app/requirements.txt && break || sleep 2; done

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000

# Run app.py when the container launches
CMD ["python", "environment/app.py"]