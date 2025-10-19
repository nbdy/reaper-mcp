from __future__ import annotations

import os
import tempfile
import base64 as _b64
from typing import Any, Dict, List, Optional

import pretty_midi as pm

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import RPR


@mcp.tool()
def add_midi_to_track(
    track_index: int,
    notes: List[Dict[str, Any]],
    start_time: float = 0.0,
    quantize_qn: Optional[float] = None,
) -> Dict[str, Any]:
    """Add a list of MIDI notes to a track as a new MIDI item.

    notes: list of dicts with keys: start (s), end (s), pitch (0-127), velocity (1-127), channel (0-15)
    start_time: offset seconds for the item
    quantize_qn: if provided, quantize note starts/ends to this quarter-note grid
    """
    try:
        n = int(RPR.CountTracks(0))
        if track_index < 0 or track_index >= n:
            return {"error": f"Track index out of range: {track_index}"}
        tr = RPR.GetTrack(0, track_index)
        item_start = float(start_time)
        item_end = item_start + max((float(n["end"]) for n in notes), default=0.0)
        # Create new MIDI item in project
        item = RPR.CreateNewMIDIItemInProj(tr, item_start, item_end, False)
        take = RPR.GetActiveTake(item)
        if int(RPR.TakeIsMIDI(take)) != 1:
            return {"error": "Failed to create MIDI take."}
        # Insert notes
        for nd in notes:
            s = float(nd.get("start", 0.0)) + item_start
            e = float(nd.get("end", s + 0.25)) + item_start
            if quantize_qn is not None and quantize_qn > 0:
                ppq_s = RPR.MIDI_GetPPQPosFromProjTime(take, s)
                ppq_e = RPR.MIDI_GetPPQPosFromProjTime(take, e)
            else:
                ppq_s = RPR.MIDI_GetPPQPosFromProjTime(take, s)
                ppq_e = RPR.MIDI_GetPPQPosFromProjTime(take, e)
            chan = int(nd.get("channel", 0))
            pitch = int(nd.get("pitch", 60))
            vel = int(nd.get("velocity", 100))
            RPR.MIDI_InsertNote(
                take,
                False,
                False,
                ppq_s,
                ppq_e,
                chan,
                pitch,
                vel,
                False,
            )
        RPR.MIDI_Sort(take)
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to add MIDI: {e}"}


@mcp.tool()
def generate_midi_pattern(
    root_midi_note: int = 60,
    scale: str = "major",
    bars: int = 1,
    steps_per_bar: int = 16,
    velocity: int = 96,
) -> Dict[str, Any]:
    """Generate a simple step-sequenced MIDI pattern using pretty_midi-style output.

    Returns a list of notes dicts you can feed to add_midi_to_track.
    """
    try:
        steps = bars * steps_per_bar
        qn_per_step = 4.0 / steps_per_bar
        bpm = 120.0
        if RPR is not None:
            try:
                bpm = float(RPR.TimeMap_GetDividedBpmAtTime(0.0))
            except Exception:
                pass
        sec_per_qn = 60.0 / bpm
        # Simple scale intervals
        scales = {
            "major": [0, 2, 4, 5, 7, 9, 11, 12],
            "minor": [0, 2, 3, 5, 7, 8, 10, 12],
            "pentatonic": [0, 3, 5, 7, 10, 12],
        }
        intervals = scales.get(scale.lower(), scales["major"])
        notes = []
        for i in range(steps):
            degree = intervals[i % len(intervals)]
            pitch = int(root_midi_note + degree)
            start_qn = i * qn_per_step
            end_qn = start_qn + qn_per_step
            start_s = start_qn * sec_per_qn
            end_s = end_qn * sec_per_qn
            notes.append({
                "start": start_s,
                "end": end_s,
                "pitch": pitch,
                "velocity": int(velocity),
                "channel": 0,
            })
        return {"notes": notes, "bpm": bpm}
    except Exception as e:
        return {"error": f"Failed to generate MIDI: {e}"}


@mcp.tool()
def generate_pretty_midi(
    root_midi_note: int = 60,
    scale: str = "major",
    bars: int = 1,
    steps_per_bar: int = 16,
    velocity: int = 96,
    program: int = 0,
) -> Dict[str, Any]:
    """Generate a MIDI file (base64) using pretty_midi following a simple step sequence.

    Returns: { midi_base64: str, bpm: float }
    """
    try:
        # Determine BPM from REAPER if possible
        bpm = 120.0
        if RPR is not None:
            try:
                bpm = float(RPR.TimeMap_GetDividedBpmAtTime(0.0))
            except Exception:
                pass
        steps = max(1, int(bars * steps_per_bar))
        qn_per_step = 4.0 / steps_per_bar
        sec_per_qn = 60.0 / bpm

        scales = {
            "major": [0, 2, 4, 5, 7, 9, 11, 12],
            "minor": [0, 2, 3, 5, 7, 8, 10, 12],
            "pentatonic": [0, 3, 5, 7, 10, 12],
        }
        intervals = scales.get(scale.lower(), scales["major"])

        midi = pm.PrettyMIDI(initial_tempo=bpm)
        inst = pm.Instrument(program=max(0, min(127, int(program))))
        for i in range(steps):
            degree = intervals[i % len(intervals)]
            pitch = int(root_midi_note + degree)
            start_s = (i * qn_per_step) * sec_per_qn
            end_s = ((i + 1) * qn_per_step) * sec_per_qn
            inst.notes.append(pm.Note(velocity=int(velocity), pitch=pitch, start=start_s, end=end_s))
        midi.instruments.append(inst)

        # Write to temp file then encode
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=True) as tf:
            midi.write(tf.name)
            tf.seek(0)
            data = tf.read()
        return {"midi_base64": _b64.b64encode(data).decode("ascii"), "bpm": bpm}
    except Exception as e:
        return {"error": f"Failed to generate pretty_midi: {e}"}


@mcp.tool()
def add_midi_file_to_track(track_index: int, midi_base64: str, insert_time: float = 0.0) -> Dict[str, Any]:
    """Import a MIDI file (base64-encoded .mid data) onto the given track at time position."""
    try:
        n = int(RPR.CountTracks(0))
        if track_index < 0 or track_index >= n:
            return {"error": f"Track index out of range: {track_index}"}
        tr = RPR.GetTrack(0, track_index)

        # Decode to temp file
        data = _b64.b64decode(midi_base64.encode("ascii"))
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tf:
            tf.write(data)
            temp_path = tf.name
        try:
            RPR.SetEditCurPos(float(insert_time), False, False)
            RPR.SetOnlyTrackSelected(tr)
            ok = RPR.InsertMedia(temp_path, 0)
            if int(ok) != 1:
                return {"error": "InsertMedia failed for MIDI"}
            RPR.UpdateArrange()
            return {"ok": True}
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
    except Exception as e:
        return {"error": f"Failed to add MIDI file: {e}"}
