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
