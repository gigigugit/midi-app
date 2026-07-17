from io import BytesIO

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

DEFAULT_NOTES = [60, 62, 64, 65, 67, 69, 71, 72]


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def normalize_notes(notes: list[int] | None) -> list[int]:
    if not notes:
        return DEFAULT_NOTES.copy()

    normalized = []
    for note in notes:
        try:
            normalized.append(clamp(int(note), 0, 127))
        except (TypeError, ValueError):
            continue

    return normalized or DEFAULT_NOTES.copy()


def generate_midi_bytes(
    tempo_bpm: int = 120,
    instrument: int = 0,
    notes: list[int] | None = None,
    ticks_per_note: int = 480,
    velocity: int = 90,
) -> bytes:
    tempo_bpm = clamp(int(tempo_bpm), 20, 300)
    instrument = clamp(int(instrument), 0, 127)
    ticks_per_note = clamp(int(ticks_per_note), 1, 3840)
    velocity = clamp(int(velocity), 1, 127)
    note_values = normalize_notes(notes)

    midi_file = MidiFile(type=1, ticks_per_beat=480)
    track = MidiTrack()
    midi_file.tracks.append(track)

    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(tempo_bpm), time=0))
    track.append(Message("program_change", program=instrument, channel=0, time=0))

    for note in note_values:
        track.append(Message("note_on", note=note, velocity=velocity, channel=0, time=0))
        track.append(Message("note_off", note=note, velocity=0, channel=0, time=ticks_per_note))

    buffer = BytesIO()
    midi_file.save(file=buffer)
    buffer.seek(0)
    return buffer.read()
