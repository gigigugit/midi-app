from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from midi_engine import DEFAULT_NOTES, generate_midi_bytes

app = FastAPI(title="midi-app backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MidiRequest(BaseModel):
    tempo_bpm: int = Field(default=120, ge=20, le=300)
    instrument: int = Field(default=0, ge=0, le=127)
    notes: list[int] = Field(default_factory=lambda: DEFAULT_NOTES.copy())
    ticks_per_note: int = Field(default=480, ge=1, le=3840)
    velocity: int = Field(default=90, ge=1, le=127)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-midi")
def generate_midi(request: MidiRequest) -> Response:
    midi_bytes = generate_midi_bytes(
        tempo_bpm=request.tempo_bpm,
        instrument=request.instrument,
        notes=request.notes,
        ticks_per_note=request.ticks_per_note,
        velocity=request.velocity,
    )
    return Response(
        content=midi_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": 'attachment; filename="generated.mid"'},
    )
