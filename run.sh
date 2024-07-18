# Build the Docker image
docker build -t transcribe-audio .

# Run the Docker container
# docker run -v $(pwd):/usr/src/app transcribe-audio

# With host network mode
docker run -it --rm --network host -v $(pwd):/usr/src/app transcribe-audio
