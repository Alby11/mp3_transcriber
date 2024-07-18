# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt first to leverage Docker cache for dependencies
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg, ping, and curl
RUN apt-get update && apt-get install -y ffmpeg iputils-ping curl

# Copy the rest of the application
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Run transcribe.py when the container launches
CMD ["python", "transcribe.py"]
