from __future__ import annotations

from typing import Any, Dict, List

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import RPR


@mcp.tool()
def get_project_details() -> Dict[str, Any]:
    """Get basic project details: bpm, track count, track names."""
    try:
        bpm = float(RPR.TimeMap_GetDividedBpmAtTime(0.0))
        n_tracks = int(RPR.CountTracks(0))
        tracks = []
        for i in range(n_tracks):
            tr = RPR.GetTrack(0, i)
            _, _, name, _ = RPR.GetSetMediaTrackInfo_String(tr, "P_NAME", "", False)
            tracks.append({"index": i, "name": name})
        return {"bpm": bpm, "track_count": n_tracks, "tracks": tracks}
    except Exception as e:
        return {"error": f"Failed to query project details: {e}"}


@mcp.tool()
def new_project(clear_tracks: bool = True) -> Dict[str, Any]:
    """Initialize the current project (optionally clearing all tracks)."""
    try:
        if clear_tracks:
            n = int(RPR.CountTracks(0))
            for i in range(n - 1, -1, -1):
                tr = RPR.GetTrack(0, i)
                RPR.DeleteTrack(tr)
        RPR.TrackList_AdjustWindows(False)
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to initialize project: {e}"}
