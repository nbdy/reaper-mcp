from __future__ import annotations

from typing import Any, Dict, Optional

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import RPR
from reaper_mcp.project import get_project_details


@mcp.tool()
def create_track(name: Optional[str] = None, index: Optional[int] = None) -> Dict[str, Any]:
    """Create a new track at optional index; returns its index."""
    try:
        n = int(RPR.CountTracks(0))
        idx = max(0, min(index if isinstance(index, int) else n, n))
        RPR.InsertTrackAtIndex(idx, True)
        tr = RPR.GetTrack(0, idx)
        if name:
            RPR.GetSetMediaTrackInfo_String(tr, "P_NAME", str(name), True)
        RPR.TrackList_AdjustWindows(False)
        return {"index": idx, "name": name or ""}
    except Exception as e:
        return {"error": f"Failed to create track: {e}"}


@mcp.tool()
def delete_track(index: int) -> Dict[str, Any]:
    """Delete track by index."""
    try:
        n = int(RPR.CountTracks(0))
        if index < 0 or index >= n:
            return {"error": f"Track index out of range: {index}"}
        tr = RPR.GetTrack(0, index)
        RPR.DeleteTrack(tr)
        RPR.TrackList_AdjustWindows(False)
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to delete track: {e}"}


@mcp.tool()
def list_tracks() -> Dict[str, Any]:
    """List tracks with indices and names."""
    return get_project_details()
