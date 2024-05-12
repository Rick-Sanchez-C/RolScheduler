# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN
ARG TIME_ZONE
ENV TIME_ZONE=$TIME_ZONE

# Run main.py when the container launches
CMD ["python", "main.py"]