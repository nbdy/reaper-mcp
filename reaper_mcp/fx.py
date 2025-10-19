from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import reapy

from reaper_mcp.mcp_core import mcp


@mcp.tool()
def list_vst_plugins() -> Dict[str, Any]:
    """List available VST plugins by parsing REAPER resource files (vstplugins*.ini)."""
    try:
        resource = reapy.get_resource_path()
        base = Path(resource)
        candidates = [
            base / "reaper-vstplugins64.ini",
            base / "reaper-vstplugins.ini",
            base / "reaper-vstplugins-arm64.ini",
        ]
        plugins: List[str] = []
        for p in candidates:
            if p.exists():
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and "=" in line:
                            name = line.split("=", 1)[0].strip()
                            if name and name not in plugins:
                                plugins.append(name)
        return {"plugins": plugins}
    except Exception as e:
        return {"error": f"Failed to list VST plugins: {e}"}


@mcp.tool()
def add_fx_to_track(track_index: int, fx_name: str, record_fx_chain: bool = False) -> Dict[str, Any]:
    """Add an FX/VST by name to a track. fx_name must match REAPER's FX browser name (e.g., 'VST3: ReaComp (Cockos)')."""
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            return {"error": f"Track index out of range: {track_index}"}
        track = tracks[track_index]
        fx = track.add_fx(name=fx_name, even_if_exists=True)
        if fx is None:
            return {"error": f"FX not found or could not be added: {fx_name}"}
        fx_index = fx.index
        return {"track_index": track_index, "fx_index": fx_index}
    except Exception as e:
        return {"error": f"Failed to add FX: {e}"}


@mcp.tool()
def list_fx_on_track(track_index: int) -> Dict[str, Any]:
    """List FX names on a given track."""
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        if track_index < 0 or track_index >= len(tracks):
            return {"error": f"Track index out of range: {track_index}"}
        track = tracks[track_index]
        fx = []
        for i, fx_obj in enumerate(track.fxs):
            fx.append({"index": i, "name": fx_obj.name})
        return {"fx": fx}
    except Exception as e:
        return {"error": f"Failed to list FX: {e}"}


@mcp.tool()
def set_fx_param(track_index: int, fx_index: int, param_index: int, value_normalized: float) -> Dict[str, Any]:
    """Set an FX parameter (normalized 0..1)."""
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        track = tracks[int(track_index)]
        fxs = list(track.fxs)
        fx = fxs[int(fx_index)]
        params = list(fx.params)
        param = params[int(param_index)]
        param.normalized = float(value_normalized)
        return {"ok": True}
    except Exception as e:
        return {"error": f"Failed to set FX param: {e}"}


@mcp.tool()
def get_fx_param(track_index: int, fx_index: int, param_index: int) -> Dict[str, Any]:
    """Get an FX parameter value and name."""
    try:
        project = reapy.Project()
        tracks = list(project.tracks)
        track = tracks[int(track_index)]
        fxs = list(track.fxs)
        fx = fxs[int(fx_index)]
        params = list(fx.params)
        param = params[int(param_index)]
        return {"value_normalized": param.normalized, "name": param.name}
    except Exception as e:
        return {"error": f"Failed to get FX param: {e}"}
