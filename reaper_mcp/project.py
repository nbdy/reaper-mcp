from __future__ import annotations

from typing import Any, Dict, List

import reapy

from reaper_mcp.mcp_core import mcp


@mcp.tool()
def get_project_details() -> Dict[str, Any]:
    """Get basic project details: bpm, track count, track names."""
    try:
        project = reapy.Project()
        bpm = project.bpm
        tracks = []
        for i, track in enumerate(project.tracks):
            tracks.append({"index": i, "name": track.name})
        return {"bpm": bpm, "track_count": len(tracks), "tracks": tracks}
    except Exception as e:
        return {"error": f"Failed to query project details: {e}"}


@mcp.tool()
def new_project(clear_tracks: bool = True) -> Dict[str, Any]:
    """Initialize the current project (optionally clearing all tracks)."""
    try:
        if clear_tracks:
            project = reapy.Project()
            # Delete tracks in reverse order to avoid index shifting issues
            for track in reversed(list(project.tracks)):
                track.delete()
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to initialize project: {e}"}


@mcp.tool()
def get_project_length() -> Dict[str, Any]:
    """Get the project length in seconds."""
    try:
        project = reapy.Project()
        length = project.length
        return {"length": length}
    except Exception as e:
        return {"error": f"Failed to get project length: {e}"}


@mcp.tool()
def save_project() -> Dict[str, Any]:
    """Save the current project."""
    try:
        project = reapy.Project()
        project.save()
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to save project: {e}"}


@mcp.tool()
def get_play_state() -> Dict[str, Any]:
    """Get the current playback state (playing, paused, stopped, recording)."""
    try:
        project = reapy.Project()
        state = {
            "is_playing": project.is_playing,
            "is_paused": project.is_paused,
            "is_stopped": project.is_stopped,
            "is_recording": project.is_recording
        }
        return state
    except Exception as e:
        return {"error": f"Failed to get play state: {e}"}


@mcp.tool()
def get_play_position() -> Dict[str, Any]:
    """Get the current play position in seconds."""
    try:
        project = reapy.Project()
        position = project.play_position
        return {"position": position}
    except Exception as e:
        return {"error": f"Failed to get play position: {e}"}


@mcp.tool()
def get_play_rate() -> Dict[str, Any]:
    """Get the current playback rate (1.0 is normal speed)."""
    try:
        project = reapy.Project()
        rate = project.play_rate
        return {"rate": rate}
    except Exception as e:
        return {"error": f"Failed to get play rate: {e}"}


@mcp.tool()
def undo() -> Dict[str, Any]:
    """Undo the last action in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    try:
        project = reapy.Project()
        project.undo()
        return {"ok": True, "action": "undo"}
    except Exception as e:
        return {"error": f"Failed to undo: {e}"}


@mcp.tool()
def redo() -> Dict[str, Any]:
    """Redo the last undone action in REAPER.
    
    Returns:
        Dict with ok status on success or error message
    """
    try:
        project = reapy.Project()
        project.redo()
        return {"ok": True, "action": "redo"}
    except Exception as e:
        return {"error": f"Failed to redo: {e}"}


@mcp.tool()
def can_undo() -> Dict[str, Any]:
    """Check if undo is available.
    
    Returns:
        Dict with can_undo boolean
    """
    try:
        project = reapy.Project()
        can_undo_val = project.can_undo()
        return {"can_undo": can_undo_val}
    except Exception as e:
        return {"error": f"Failed to check undo availability: {e}"}


@mcp.tool()
def can_redo() -> Dict[str, Any]:
    """Check if redo is available.
    
    Returns:
        Dict with can_redo boolean
    """
    try:
        project = reapy.Project()
        can_redo_val = project.can_redo()
        return {"can_redo": can_redo_val}
    except Exception as e:
        return {"error": f"Failed to check redo availability: {e}"}


@mcp.tool()
def beats_to_time(beats: float) -> Dict[str, Any]:
    """Convert beats to time in seconds.
    
    Args:
        beats: Number of beats (quarter notes)
    
    Returns:
        Dict with time in seconds
    """
    try:
        project = reapy.Project()
        time = project.beats_to_time(float(beats))
        return {"beats": beats, "time": time}
    except Exception as e:
        return {"error": f"Failed to convert beats to time: {e}"}


@mcp.tool()
def time_to_beats(time: float) -> Dict[str, Any]:
    """Convert time in seconds to beats.
    
    Args:
        time: Time in seconds
    
    Returns:
        Dict with beats (quarter notes)
    """
    try:
        project = reapy.Project()
        beats = project.time_to_beats(float(time))
        return {"time": time, "beats": beats}
    except Exception as e:
        return {"error": f"Failed to convert time to beats: {e}"}


@mcp.tool()
def get_project_name() -> Dict[str, Any]:
    """Get the project name.
    
    Returns:
        Dict with project name
    """
    try:
        project = reapy.Project()
        name = project.name
        return {"name": name}
    except Exception as e:
        return {"error": f"Failed to get project name: {e}"}


@mcp.tool()
def get_project_path() -> Dict[str, Any]:
    """Get the project file path.
    
    Returns:
        Dict with project path (empty string if not saved)
    """
    try:
        project = reapy.Project()
        path = project.path
        return {"path": path}
    except Exception as e:
        return {"error": f"Failed to get project path: {e}"}


@mcp.tool()
def is_project_dirty() -> Dict[str, Any]:
    """Check if the project has unsaved changes.
    
    Returns:
        Dict with is_dirty boolean
    """
    try:
        project = reapy.Project()
        dirty = project.is_dirty()
        return {"is_dirty": dirty}
    except Exception as e:
        return {"error": f"Failed to check project dirty status: {e}"}
