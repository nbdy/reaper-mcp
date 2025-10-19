from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from reaper_mcp.mcp_core import mcp
from reaper_mcp.util import RPR


@mcp.tool()
def list_vst_plugins() -> Dict[str, Any]:
    """List available VST plugins by parsing REAPER resource files (vstplugins*.ini)."""
    try:
        resource = RPR.GetResourcePath()
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
        n = int(RPR.CountTracks(0))
        if track_index < 0 or track_index >= n:
            return {"error": f"Track index out of range: {track_index}"}
        tr = RPR.GetTrack(0, track_index)
        rec_fx = 1 if record_fx_chain else 0
        fx_index = int(RPR.TrackFX_AddByName(tr, fx_name, rec_fx, 1))
        if fx_index < 0:
            return {"error": f"FX not found or could not be added: {fx_name}"}
        return {"track_index": track_index, "fx_index": fx_index}
    except Exception as e:
        return {"error": f"Failed to add FX: {e}"}


@mcp.tool()
def list_fx_on_track(track_index: int) -> Dict[str, Any]:
    """List FX names on a given track."""
    try:
        n = int(RPR.CountTracks(0))
        if track_index < 0 or track_index >= n:
            return {"error": f"Track index out of range: {track_index}"}
        tr = RPR.GetTrack(0, track_index)
        fx_count = int(RPR.TrackFX_GetCount(tr))
        fx = []
        for i in range(fx_count):
            buf = RPR.TrackFX_GetFXName(tr, i, "", 4096)
            name = buf[3] if isinstance(buf, tuple) and len(buf) >= 4 else str(buf)
            fx.append({"index": i, "name": name})
        return {"fx": fx}
    except Exception as e:
        return {"error": f"Failed to list FX: {e}"}


@mcp.tool()
def set_fx_param(track_index: int, fx_index: int, param_index: int, value_normalized: float) -> Dict[str, Any]:
    """Set an FX parameter (normalized 0..1)."""
    try:
        tr = RPR.GetTrack(0, int(track_index))
        ok = RPR.TrackFX_SetParamNormalized(tr, int(fx_index), int(param_index), float(value_normalized))
        return {"ok": bool(ok)}
    except Exception as e:
        return {"error": f"Failed to set FX param: {e}"}


@mcp.tool()
def get_fx_param(track_index: int, fx_index: int, param_index: int) -> Dict[str, Any]:
    """Get an FX parameter value and name."""
    try:
        tr = RPR.GetTrack(0, int(track_index))
        val = float(RPR.TrackFX_GetParamNormalized(tr, int(fx_index), int(param_index)))
        buf = RPR.TrackFX_GetParamName(tr, int(fx_index), int(param_index), "", 4096)
        name = buf[4] if isinstance(buf, tuple) and len(buf) >= 5 else str(buf)
        return {"value_normalized": val, "name": name}
    except Exception as e:
        return {"error": f"Failed to get FX param: {e}"}
