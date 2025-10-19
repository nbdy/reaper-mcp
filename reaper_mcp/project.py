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
