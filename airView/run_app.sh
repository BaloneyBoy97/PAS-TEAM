#!/bin/bash

# Run the Docker container
docker run -p 5001:5000 baloneyboy/my-python-app:v1 &

# Wait for a few seconds to ensure the container starts
sleep 5

# Open the browser
open http://127.0.0.1:5001