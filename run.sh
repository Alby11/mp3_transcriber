# Build the Docker image
docker build -t transcribe-audio .

# Run the Docker container
docker run -v $(pwd):/usr/src/app transcribe-audio
