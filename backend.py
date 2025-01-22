from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Retrieve Deepgram API key from environment
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the speech transcription service!"}

@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    """
    Upload audio file for transcription.
    """
    try:
        # Read and validate the audio file
        audio_data = await audio.read()
        if not audio_data:
            return JSONResponse({"error": "No audio data provided"}, status_code=400)

        # Send audio data to Deepgram for transcription
        transcription = await transcribe_audio(audio_data)

        # Check for transcription errors
        if transcription.startswith("Error"):
            return JSONResponse({"error": transcription}, status_code=400)

        return JSONResponse({"transcription": transcription})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def transcribe_audio(audio_data):
    """
    Transcribe audio using Deepgram API.
    """
    url = "https://api.deepgram.com/v1/listen?language=en-au&model=nova-2-medical"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=audio_data)

    if response.status_code == 200:
        results = response.json().get("results", {})
        channels = results.get("channels", [{}])
        alternatives = channels[0].get("alternatives", [{}])
        return alternatives[0].get("transcript", "")
    else:
        error_message = response.json().get("error", "Unknown error occurred.")
        return f"Error in transcription: {error_message}"
