import requests
import speech_recognition as sr
from pydub import AudioSegment
import os
import time

# Paths
mp3_file_path = "audio.mp3"  # MP3 file in the same directory as the Dockerfile
wav_file_path = "temp_audio.wav"

# Convert MP3 to WAV
audio = AudioSegment.from_mp3(mp3_file_path)
audio.export(wav_file_path, format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()


# Test network connectivity
def test_connectivity():
    try:
        response = os.system("ping -c 1 google.com")
        if response == 0:
            print("Network connectivity: OK")
        else:
            print("Network connectivity: FAILED")
        response = os.system("curl -s --head http://www.google.com")
        if response == 0:
            print("HTTP connectivity: OK")
        else:
            print("HTTP connectivity: FAILED")
    except Exception as e:
        print(f"Error testing network connectivity: {e}")


# Manually interact with Google Speech Recognition API
def transcribe_google_manual():
    google_speech_api_url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=YOUR_GOOGLE_API_KEY"
    headers = {
        "Content-Type": "audio/l16; rate=16000",
    }

    with open(wav_file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(
                google_speech_api_url, headers=headers, data=audio_data, timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                transcription = result["result"][0]["alternative"][0]["transcript"]
                return transcription
            else:
                print(
                    f"Google API error: {response.status_code}. Retrying... ({attempt + 1}/{max_retries})"
                )
        except requests.exceptions.RequestException as e:
            print(f"RequestException: {e}. Retrying... ({attempt + 1}/{max_retries})")
        except Exception as e:
            print(
                f"An unexpected error occurred with Google API: {e}. Retrying... ({attempt + 1}/{max_retries})"
            )

        time.sleep(5)  # Wait for 5 seconds before retrying
    return None


# Test connectivity before attempting transcription
test_connectivity()

# Attempt transcription with manual Google API interaction
transcription = transcribe_google_manual()
if transcription:
    print("Transcription:")
    print(transcription)
else:
    print("Failed to transcribe the audio with Google Speech Recognition.")
