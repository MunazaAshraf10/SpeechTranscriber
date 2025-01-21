from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx  # Async HTTP library
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORSMiddleware to allow frontend to communicate with backend
origins = [
    "http://127.0.0.1:8001",  # Allow frontend to communicate with backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_methods =['POST', 'GET']
)

# Serve static files (e.g., index.html) from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Get API key from the environment
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the speech transcription service!"}

@app.get("/favicon.ico")
async def favicon():
    return None  # Or provide a file path to a favicon.ico if you want

@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    try:
        audio_data = await audio.read()
        if not audio_data:
            return JSONResponse({"error": "No audio data provided"}, status_code=400)
        
        chunks = chunk_audio(audio_data)  # Function to chunk audio
        
        transcriptions = []
        for chunk in chunks:
            transcription = await transcribe_audio(chunk)
            transcriptions.append(transcription)

        return JSONResponse({"transcription": " ".join(transcriptions)})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

def chunk_audio(audio_data):
    # Here, split the audio into chunks for faster processing
    chunk_size = 1024 * 1024  # Adjust this based on your need
    return [audio_data[i:i + chunk_size] for i in range(0, len(audio_data), chunk_size)]

async def transcribe_audio(chunk):
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }

    # Use httpx for async HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=chunk)
    
    if response.status_code == 200:
        return response.json().get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', "")
    else:
        return f"Error in transcription: {response.status_code}"
