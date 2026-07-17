const form = document.getElementById("midi-form");
const statusText = document.getElementById("status");
const backendUrl = "http://127.0.0.1:8000/generate-midi";

function clamp(value, minimum, maximum) {
  return Math.max(minimum, Math.min(maximum, value));
}

function parseNotes(csv) {
  const notes = csv
    .split(",")
    .map((part) => Number.parseInt(part.trim(), 10))
    .filter((note) => Number.isInteger(note))
    .map((note) => clamp(note, 0, 127));

  return notes.length > 0 ? notes : [60, 62, 64, 65, 67, 69, 71, 72];
}

function setStatus(message, isError = false) {
  statusText.textContent = message;
  statusText.classList.toggle("error", isError);
}

async function generateMidi(payload) {
  const response = await fetch(backendUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Backend request failed.");
  }

  return response.blob();
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("Generating MIDI...");

  const payload = {
    tempo_bpm: clamp(Number.parseInt(form.tempo_bpm.value, 10) || 120, 20, 300),
    instrument: clamp(Number.parseInt(form.instrument.value, 10) || 0, 0, 127),
    notes: parseNotes(form.notes.value),
    ticks_per_note: clamp(Number.parseInt(form.ticks_per_note.value, 10) || 480, 1, 3840),
    velocity: clamp(Number.parseInt(form.velocity.value, 10) || 90, 1, 127),
  };

  try {
    const blob = await generateMidi(payload);
    downloadBlob(blob, "generated.mid");
    setStatus("MIDI downloaded as generated.mid");
  } catch (error) {
    setStatus(`Error: ${error.message}`, true);
  }
});
