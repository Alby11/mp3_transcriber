import speech_recognition as sr
from pydub import AudioSegment
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError
import os
import time
import azure.cognitiveservices.speech as speechsdk

# Paths
mp3_file_path = "audio.mp3"  # MP3 file in the same directory as the Dockerfile
wav_file_path = "temp_audio.wav"

# Convert MP3 to WAV
audio = AudioSegment.from_mp3(mp3_file_path)
audio.export(wav_file_path, format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()


# Transcribe with Google Speech Recognition
def transcribe_google():
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with sr.AudioFile(wav_file_path) as source:
                audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            return transcription
        except sr.RequestError as e:
            print(
                f"Google RequestError: {e}. Retrying... ({attempt + 1}/{max_retries})"
            )
            time.sleep(5)  # Wait for 5 seconds before retrying
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred with Google: {e}")
            return None
    return None


# Transcribe with Azure Speech Recognition
def transcribe_azure():
    try:
        speech_key = "YOUR_AZURE_SPEECH_KEY"
        service_region = "YOUR_AZURE_SERVICE_REGION"

        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region
        )
        audio_config = speechsdk.audio.AudioConfig(filename=wav_file_path)

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized with Azure.")
        else:
            print(f"Azure Speech Recognition error: {result.reason}")
    except Exception as e:
        print(f"An unexpected error occurred with Azure: {e}")
    return None


# Transcribe with Amazon Transcribe
def transcribe_amazon():
    try:
        transcribe_client = boto3.client(
            "transcribe", region_name="us-east-1"
        )  # Replace with your AWS region

        job_name = "transcription_job"
        job_uri = "file://" + os.path.abspath(wav_file_path)

        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": job_uri},
            MediaFormat="wav",
            LanguageCode="en-US",
        )

        while True:
            status = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
                "COMPLETED",
                "FAILED",
            ]:
                break
            print("Waiting for Amazon Transcribe to complete...")
            time.sleep(10)

        if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            transcription = status["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            return transcription
    except (BotoCoreError, NoCredentialsError, ClientError) as e:
        print(f"Amazon Transcribe error: {e}")
    return None


# Attempt transcription with Google first, then Azure, then Amazon
transcription = transcribe_google()
if not transcription:
    print("Google failed, trying Azure...")
    transcription = transcribe_azure()
if not transcription:
    print("Azure failed, trying Amazon...")
    transcription = transcribe_amazon()

if transcription:
    print("Transcription:")
    print(transcription)
else:
    print("Failed to transcribe the audio with all services.")
