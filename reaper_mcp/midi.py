from __future__ import annotations

import logging
import os
import tempfile
import base64 as _b64
from typing import Any, Dict, List, Optional

import pretty_midi as pm
import reapy

from reaper_mcp.mcp_core import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def add_midi_to_track(
    track_index: int,
    notes: List[Dict[str, Any]],
    start_time: float = 0.0,
    quantize_qn: Optional[float] = None,
) -> Dict[str, Any]:
    """Add a list of MIDI notes to a track as a new MIDI item.

    Args:
        track_index: Track index (0-based) to add MIDI to
        notes: List of dicts with keys: start (s), end (s), pitch (0-127), velocity (1-127), channel (0-15)
        start_time: Offset seconds for the item
        quantize_qn: If provided, quantize note starts/ends to this quarter-note grid
    
    Note: If you receive a 422 error, ensure numeric parameters (track_index, start_time, quantize_qn)
          are sent as numbers, not strings.
    """
    logger.info(f"add_midi_to_track called with track_index={track_index}, start_time={start_time}, "
                f"quantize_qn={quantize_qn}, notes count={len(notes) if notes else 0}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            error_msg = f"Track index out of range: {track_index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        track = tracks[track_index]
        item_start = float(start_time)
        item_length = max((float(n["end"]) for n in notes), default=0.0)
        # Create new MIDI item in project
        item = track.add_midi_item(start=item_start, length=item_length)
        # Insert notes
        for nd in notes:
            start = float(nd.get("start", 0.0))
            end = float(nd.get("end", start + 0.25))
            channel = int(nd.get("channel", 0))
            pitch = int(nd.get("pitch", 60))
            velocity = int(nd.get("velocity", 100))
            item.add_note(pitch=pitch, start=start, end=end, velocity=velocity, channel=channel)
        logger.info(f"Successfully added {len(notes)} MIDI notes to track {track_index}")
        return {"ok": True}
    except Exception as e:
        error_msg = f"Failed to add MIDI: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


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
        try:
            project = reapy.Project()
            bpm = project.bpm
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
        try:
            project = reapy.Project()
            bpm = project.bpm
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
    """Import a MIDI file (base64-encoded .mid data) onto the given track at time position.
    
    Args:
        track_index: Track index (0-based) to add MIDI file to
        midi_base64: Base64-encoded MIDI file data
        insert_time: Time position in seconds to insert the MIDI
    
    Note: If you receive a 422 error, ensure numeric parameters (track_index, insert_time)
          are sent as numbers, not strings.
    """
    logger.info(f"add_midi_file_to_track called with track_index={track_index}, insert_time={insert_time}")
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            error_msg = f"Track index out of range: {track_index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        track = tracks[track_index]

        # Decode to temp file
        data = _b64.b64decode(midi_base64.encode("ascii"))
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tf:
            tf.write(data)
            temp_path = tf.name
        try:
            track.add_audio_item(file_path=temp_path, position=float(insert_time))
            logger.info(f"Successfully added MIDI file to track {track_index} at time {insert_time}")
            return {"ok": True}
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
    except Exception as e:
        error_msg = f"Failed to add MIDI file: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
