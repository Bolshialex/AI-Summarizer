# Summarizer-AI

## Prerequisites

- Python 3.11+
- Node.js 18+ (for the frontend)
- **ffmpeg** — required by the speech-to-text component to extract audio from video files and split long audio into chunks.

Install ffmpeg:

- **Mac:** `brew install ffmpeg`
- **Windows:** `choco install ffmpeg` (or download a build from https://www.gyan.dev/ffmpeg/builds/ and add it to your PATH)

> Before the `/transcribe` endpoint will work, you also need a Groq API key. See [Speech-to-Text API → Environment Setup](#environment-setup) at the bottom of this file.

## First-Time Setup (Manual)

The first time you clone the project, follow these steps to create the virtual environment and install dependencies. After this is done once, you can use the script in the next section for daily startup.

### MAC:

To start, make sure you're in the `backend` folder first.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn main:app --reload
```

- **Ctrl + C** to stop the server.

Deactivate the virtual environment:

```bash
deactivate
```

---

### Windows:

To start, make sure you're in the `backend` folder first.

Create a virtual environment:

```cmd
python -m venv venv
```

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
python -m pip install -r requirements.txt
```

Start the backend server:

```cmd
uvicorn main:app --reload
```

- **Ctrl + C** to stop the server.

Deactivate the virtual environment:

```cmd
deactivate
```

## Daily Startup (Auto Run W/ Script)

After the first-time setup is done, you can use this script for daily startup. It activates the venv, updates any missing dependencies, and starts the server in one command.

### Mac / Linux

**1. Make it executable (one-time setup):**
Open your terminal in the `backend` folder and run:

```bash
chmod +x run_server.sh
```

**2. Run the server:**
Whenever you want to start the backend, just open your terminal in the `backend` folder and run:

```bash
./run_server.sh
```

---

### Windows

**1. Run the server:**
Whenever you want to start the backend, you can either:

- Double-click the `run_server.bat` file in File Explorer.
- OR, open your terminal/command prompt in the `backend` folder and type:
  ```cmd
  run_server.bat
  ```

## Updating Dependencies

To save your current dependencies into `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Speech-to-Text API

The backend exposes `POST /transcribe`, which accepts an audio or video file and returns a transcript with per-segment timestamps. It runs on Groq's free Whisper API.

### Environment Setup

**1. Get a Groq API key:**
Sign up at https://console.groq.com (free, no credit card required), then create a key at https://console.groq.com/keys.

**2. Create your `.env`:**
In the `backend` folder, copy the example file:

```bash
cp .env.example .env
```

**3. Add your key:**
Open `backend/.env` and replace `your_groq_api_key_here` with the key you just created.

> `.env` is gitignored — never commit it.

### Test it via Swagger UI

Once the backend is running and your `.env` is set up:

**1.** Open http://127.0.0.1:8000/docs in your browser.

**2.** Expand `POST /transcribe` → click **Try it out** → choose an audio or video file → click **Execute**.

You'll get back JSON like:

```json
{
  "text": "Full transcript of the audio...",
  "segments": [
    { "start": 0.0, "end": 4.2, "text": "First segment of speech" },
    { "start": 4.2, "end": 9.8, "text": "Second segment of speech" }
  ]
}
```

### Notes

- **Video files work too** — ffmpeg pulls the audio track automatically. Tested with MP3, MP4, WAV, M4A.
- **Large files** (>25 MB) are split into 20-minute chunks and stitched back together, so long podcasts work fine.
- **Multilingual** — Whisper handles ~100 languages out of the box; no need to specify.
- **Model:** Groq `whisper-large-v3-turbo` (free tier).