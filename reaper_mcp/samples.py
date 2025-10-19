from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import reapy

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import _load_sample_dirs, _save_sample_dirs

logger = logging.getLogger(__name__)


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

    Args:
        track_index: Track index (0-based) to import sample to
        file_path: Full path to the audio file to import
        insert_time: Time position in seconds to insert the sample
        time_stretch_playrate: If provided, sets the active take's playback rate (1.0 = no stretch, 2.0 = double speed)
    
    Note: If you receive a 422 error, ensure numeric parameters (track_index, insert_time, time_stretch_playrate)
          are sent as numbers, not strings.
    """
    logger.info(f"import_sample_to_track called with track_index={track_index}, file_path={file_path}, "
                f"insert_time={insert_time}, time_stretch_playrate={time_stretch_playrate}")
    if not Path(file_path).is_file():
        error_msg = f"File not found: {file_path}"
        logger.warning(error_msg)
        return {"error": error_msg}
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            error_msg = f"Track index out of range: {track_index} (valid: 0-{len(tracks)-1})"
            logger.warning(error_msg)
            return {"error": error_msg}
        track = tracks[track_index]
        # Insert audio item at the specified position
        item = track.add_audio_item(file_path=file_path, position=float(insert_time))
        if time_stretch_playrate is not None:
            take = item.active_take
            take.playback_rate = float(time_stretch_playrate)
        logger.info(f"Successfully imported sample to track {track_index} at time {insert_time}")
        return {"ok": True}
    except Exception as e:
        error_msg = f"Failed to import sample: {e}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
