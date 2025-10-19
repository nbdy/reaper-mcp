from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import reapy

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import _load_sample_dirs, _save_sample_dirs


@mcp.tool()
def list_sample_dirs() -> Dict[str, Any]:
    """List configured sample directories."""
    return {"sample_dirs": _load_sample_dirs()}


@mcp.tool()
def add_sample_dir(path: str) -> Dict[str, Any]:
    """Add a sample directory (persisted)."""
    if not path:
        return {"error": "Path is required"}
    dirs = _load_sample_dirs()
    if path not in dirs:
        dirs.append(path)
        _save_sample_dirs(dirs)
    return {"sample_dirs": dirs}


@mcp.tool()
def remove_sample_dir(path: str) -> Dict[str, Any]:
    """Remove a sample directory."""
    dirs = [d for d in _load_sample_dirs() if d != path]
    _save_sample_dirs(dirs)
    return {"sample_dirs": dirs}


@mcp.tool()
def search_samples(query: Optional[str] = None, exts: Optional[List[str]] = None, limit: int = 100) -> Dict[str, Any]:
    """Search for audio samples across configured directories.

    query: substring to match in file names (case-insensitive)
    exts: list of extensions to include (default: wav,aiff,flac,mp3,ogg)
    limit: maximum results
    """
    dirs = _load_sample_dirs()
    if not dirs:
        return {"error": "No sample directories configured."}
    if not exts:
        exts = [".wav", ".aiff", ".aif", ".flac", ".mp3", ".ogg"]
    q = (query or "").lower()
    results: List[str] = []
    try:
        for d in dirs:
            base = Path(d)
            for root, _, files in os.walk(base):
                root_p = Path(root)
                for fn in files:
                    if any(fn.lower().endswith(e) for e in exts):
                        if not q or q in fn.lower():
                            results.append(str(root_p / fn))
                            if len(results) >= limit:
                                return {"files": results}
        return {"files": results}
    except Exception as e:
        return {"error": f"Failed to search samples: {e}"}


@mcp.tool()
def import_sample_to_track(track_index: int, file_path: str, insert_time: float = 0.0, time_stretch_playrate: Optional[float] = None) -> Dict[str, Any]:
    """Import a sample onto the given track at time position. Optionally set take playrate for time-stretching.

    time_stretch_playrate: if provided, sets the active take's D_PLAYRATE to this value (1.0 = no stretch)
    """
    if not Path(file_path).is_file():
        return {"error": f"File not found: {file_path}"}
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            return {"error": f"Track index out of range: {track_index}"}
        track = tracks[track_index]
        # Insert audio item at the specified position
        item = track.add_audio_item(file_path=file_path, position=float(insert_time))
        if time_stretch_playrate is not None:
            take = item.active_take
            take.playback_rate = float(time_stretch_playrate)
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to import sample: {e}"}
