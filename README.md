# midi-app

Starter app for generating Standard MIDI Files (SMF) with a Python backend and a plain HTML/JavaScript frontend. The structure keeps the music generation engine in Python while the browser UI stays simple and ready for a future Electron wrapper.

## Structure

```text
backend/
  app.py
  midi_engine.py
  requirements.txt
frontend/
  index.html
  app.js
  style.css
```

## Backend setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the FastAPI backend:

```bash
cd backend
uvicorn app:app --reload
```

The backend exposes:

- `GET /health`
- `POST /generate-midi`

## Frontend usage

Open `/home/runner/work/midi-app/midi-app/frontend/index.html` in a browser, or serve the `frontend/` folder with a small static server if preferred.

Fill in the controls, click **Generate MIDI**, and the browser will download `generated.mid`.

## Workflow

1. Start the backend with Uvicorn.
2. Open the frontend page.
3. Enter tempo, instrument, note CSV, ticks per note, and velocity.
4. Generate the MIDI file.
5. Open the downloaded `.mid` file in your DAW, media player, or MIDI editor.

## Architecture intent

- Python + `mido` handles SMF generation.
- FastAPI provides a local API boundary.
- Plain JS drives the UI and download flow.
- This split is ready for future desktop packaging with Electron, and can later evolve for other shells if needed.