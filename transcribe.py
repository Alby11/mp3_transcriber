import speech_recognition as sr
from pydub import AudioSegment
import os
import signal
import time  # Add the missing import for time

# Paths
mp3_file_path = "audio.mp3"  # MP3 file in the same directory as the Dockerfile
wav_file_path = "temp_audio.wav"

# Convert MP3 to WAV
audio = AudioSegment.from_mp3(mp3_file_path)
audio.export(wav_file_path, format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()


# Function to handle timeout
class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


# Set the signal handler
signal.signal(signal.SIGALRM, timeout_handler)


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


# Transcribe with Google Speech Recognition
def transcribe_google():
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with sr.AudioFile(wav_file_path) as source:
                audio_data = recognizer.record(source)

            # Start the timer
            signal.alarm(20)  # Increase to 20 seconds timeout
            try:
                transcription = recognizer.recognize_google(audio_data)
                signal.alarm(0)  # Cancel the timer
                return transcription
            except TimeoutException:
                print(
                    f"Google Speech Recognition timed out. Retrying... ({attempt + 1}/{max_retries})"
                )
            except sr.RequestError as e:
                print(
                    f"Google RequestError: {e}. Retrying... ({attempt + 1}/{max_retries})"
                )
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
                return None
            except Exception as e:
                print(f"An unexpected error occurred with Google: {e}")
                return None
            finally:
                signal.alarm(0)  # Ensure the timer is canceled

            time.sleep(5)  # Wait for 5 seconds before retrying
        except Exception as e:
            print(f"An unexpected error occurred during retry: {e}")
            return None
    return None


# Test connectivity before attempting transcription
test_connectivity()

# Attempt transcription with Google
transcription = transcribe_google()
if transcription:
    print("Transcription:")
    print(transcription)
else:
    print("Failed to transcribe the audio with Google Speech Recognition.")
