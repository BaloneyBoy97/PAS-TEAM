# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the specific app.py from the environment folder (if necessary)
COPY environment/app.py /app/app.py

# Copy the requirements.txt file
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Set environment variables for Flask
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
