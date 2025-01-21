# SpeechTranscriber

A real-time voice-to-text application that uses FastAPI and Deepgram API for speech transcription. This application allows users to upload audio, and the speech is transcribed as it's being spoken, using chunks for faster processing.

## Features

- Real-time audio-to-text transcription
- Chunked processing for faster transcription
- Built with FastAPI for the backend and Deepgram API for transcription
- Easy-to-use frontend for uploading audio

## Installation

### 1. Clone the Repository

git clone https://github.com/MunazaAshraf/SpeechTranscriber.git
cd SpeechTranscriber

### 2. Set up the Environment
Create a virtual environment to isolate the project's dependencies:
python -m venv venv

Activate the virtual environment:

On Windows:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate

### 3. Install Dependencies
Install the required packages from the requirements.txt file:
pip install -r requirements.txt

### 4. Set up API Key
Create a .env file in the root directory of your project and add your Deepgram API key:
DEEPGRAM_API_KEY=your_deepgram_api_key

### 5. Run the Backend (FastAPI)
Start the FastAPI server by running the following command:
uvicorn main:app --reload
The server will be running on http://127.0.0.1:8000. You can interact with the API via a frontend or Postman.

### 6. Run the Frontend (Static File Server)
To serve the frontend files (frontend.html), use a simple HTTP server to serve your static files.
In the terminal, navigate to the directory where frontend.html is located and run the following command:
python -m http.server 8001 --bind 127.0.0.1
The frontend will be accessible at http://127.0.0.1:8001 and will allow users to upload audio files for transcription.
