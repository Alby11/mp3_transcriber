# Audio Transcription Service

This project provides a Dockerized solution for transcribing audio files from MP3 to text. The service attempts to use Google Speech Recognition first, and falls back to Microsoft Azure Speech and Amazon Transcribe if needed.

## Features

- Convert MP3 to WAV format.
- Transcribe audio using Google Speech Recognition.
- Fall back to Microsoft Azure Speech and Amazon Transcribe if Google fails.
- Dockerized for easy setup and deployment.

## Prerequisites

- Docker
- API keys for Google Speech Recognition, Microsoft Azure Speech, and Amazon Transcribe.

## Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/audio-transcription-service.git
   cd audio-transcription-service
