from __future__ import annotations

from typing import Any, Dict, Optional

import reapy

from reaper_mcp.mcp_core import mcp
from reaper_mcp.project import get_project_details


@mcp.tool()
def create_track(name: Optional[str] = None, index: Optional[int] = None) -> Dict[str, Any]:
    """Create a new track at optional index; returns its index."""
    try:
        project = reapy.Project()
        n = len(project.tracks)
        idx = max(0, min(index if isinstance(index, int) else n, n))
        track = project.add_track(index=idx)
        if name:
            track.name = str(name)
        return {"index": idx, "name": name or ""}
    except Exception as e:
        return {"error": f"Failed to create track: {e}"}


@mcp.tool()
def delete_track(index: int) -> Dict[str, Any]:
    """Delete track by index."""
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if index < 0 or index >= len(tracks):
            return {"error": f"Track index out of range: {index}"}
        tracks[index].delete()
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to delete track: {e}"}


@mcp.tool()
def list_tracks() -> Dict[str, Any]:
    """List tracks with indices and names."""
    return get_project_details()
